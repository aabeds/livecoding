import requests
import json
from discordbot import CONFIG

YF_BASE_URL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/"

class YfRequest():
    headers = {
        'x-rapidapi-key': CONFIG.get("rapidapi-key"),
        'x-rapidapi-host': CONFIG.get("rapidapi-host")
    }

    def get_request(self, query_str: str, **kwargs):
        region = kwargs.get("region") or "US"

        url = YF_BASE_URL + "auto-complete"

        querystring = {
            "q": query_str,
            "region": region
        }

        response = requests.request("GET", url, headers=self.headers, params=querystring)

        return response

    def get_symbol_summary(self, symbol: str, **kwargs):
        url = YF_BASE_URL + "stock/v2/get-summary"
        region = kwargs.get("region") or "US"

        querystring = {"symbol": symbol, "region": region}

        response = requests.request("GET", url, headers=self.headers, params=querystring)

        return response

    def get_price(self, symbol ):
        summary = self.get_symbol_summary(symbol)
        summary_json = json.loads(summary.text)

        symbol_price = summary_json.get("price")

        symbol_price_raw = symbol_price.get("regularMarketOpen").get("raw")
        print(symbol_price)
        return symbol_price_raw

if __name__ == '__main__':
    yf = YfRequest()

    result_str = yf.get_request("btc")
    result_json = json.loads(result_str.text)

    quotes = result_json.get("quotes")

    for quote in quotes:
        print(quote)
        print(quote.get("shortname"))
        symbol = quote.get("symbol")

        summary = yf.get_symbol_summary(symbol)
        summary_json = json.loads(summary.text)

        symbol_price = summary_json.get("price")

        symbol_price_raw = symbol_price.get("regularMarketOpen").get("raw")
        print(f"Raw Price: {symbol_price_raw}")

    yf.get_price("BTC")