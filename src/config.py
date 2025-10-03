import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN не установлен в .env")
    if not chat_id:
        raise ValueError("TELEGRAM_CHAT_ID не установлен в .env")

    return {
        "TELEGRAM_BOT_TOKEN": token.strip(),
        "TELEGRAM_CHAT_ID": chat_id.strip(),
    }
