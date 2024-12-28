from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import tasks
import asyncio
import csv
from datetime import datetime,timedelta
import logging
from commands import command_resolve

# files from env
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
AIRIO: Final[str] = os.getenv('AIRIO_FOLDER')
CHANNEL: Final[str] = os.getenv('BAN_CHANNEL_ID')
ELV_CHANNEL: Final[str] = os.getenv('ADMIN_CHANNEL_NAME')

# setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)
logger=logging.getLogger(__name__)
logging.basicConfig(filename='log.txt', level=logging.NOTSET,format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

# messages
async def send_message(message: Message, user_message: str, user: str, channel: str) -> None:
    if not user_message:
        logger.info('(Message was empty because intents were not enabled probably)')
        return

    try:
        response: str = command_resolve(user_message,user,channel,ELV_CHANNEL)
        logger.info(f'Command ran {user_message,user,channel,ELV_CHANNEL}')
        await message.channel.send(response)
    except Exception as e:
        logger.info(e)

# on start
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')
    logger.info(f'{client.user} is now running!')
    bans_hourly.start()

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    if(message.content.startswith('!')):
        await send_message(message, user_message, username, channel)

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