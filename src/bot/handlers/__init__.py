from aiogram import Dispatcher

from .user import user_router
from ..dialogs import dialog


def setup_routers(dp: Dispatcher) -> None:
    dp.include_routers(user_router, dialog)


__all__ = ["setup_routers",]
