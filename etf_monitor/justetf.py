import requests


def loadIsin(isin: str):
    response = requests.get(
        "https://www.justetf.com/api/etfs/IE00B4K48X80/quote",
        params={"locale": "en", "currency": "EUR", "isin": isin},
    )
    return response


def get_quote(isin: str):
    data = loadIsin(isin)
    return data.json()["latestQuote"]["localized"]
