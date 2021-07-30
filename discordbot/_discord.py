import requests
from discordbot import CONFIG

OAUTH2_ENDPOINT = "https://discord.com/api/oauth2/"

data = {
    "client_id": CONFIG.get("client-id"),
    "client_secret": CONFIG.get("client-secret"),
    'grant_type': 'authorization_code',
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}
r = requests.post("https://discord.com/api/oauth2/authorize?client_id=860232740670013491&permissions=2147891264&scope=bot", data=data, headers=headers)
print(r.json())