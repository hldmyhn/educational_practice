from typing import Callable, Awaitable, Union, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, time_limit: Union[int, float] = 2) -> None:
        self._limit = TTLCache(maxsize=20_000, ttl=time_limit)

    async def __call__(
            self,
            handler: Callable[
                [Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]
            ],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any],
    ) -> Any:
        if event.from_user.id in self._limit:
            return await event.reply("<b>Не спамь, подожди немного!</b>")
        else:
            self._limit[event.from_user.id] = None
        return await handler(event, data)
