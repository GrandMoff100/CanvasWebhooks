import contextlib
import time

import discord
import json
import os
from threading import Thread
import asyncio
from database import MessageDatabase

client = discord.Client()
database = MessageDatabase()


@client.event
async def on_ready():
    print('Webhooks started and bot is starting.')

@client.event
async def on_message(message):
    if message.channel.name == 'rules':
        await client.delete_message(message)
    if message.content == '!accept' and message.channel.name == 'rules':
        await client.add_roles(message.author, 'Member')
    if message.channel != 'rules':
        database.add_message(message, time.time())
        print(message.content)
    if message.content == '!delete-all':
        for m in database.discord_messages:
            if input("%s?" % m).startswith("y"):
                with contextlib.suppress(ValueError):
                    database.del_message(message_id=message.id)
                    await client.delete_message(m)


client.run(os.environ.get("token"))