"""
Skooli Buddy Telegram-bot.
Hanterar GDPR-samtyckesgate, Sokratiska svar och föräldrakommandon.
"""
import os
import sys

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
from .logger import log_turn

load_dotenv()

CONSENT_REQUEST_MSG = (
    "Hej! 👋 Innan vi kan börja behöver en förälder ge sitt samtycke.\n\n"
    "📋 *Föräldrar:* Skriv /consent [lösenord] för att godkänna att ditt barn "
    "använder Skooli Buddy. Lösenordet hittar du i din .env-konfiguration."
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


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hanterar /start — kräver samtycke innan barnet får chatta."""
    chat_id = update.effective_chat.id
    if not has_consent(chat_id):
        await update.message.reply_text(CONSENT_REQUEST_MSG, parse_mode="Markdown")
        return
    await update.message.reply_text(WELCOME_MSG)


async def cmd_consent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hanterar /consent [lösenord] — registrerar förälders samtycke."""
    chat_id = update.effective_chat.id
    guardian_passphrase = os.getenv("GUARDIAN_PASSPHRASE", "")

    if not guardian_passphrase:
        await update.message.reply_text(
            "⚠️ GUARDIAN_PASSPHRASE är inte konfigurerat. Kontakta systemadministratören."
        )
        return

    args = context.args or []
    if not args or args[0] != guardian_passphrase:
        await update.message.reply_text(
            "❌ Fel lösenord. Försök igen med /consent [lösenord]"
        )
        return

    record_consent(chat_id)
    await update.message.reply_text(
        "✅ *Samtycke registrerat!*\n\n"
        "Tack! Skooli Buddy är nu aktiverat för det här chattfönstret.\n\n"
        "📊 *Integritetsinformation:*\n"
        "• Vi sparar bara samtalets innehåll och ett anonymt ID\n"
        "• Inga namn eller personuppgifter lagras\n"
        "• Du kan återkalla samtycket när som helst med /revoke\n\n"
        "Ditt barn kan nu skriva /start för att börja!",
        parse_mode="Markdown",
    )


async def cmd_revoke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hanterar /revoke — återkallar samtycke och raderar data."""
    chat_id = update.effective_chat.id
    revoke_consent(chat_id)
    reset_chat(chat_id)
    await update.message.reply_text(
        "🗑️ Samtycke återkallat och konversationsdata raderad.\n"
        "Skooli Buddy svarar inte längre i det här chattfönstret.\n"
        "Du kan ge samtycke igen när som helst med /consent [lösenord]."
    )


async def cmd_reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hanterar /reset — rensar konversationshistorik."""
    chat_id = update.effective_chat.id
    if not has_consent(chat_id):
        await update.message.reply_text(CONSENT_REQUEST_MSG, parse_mode="Markdown")
        return
    reset_chat(chat_id)
    await update.message.reply_text(
        "🔄 Ny konversation! Vad vill du utforska idag?"
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hanterar /help — visar tillgängliga kommandon."""
    await update.message.reply_text(HELP_MSG, parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hanterar vanliga meddelanden — kräver samtycke, anropar Gemini."""
    chat_id = update.effective_chat.id
    user_text = update.message.text or ""

    if not has_consent(chat_id):
        await update.message.reply_text(CONSENT_REQUEST_MSG, parse_mode="Markdown")
        return

    # Visa typing-indikator medan Gemini tänker
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    bot_reply = get_response(chat_id, user_text)
    log_turn(chat_id, user_text, bot_reply)

    # Splitta om svaret överstiger Telegrams 4096-teckensgräns
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

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("consent", cmd_consent))
    app.add_handler(CommandHandler("revoke", cmd_revoke))
    app.add_handler(CommandHandler("reset", cmd_reset))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Skooli Buddy startar... tryck Ctrl+C för att stoppa.")
    app.run_polling()


if __name__ == "__main__":
    main()
