#!/usr/bin/python
from discord import Client, NotFound, HTTPException, Forbidden
import os
import json
import asyncio
import logging
import task
from dispatcher import dispatcher
from dotenv import load_dotenv
load_dotenv()

servers = []

loop = asyncio.get_event_loop()
client = Client(loop=loop)
task.load_tasks()


def get_servers():
    with open("servers.json") as stream:
        j = json.load(stream)

    for s in j["servers"]:
        servers.append(s)


async def send_message(c, content):
    for _ in range(3):
        try:
            user = await c.fetch_user(int(os.getenv("TARGET_ID")))
            await user.send(content)
            break
        except (NotFound, HTTPException, Forbidden) as err:
            logging.error(err)


@client.event
async def on_ready():
    _, pending = await asyncio.wait(dispatcher.get_set(client, servers, loop), timeout=180)
    if len(pending) != 0:
        await send_message("Timeout reached! Something did not complete")
    await client.logout()


async def main():
    try:
        await client.start(os.getenv("BOT_TOKEN"))
        await client.close()
    except Exception as err:
        logging.error(err)


if __name__ == '__main__':
    try:
        get_servers()
        loop.run_until_complete(main())
    except Exception as err:
        logging.error(err)
