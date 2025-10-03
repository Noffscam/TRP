import requests

COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=the-open-network&vs_currencies=rub"
)

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "TON-RUB-Price-Bot/1.0 (+https://github.com/your-repo)"
}

def get_ton_price_rub() -> float:
    """
    Возвращает цену TON в RUB как float.
    Бросает исключение при ошибке.
    """
    resp = requests.get(COINGECKO_URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if "the-open-network" not in data or "rub" not in data["the-open-network"]:
        raise ValueError("Данные о TON/RUB не найдены в ответе API")

    return float(data["the-open-network"]["rub"])
