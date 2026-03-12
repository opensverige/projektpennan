"""
Skooli Buddy Telegram-bot.
Hanterar GDPR-samtyckesgate, sessionsgränser och Sokratiska svar.
Texter och regler enligt SKOOLI_BUDDY_SAFETY_SPEC.md.
"""
import os
import sys
from datetime import datetime, timezone, timedelta

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv

from .consent import has_consent, record_consent, revoke_consent
from .core import get_response, reset_chat
from .logger import log_turn, delete_logs_for_chat

load_dotenv()

# Enda tillåtna användaren — ignorera alla andra
ALLOWED_CHAT_ID = 544123218

# Sessionsgränser (DEL 2)
SESSION_MSG_LIMIT = 30
DAY_MSG_LIMIT = 100
PAUSE_MINUTES = 15

# Session state (in-memory, nollställs vid omstart)
_session_counts: dict[int, int] = {}
_pause_until: dict[int, datetime] = {}
_day_counts: dict[int, dict] = {}   # {chat_id: {"count": int, "date": "YYYY-MM-DD"}}
_turn_counts: dict[int, int] = {}   # absolut turn-nummer per chat_id


# ── DEL 7: Felmeddelanden (kopierade ordagrant) ──────────────────────────────
ERROR_GEMINI         = "Oj, jag tänkte för länge! 🤔 Kan du säga det igen?"
ERROR_SAFETY_FILTER  = "Det där kan jag inte hjälpa med just nu. Vill du utforska något annat? 😊"
ERROR_IMAGE_ANALYSIS = "Hmm, jag kunde inte riktigt se bilden. Kan du ta en ny? 📸"
ERROR_IMAGE_GEN      = "Jag försökte rita men det blev inte bra! Vi kan prata om det istället. 😊"
ERROR_UNKNOWN        = "Oj! Något gick snett. Skriv /reset så börjar vi om! 🔄"
MSG_NO_CONSENT       = "Jag behöver din förälders godkännande först! 🔑\nBe en vuxen skriva /consent [lösenord]"
MSG_SESSION_LIMIT    = (
    "Vi har chattat ett bra tag nu! 🌟 Dags för en paus.\n"
    "Gå ut, rör på dig, rita något, eller gör något kul.\n"
    "Jag finns här när du kommer tillbaka om en stund!"
)
MSG_DAY_LIMIT        = "Vi har haft en riktigt bra dag! 🎉 Nu stänger jag för\nidag. Vi ses imorgon! Hej då! 👋"


# ── DEL 3: Samtyckestexter (kopierade ordagrant) ─────────────────────────────
CONSENT_REQUEST_MSG = (
    "Hej! Jag är Skooli Buddy — en studiekompis! 📚\n\n"
    "Innan vi kan börja behöver din förälder eller\n"
    "vårdnadshavare godkänna.\n\n"
    "👨‍👩‍👧 Förälder: Skriv /consent [lösenord]\n\n"
    "Du har fått lösenordet separat."
)

CONSENT_GRANTED_MSG = (
    "✅ Samtycke registrerat.\n\n"
    "Ditt barn kan nu chatta med Skooli Buddy.\n\n"
    "Vad vi sparar:\n"
    "• Anonymiserade konversationsloggar (inget namn, ingen\n"
    "  persondata)\n"
    "• Ett numeriskt ID för att hålla reda på samtalet\n\n"
    "Vad vi INTE sparar:\n"
    "• Barnets namn, telefonnummer eller Telegram-användarnamn\n"
    "• Bilder som barnet skickar (de processas men lagras inte)\n\n"
    "Dina rättigheter:\n"
    "• Se konversationsloggar i föräldrapanelen\n"
    "• Radera ALL data när som helst med /revoke\n"
    "• Pausa boten med /pause\n\n"
    "Skriv /start för att låta barnet börja!"
)

CONSENT_REVOKED_MSG = (
    "Samtycke återkallat. All data raderad. ✅\n"
    "Skooli Buddy svarar inte längre i denna chatt.\n"
    "Skriv /consent [lösenord] om du vill börja om."
)

WELCOME_MSG = (
    "Hej! Jag är Skooli Buddy — din studiekompis! 🎒\n\n"
    "Jag hjälper dig att tänka och lära dig saker — fast inte genom att ge dig svaren. "
    "Tillsammans utforskar vi! Vad vill du lära dig idag?"
)

HELP_MSG = (
    "*Kommandon:*\n"
    "/start — Starta Skooli Buddy\n"
    "/reset — Börja om konversationen\n"
    "/help — Visa den här hjälptexten\n"
    "/revoke — Återkalla samtycke och radera data *(förälder)*\n"
    "/consent [lösenord] — Ge samtycke *(förälder)*"
)


def _get_today_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")


