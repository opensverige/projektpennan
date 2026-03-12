"""
Föräldra-dashboard för Skooli Buddy.
Lösenordsskyddad Streamlit-app som visar anonymiserade konversationsloggar.
Kör: streamlit run dashboard/app.py
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

LOGS_DIR = Path(__file__).parent.parent / "logs"
GUARDIAN_PASSPHRASE = os.getenv("GUARDIAN_PASSPHRASE", "")


def load_logs() -> list[dict]:
    """Laddar alla JSONL-loggfiler från logs/."""
    entries = []
    for log_file in sorted(LOGS_DIR.glob("*.jsonl")):
        with log_file.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return entries


def check_auth() -> bool:
    """Enkel lösenordsvalidering via session state."""
    if st.session_state.get("authenticated"):
        return True
    return False


def show_login() -> None:
    """Visar inloggningsformuläret."""
    st.title("Skooli Buddy — Föräldradashboard 🏫")
    st.markdown("Ange ditt föräldralösenord för att se konversationsstatistik.")
    password = st.text_input("Lösenord", type="password", key="password_input")
    if st.button("Logga in"):
        if password == GUARDIAN_PASSPHRASE and GUARDIAN_PASSPHRASE:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Fel lösenord.")


def show_dashboard(entries: list[dict]) -> None:
    """Visar dashboarden med statistik och konversationer."""
    st.title("Skooli Buddy — Föräldradashboard 🏫")

    if st.button("Logga ut"):
        st.session_state["authenticated"] = False
        st.rerun()

    if not entries:
        st.info("Inga konversationer loggade än. Starta Skooli Buddy och chatta!")
        return

    # Statistik
    dates = set()
    for e in entries:
        try:
            dates.add(e["ts"][:10])
        except (KeyError, TypeError):
            pass

    col1, col2, col3 = st.columns(3)
    col1.metric("Totalt antal meddelanden", len(entries))
    col2.metric("Aktiva dagar", len(dates))
    col3.metric("Snitt per dag", f"{len(entries) / max(len(dates), 1):.1f}")

    st.divider()

    # Senaste 50 turer
    st.subheader("Senaste konversationer")
    recent = entries[-50:][::-1]  # Nyaste först

    for entry in recent:
        ts = entry.get("ts", "")[:19].replace("T", " ")
        with st.expander(f"🕐 {ts} — Chat ID: {entry.get('chat_id', '?')}"):
            st.markdown(f"**Barn:** {entry.get('user', '')}")
            st.markdown(f"**Skooli Buddy:** {entry.get('bot', '')}")


def main() -> None:
    st.set_page_config(
        page_title="Skooli Buddy Dashboard",
        page_icon="🏫",
        layout="wide",
    )

    if not check_auth():
        show_login()
        return

    entries = load_logs()
    show_dashboard(entries)


if __name__ == "__main__":
    main()
