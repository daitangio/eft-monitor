from typing import List
import logging,datetime
import telegram

from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd


import requests

from .justetf import get_quote,get_info

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# First implementation just have an in memory list of isin with app (average purchase price= prezzo medio di carico) and two ather alerts limits.
# Below a sample
RUN_LIST = {
    "IE00B4K48X80":{
        "alertup": 85,
        "alertdown": 79,
        "app": 78.402857,
        "qty": 7,
        "desc": "MSCI Europe leading stocks industrial countries"
    },
    "IE00B579F325":None,
    "DE000A1EK0G3":None,
    "IE00B5M1WJ87":None,
    "IE00B6YX5D40":None,
    "IE00B4L5Y983":None,
    "IE00B8GKDB10":{
        "alertup": 65,
        "alertdown": 64,
        "app": 0,
        "qty": 0,
        "desc":"FTSE All-World High Dividend Yield index"
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
    telegram_token_api: str
    telegram_chat_id: str
    model_config = SettingsConfigDict(env_file="etf_monitor.env")


settings = Settings()
app = FastAPI()

async def etf_notify(msg:str):
    bot = telegram.Bot(token=settings.telegram_token_api)
    await bot.send_message(chat_id=settings.telegram_chat_id, text=msg)




@app.get("/")
async def root():
    """
    Etf Monitor
    Wellcome!
    Etf monitor is able to monitor ETF using JustETF api, and
    """
    await etf_notify("Etf_monitor ready to report")
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
        #isin_info.append(get_info(isin))
        current_date=datetime.datetime.now().isoformat()
        date_list.append(current_date)        
        if RUN_LIST[isin]!=None:
            current_etf=RUN_LIST[isin]
            log.info(f"Processing {isin}")
            alert_limit=current_etf["alertup"]
            desc=current_etf.get("desc","")
            if quote > alert_limit:                
                msg=f"{isin} +Reached alert limit {alert_limit} >> {quote} {desc}"
                log.info(msg)
                await etf_notify(msg)
            alert_limit_below=current_etf["alertdown"]
            if quote < alert_limit_below:
                msg=f"{isin} -Reached alert limit {alert_limit_below} >> {quote} {desc}"
                log.info(msg)
                await etf_notify(msg)
        dfIsin=pd.DataFrame({"date": [current_date],   "price": [quote]})
        dfIsin.to_csv(f"./data/{isin}_etf_monitor.csv", mode='a', header=False, index=False)    
    df = pd.DataFrame({"isin": isin_list, "date": date_list, "price": quote_list} )
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
