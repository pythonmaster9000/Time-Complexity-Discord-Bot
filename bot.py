import discord
from discord.ext import commands
import requests
import random
from typing import Union

intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)


def kru_code(code: str) -> Union[dict, bool]:
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.timecomplexity.ai',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.timecomplexity.ai/?id=e6debedb-efa1-425b-b5b0-d22b54453609',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'x-session-id': f'9c14ca04-a1f4-4fff-81fe-998613a{random.randint(100,999)}92',
    }

    json_data = {
        'inputCode': code,
    }
    response = requests.post('https://www.timecomplexity.ai/api/analyze', headers=headers, json=json_data)
    if response.status_code == 200:
        return response.json()
    return False


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if '```py' in message.content and len(message.content) > 7:
        res = kru_code(message.content.replace('```py', '').replace('```', ''))
        if not res:
            return
        time_complexity, reasoning = res.get('timeComplexity'), res.get('reasoning')
        await message.channel.send(f'{reasoning}')


client.run('YOUR TOKEN HERE')
