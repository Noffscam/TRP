import time
import logging
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore

from config import load_config
from ton_price import get_ton_price_rub

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

INTERVAL_MINUTES = 4

def send_to_telegram(token: str, chat_id: str, text: str) -> None:
    """
    Отправляет текстовое сообщение в Telegram (Bot API).
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": True,
        "parse_mode": None,  # без форматирования
    }
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()

def job():
    """
    Задача: получить цену TON в RUB и отправить её как единственное сообщение.
    """
    try:
        price_rub = get_ton_price_rub()
        message = f"{price_rub:.2f}₽"
        cfg = load_config()
        send_to_telegram(cfg["TELEGRAM_BOT_TOKEN"], cfg["TELEGRAM_CHAT_ID"], message)
        logging.info(f"Отправлено: {message}")
    except Exception as e:
        logging.error(f"Ошибка при выполнении задачи: {e}")

def main():
    logging.info("Запуск TON RUB Price Bot")
    # Проверим конфиг один раз при старте
    load_config()

    jobstores = {
        'default': MemoryJobStore()
    }
    executors = {
        'default': ThreadPoolExecutor(2)
    }

    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, timezone="UTC")
    scheduler.add_job(job, 'interval', minutes=INTERVAL_MINUTES, next_run_time=None)
    scheduler.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Остановка бота...")
        scheduler.shutdown()

if __name__ == "__main__":
    main()
