import requests
import json



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