from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import tasks
import asyncio
import csv
from datetime import datetime,timedelta
import logging

# files from env
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
AIRIO: Final[str] = os.getenv('AIRIO_FOLDER')
CHANNEL: Final[str] = os.getenv('CHANNEL_ID')

# setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)
logger=logging.getLogger(__name__)
logging.basicConfig(filename='log.txt', level=logging.NOTSET,format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

# on start
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')
    logger.info(f'{client.user} is now running!')
    bans_hourly.start()

# ban list check task
@tasks.loop(hours = 1)
async def bans_hourly() -> None:
    logger.info('Hourly bans called')
    channel = client.get_channel(int(CHANNEL))
    last_hour_date_time = datetime.now() - timedelta(hours = 1)
    with open(str(AIRIO)+'/Airio.ban.txt',newline='') as csvfile:
        reader = csv.reader(csvfile,delimiter='	')
        for row in reader:
            if datetime.strptime(row[3],'%Y-%m-%d %H:%M:%S')>last_hour_date_time:
                if row[4]=="0":
                    row[4]="half"
                if row[5]=="":
                    row[5]="unspecified"
                msgStr = f"{row[3]}: User `{row[0]}` recieved a {row[4]} day ban for reason \"{row[5]}\". Responsible limad `{row[2]}`."
                await channel.send(msgStr)

# main
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()