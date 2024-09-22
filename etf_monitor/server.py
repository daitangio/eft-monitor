from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd
# Cache
from functools import lru_cache

import requests

from .justetf import get_quote

# First implementation just have an in memory list of isin with app (average purchase price= prezzo medio di carico)
RUN_LIST={
"IE00B4K48X80",
"IE00B579F325",
"DE000A1EK0G3",
"IE00B5M1WJ87",
"IE00B6YX5D40",
"IE00B4L5Y983",
"IE00B8GKDB10",
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
    db_url: str = "sqlite://:memory:"
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
    return {
        "version": "etf_monitor-1.0.0",
        "env": settings.etf_env
        }


@app.get("/cron/scan")
async def scan_price():
    """
    For every element in the runlist, scan and return current price in EUR
    """
    global RUN_LIST
    quote_list=[]
    isin_list=[]
    for isin in RUN_LIST:
        quote=get_quote(isin)
        isin_list.append(isin)
        quote_list.append(quote)
    df = pd.DataFrame({
        "isin":isin_list, 
        "price":quote_list})
    return df.to_json()

@app.post("/add/")
async def add_etf(item: Etf):
    """Search for Etf data.
    Try with IE00B4K48X80


    """
    # First of all make a direct access to just ETF with
    # https://www.justetf.com/api/etfs/IE00B4K48X80/quote?locale=en&currency=EUR&isin=IE00B4K48X80
    
    return item