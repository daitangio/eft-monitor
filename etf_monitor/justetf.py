import requests
from stockdex import Ticker


# Cache
from functools import lru_cache

def loadIsin(isin: str):
    """ Very simple function to load the isin from justetf, we use a json API
    It can change, so be careful
    """
    response = requests.get(
        f"https://www.justetf.com/api/etfs/{isin}/quote",
        params={"locale": "en", "currency": "EUR", "isin": isin},
    )
    return response

@lru_cache(maxsize=64)
def get_info(input_isin: str):
    etf = Ticker(isin=input_isin, security_type="etf")
    return etf.justetf_description

def get_quote(isin: str):
    data = loadIsin(isin)
    return float(data.json()["latestQuote"]["localized"])
