import json
import os
import discord

from pathlib import Path

from discord import Message

from discordbot.yahoofinance import YfRequest
from json_interface import create_new_json_file, read_json_file, write_json_file

client = discord.Client()
yf = YfRequest()

json_path = Path("data.json")

if not os.path.exists(json_path):
    create_new_json_file(json_path)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: Message):
    print("Message read:", message.content)
    print("Author:", message.author.name)
    if message.author == client.user:
        return

    message_content: str = message.content  #
    message_content_arr = message.content.split(" ")
    print("All message contents:", message_content_arr)
    if message_content.startswith("$price"):
        await msg_price(message)

    elif message_content.startswith("$summary"):
        await msg_price_summary(message)

    elif message_content_arr[0] == "$bahasa":
        print("Mentioned Users:", message.mentions)
        print("Mentioned Users (raw):", message.raw_mentions)
        try:
            message_content_1 = message_content_arr[1]
            if message_content_1 == "reset":
                await msg_bahasa_reset(message)
            else:
                await msg_bahasa_counter(message)
        except Exception as e:
            await message.channel.send("Error in command")


async def msg_bahasa_counter(message: Message):
    username = message.content.split(" ")[1]

    users = read_json_file(json_path)
    if username not in users.keys():
        users[username] = {}

    if message.author.name not in users[username].keys():
        print("Author not yet registered in Json")
        users[username][message.author.name] = 1
    else:
        print("Author's counter +1")
        users[username][message.author.name] += 1

    if users[username][message.author.name]:
        nad_cnt = users[username].get("Nad") or 0

        output_msg = (
            f"{username}'s total points : {sum(users[username].values())}. "
            f"{message.author.name} reported {users[username][message.author.name]} time(s). "
            f"CCO Nad reported {nad_cnt} time(s)"
        )
        write_json_file(json_path, users)
        await message.channel.send(output_msg)
    else:
        print("Exception?")


async def msg_bahasa_reset(message: Message):
    if message.author.name.lower() in ["aabeds", "majujur", "kimimccaw", "pikliwoah"]:
        create_new_json_file(json_path)
        await message.channel.send("Kosong-Kosong balik")
    else:
        await message.channel.send(f"Nice try ;) {message.author.name} cuba lagi yer!")


async def msg_price_summary(message: Message):
    ticker = message.content.split(" ")[1]
    summary = yf.get_symbol_summary(ticker)
    print("Ticker:", ticker)
    await message.channel.send(f"{ticker} summary: {summary.text[:400]}")


async def msg_price(message: Message):
    ticker = message.content.split(" ")[1]
    price = yf.get_price(ticker)
    print("Ticker:", ticker)
    await message.channel.send(f"{ticker} price: {price}")


if __name__ == '__main__':
    token = os.environ["DISCORD_TOKEN"]
    client.run(token)
