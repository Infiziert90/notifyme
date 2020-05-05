import asyncio
import logging
from dispatcher.register import run_me
from main import send_message


@run_me()
async def run(client, servers):
    for s in servers:
        proc = await asyncio.create_subprocess_shell(
            f"ping {s}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        logging.info(stdout)
        logging.error(stderr)
        try:
            await send_message(client, f"{stdout}\n\n\n{stderr}")
        except Exception as err:
            logging.error(err)
