# GG Taken from https://github.com/ahnazary/stockdex#fundamental-data-from-yahoo-finance-api-fast-queries-through-yahoo-finance-api


from .justetf import get_quote


def loadIsin(isin: str):
    response = requests.get(
        "https://www.justetf.com/api/etfs/IE00B4K48X80/quote",
        params={"locale": "en", "currency": "EUR", "isin": isin},
    )
    return response.json()


print(get_quote("IE00B4K48X80"))
exit()


from stockdex import Ticker

etf = Ticker(isin="IE00B4K48X80", security_type="etf")

etf_general_info = etf.justetf_general_info
print(etf_general_info.to_json())
# print(repr(etf_general_info))
print("WKN")
# print(etf.justetf_wkn)
print("DESCR")
# print( etf.justetf_description)
print("Basics")

# Basic data about the ETF
etf_basics = etf.justetf_basics

print(etf_basics.to_json())


# # Holdings of the ETF by company, country and sector
# etf_holdings_companies = etf.justetf_holdings_companies
# etf_holdings_countries = etf.justetf_holdings_countries
# etf_holdings_sectors = etf.justetf_holdings_sectors
