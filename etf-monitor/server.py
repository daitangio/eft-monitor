from fastapi import FastAPI
from pydantic import BaseModel
import requests

from .justetf import *

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

app = FastAPI()

@app.get("/")
async def root():
    """
    Etf Monitor
    Wellcome!
    Etf monitor is able to monitor ETF using JustETF api, and
    """
    return {"version": "etf-monitor-1.0.0"}

@app.post("/add/")
async def add_etf(item: Etf):
    """Search for Etf data.
    Try with IE00B4K48X80


    """
    # First of all make a direct access to just ETF with
    # https://www.justetf.com/api/etfs/IE00B4K48X80/quote?locale=en&currency=EUR&isin=IE00B4K48X80
    
    return item