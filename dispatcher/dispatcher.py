import asyncio
from typing import Callable, NamedTuple


class Command(NamedTuple):
    func: Callable

commands = []


def register(func: Callable):
    commands.append(Command(func))


def get_set(client, servers, loop):
    return {loop.create_task(x.func(client, servers)) for x in commands}