# eft-monitor
Monitor etf quotes using JustEtf using only SQLite and python3

This tiny monitor is based on [stockdex](https://github.com/ahnazary/stockdex) for accessing justETF API.

[ ] TODO: The monitor exposes a REST API done with [fastapi](https://fastapi.tiangolo.com) to register ISIN, define monitor delay and so on

# Getting Stared

Install virtualenv using the script provided:

    ./bin/installVirtualEnv

 Then enter in the virtualenv and run the endless server

    fastapi dev etf-monitor/server.py

Look at the documentation here:

http://127.0.0.1:8000/docs  