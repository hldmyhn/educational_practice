from aiogram import Bot
from aiogram.types import BotCommand


async def bot_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="♻️ Перезапустить бота"),
        BotCommand(command="search", description="Спарсить вакансии"),
    ]

    await bot.set_my_commands(commands)

__all__ = ["bot_commands",]
