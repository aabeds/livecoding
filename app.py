import os

from discordbot.bot import client

token = os.environ["DISCORD_TOKEN"]
print(token)
client.run(token)