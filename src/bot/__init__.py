from aiogram import Dispatcher

from .commands import bot_commands


def setup_commands(dp: Dispatcher) -> None:
    dp.startup.register(bot_commands)


__all__ = ["setup_commands",]
