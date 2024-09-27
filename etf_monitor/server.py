from typing import List
import logging,datetime

from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd


import requests

from .justetf import get_quote,get_info

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# First implementation just have an in memory list of isin with app (average purchase price= prezzo medio di carico)
RUN_LIST = {
    "IE00B4K48X80":{
        "alertup": 80,
        "alertdown": 78,
        "app": 78.402857,
        "qty": 7
    },
    "IE00B579F325":None,
    "DE000A1EK0G3":None,
    "IE00B5M1WJ87":None,
    "IE00B6YX5D40":None,
    "IE00B4L5Y983":None,
    "IE00B8GKDB10":{
        "alertup": 64,
        "alertdown": 60,
        "app": 0,
        "qty": 0
    },
}


class Etf(BaseModel):
    isin: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "isin": "IE00B4K48X80",
                }
            ]
        }
    }


# See https://fastapi.tiangolo.com/advanced/settings/#run-the-server
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    etf_env: str = "prod"
    db_url: str
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
app = FastAPI()


@app.get("/")
async def root():
    """
    Etf Monitor
    Wellcome!
    Etf monitor is able to monitor ETF using JustETF api, and
    """
    return {"version": "etf_monitor-1.0.0", "env": settings.etf_env}


@app.get("/cron/scan")
async def scan_price():
    """
    For every element in the runlist, scan and return current price in EUR
    """
    global RUN_LIST
    quote_list = []
    isin_list = []
    isin_info=[]
    date_list = []
    for isin in RUN_LIST.keys():
        quote = get_quote(isin)
        isin_list.append(isin)
        quote_list.append(quote)
        isin_info.append(get_info(isin))
        date_list.append(datetime.datetime.now().isoformat())
        if RUN_LIST[isin]!=None:
            log.info(f"Processing {isin} {isin_info}")
            alert_limit=RUN_LIST[isin]["alertup"]
            if quote > alert_limit:
                log.info(f"Reached alert limit {alert_limit} by {isin} {quote} ")
            alert_limit_below=RUN_LIST[isin]["alertdown"]
            if quote < alert_limit_below:
                log.info(f"Reached LOWER alert limit {alert_limit_below} by {isin} {quote} ")
    df = pd.DataFrame({"isin": isin_list, "price": quote_list, "date": date_list})
    df.to_csv("./data/etf_monitor.csv", mode='a', header=False, index=False)
    return df


@app.post("/add/")
async def add_etf(item: Etf):
    """Search for Etf data.
    Try with IE00B4K48X80


    """
    # First of all make a direct access to just ETF with
    # https://www.justetf.com/api/etfs/IE00B4K48X80/quote?locale=en&currency=EUR&isin=IE00B4K48X80

    return item
