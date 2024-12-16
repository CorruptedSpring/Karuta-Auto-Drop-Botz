from time import sleep
import requests

def GetData():
        with open("otherdata.data", "r") as file:
            data = file.readlines()
        return data

def DropKaruta(ChannelID, Token):
    url = f"https://discord.com/api/v9/channels/1284893215467507773/messages"
    headers = {
         Authorization: Token
         
    }
    {"mobile_network_type":"unknown","content":"ok","nonce":"1318296299350523904","tts":false,"flags":0}
    requests = requests.post(url, headers=headers)
         

ChannelID = GetData()[0].strip()
Time = int(GetData()[1].strip())

while True:
    pass