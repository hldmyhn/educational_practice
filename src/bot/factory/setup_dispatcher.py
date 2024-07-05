from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from bot import setup_commands
from bot.handlers import setup_routers
from bot.middlewares import setup_middlewares


def setup_dispatcher() -> Dispatcher:
    dp: Dispatcher = Dispatcher(
        storage=MemoryStorage(),
    )

    setup_routers(dp)
    setup_commands(dp)
    setup_middlewares(dp)

    setup_dialogs(dp)
    return dp


__all__ = ["setup_dispatcher",]
