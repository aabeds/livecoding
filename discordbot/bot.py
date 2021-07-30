import json
import os
import discord
import requests

YF_BASE_URL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/"
RAPIDAPI_KEY = ""
RAPIDAPI_HOST = ""


class YfRequest:
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
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

    def get_price(self, symbol):
        summary = self.get_symbol_summary(symbol)
        summary_json = json.loads(summary.text)

        symbol_price = summary_json.get("price")

        symbol_price_raw = symbol_price.get("regularMarketOpen").get("raw")
        print(symbol_price)
        return symbol_price_raw


client = discord.Client()
yf = YfRequest()

users = {}


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    print("Message read:", message.content)
    if message.author == client.user:
        return

    message_content: str = message.content
    if message_content.startswith("$price"):
        await msg_price(message)

    elif message_content.startswith("$summary"):
        await msg_price_summary(message)

    elif message_content.startswith("$bahasa"):
        message_content_1 = message.content.split(" ")[1]
        if message_content == "reset":
            await msg_bahasa_reset(message)
        elif message_content_1[0] == "@":
            await msg_bahasa_counter(message)


async def msg_bahasa_counter(message):
    username = message.content.split(" ")[1]
    print(username)
    if username not in users.keys():
        users[username] = {}

    if username == "@aabeds":
        await message.channel.send("Ni T20 :)")

    if message.author.name not in users[username].keys():
        users[username][message.author.name] = 1
    else:
        users[username][message.author.name] += 1

    if users[username][message.author.name]:
        nad_cnt = users[username].get("Nad") or 0

        output_msg = (
            f"{username}'s total points : {sum(users[username].values())}. "
            f"{message.author.name} reported {users[username][message.author.name]} time(s). "
            f"Nad reported {nad_cnt} time(s)"
        )
        await message.channel.send(output_msg)


async def msg_bahasa_reset(message):
    global users
    if message.author.name in ["aabeds", "Majujur", "kimimccaw", "pikliwoah"]:
        users = {}
        await message.channel.send("Resetted counter")
    else:
        await message.channel.send(f"User {message.author.name} doesn't have the permission to reset counter")


async def msg_price_summary(message):
    ticker = message.content.split(" ")[1]
    summary = yf.get_symbol_summary(ticker)
    print("Ticker:", ticker)
    await message.channel.send(f"{ticker} summary: {summary.text[:400]}")


async def msg_price(message):
    ticker = message.content.split(" ")[1]
    price = yf.get_price(ticker)
    print("Ticker:", ticker)
    await message.channel.send(f"{ticker} price: {price}")


if __name__ == '__main__':
    token = os.environ["DISCORD_TOKEN"]
    client.run(token)