def _check_and_increment(chat_id: int) -> str | None:
    """
    Kontrollerar sessionsgränser och ökar räknare.
    Returnerar felmeddelande (DEL 2/DEL 7) om gräns nådd, annars None.
    """
    now = datetime.now(tz=timezone.utc)

    # Pågående paus?
    if chat_id in _pause_until:
        remaining = _pause_until[chat_id] - now
        if remaining.total_seconds() > 0:
            minutes_left = max(1, int(remaining.total_seconds() / 60) + 1)
            return f"Jag tar en liten paus just nu! 😊 Vi kan chatta igen om\n{minutes_left} minuter."
        else:
            del _pause_until[chat_id]
            _session_counts[chat_id] = 0

    # Dag-räknare
    today = _get_today_utc()
    day_entry = _day_counts.get(chat_id, {"count": 0, "date": today})
    if day_entry["date"] != today:
        day_entry = {"count": 0, "date": today}
    if day_entry["count"] >= DAY_MSG_LIMIT:
        return MSG_DAY_LIMIT

    # Öka räknare
    day_entry["count"] += 1
    _day_counts[chat_id] = day_entry
    session_count = _session_counts.get(chat_id, 0) + 1
    _session_counts[chat_id] = session_count

    # Nådd sessionsgränsen?
    if session_count >= SESSION_MSG_LIMIT:
        _pause_until[chat_id] = now + timedelta(minutes=PAUSE_MINUTES)
        _session_counts[chat_id] = 0
        return MSG_SESSION_LIMIT

    return None


def _next_turn(chat_id: int) -> int:
    n = _turn_counts.get(chat_id, 0) + 1
    _turn_counts[chat_id] = n
    return n


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hanterar /start."""
    chat_id = update.effective_chat.id
    if not has_consent(chat_id):
        await update.message.reply_text(CONSENT_REQUEST_MSG)
        return
    await update.message.reply_text(WELCOME_MSG)


async def cmd_consent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hanterar /consent [lösenord] — registrerar förälders samtycke."""
    chat_id = update.effective_chat.id
    guardian_passphrase = os.getenv("GUARDIAN_PASSPHRASE", "")

    if not guardian_passphrase:
        await update.message.reply_text(ERROR_UNKNOWN)
        return

    args = context.args or []
    if not args or args[0] != guardian_passphrase:
        await update.message.reply_text("❌ Fel lösenord. Försök igen med /consent [lösenord]")
        return

    record_consent(chat_id)
    await update.message.reply_text(CONSENT_GRANTED_MSG)


async def cmd_revoke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hanterar /revoke — återkallar samtycke och raderar ALL data (DEL 3)."""
    chat_id = update.effective_chat.id
    revoke_consent(chat_id)
    reset_chat(chat_id)
    delete_logs_for_chat(chat_id)
    _session_counts.pop(chat_id, None)
    _pause_until.pop(chat_id, None)
    _day_counts.pop(chat_id, None)
    _turn_counts.pop(chat_id, None)
    await update.message.reply_text(CONSENT_REVOKED_MSG)


async def cmd_reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hanterar /reset — rensar konversationshistorik och sessionsräknare."""
    chat_id = update.effective_chat.id
    if not has_consent(chat_id):
        await update.message.reply_text(MSG_NO_CONSENT)
        return
    reset_chat(chat_id)
    _session_counts.pop(chat_id, None)
    _pause_until.pop(chat_id, None)
    await update.message.reply_text("🔄 Ny konversation! Vad vill du utforska idag?")


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hanterar /help."""
    await update.message.reply_text(HELP_MSG, parse_mode="Markdown")


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """DEL 8: Röstmeddelanden stöds inte."""
    await update.message.reply_text(
        "Jag kan bara läsa text och bilder just nu! Skriv det\nistället, så hjälper jag dig. 😊"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hanterar vanliga textmeddelanden."""
    chat_id = update.effective_chat.id
    user_text = update.message.text or ""

    if not has_consent(chat_id):
        await update.message.reply_text(MSG_NO_CONSENT)
        return

    # Kontrollera session- och daggränser (DEL 2)
    limit_msg = _check_and_increment(chat_id)
    if limit_msg:
        await update.message.reply_text(limit_msg)
        return

    turn = _next_turn(chat_id)
    session_msgs = _session_counts.get(chat_id, 0)

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    bot_reply = get_response(chat_id, user_text)

    # Logga enligt DEL 5-format
    log_turn(
        chat_id=chat_id,
        user_msg=user_text,
        bot_reply=bot_reply,
        turn=turn,
        session_messages=session_msgs,
    )

    if len(bot_reply) <= 4096:
        await update.message.reply_text(bot_reply)
    else:
        for i in range(0, len(bot_reply), 4096):
            await update.message.reply_text(bot_reply[i : i + 4096])


def main() -> None:
    """Startar Telegram-boten."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Fel: TELEGRAM_BOT_TOKEN saknas i .env", file=sys.stderr)
        sys.exit(1)

    app = Application.builder().token(token).build()

    allowed = filters.Chat(ALLOWED_CHAT_ID)
    app.add_handler(CommandHandler("start", cmd_start, filters=allowed))
    app.add_handler(CommandHandler("consent", cmd_consent, filters=allowed))
    app.add_handler(CommandHandler("revoke", cmd_revoke, filters=allowed))
    app.add_handler(CommandHandler("reset", cmd_reset, filters=allowed))
    app.add_handler(CommandHandler("help", cmd_help, filters=allowed))
    app.add_handler(MessageHandler(allowed & filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(allowed & filters.TEXT & ~filters.COMMAND, handle_message))

    print("Skooli Buddy startar... tryck Ctrl+C för att stoppa.")
    app.run_polling()


if __name__ == "__main__":
    main()
