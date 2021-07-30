import os
import discord
import yahoofinance

client = discord.Client()
yf = yahoofinance.YfRequest()

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
        await msg_bahasa_counter(message)


async def msg_bahasa_counter(message):
    username = message.content.split(" ")[1]
    if username not in users.keys():
        users[username] = {}
        users[username][message.author.name] = 1
    else:
        users[username][message.author.name] += 1
    output_msg = (
        f"{username}'s total points :{sum(users[username].values())}. "
        f"{message.author.name} reported {users[username][message.author.name]}"
    )
    await message.channel.send(output_msg)


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
