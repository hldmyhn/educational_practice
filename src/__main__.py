from asyncio import run

from aiogram import Bot, Dispatcher

from bot.data import load_config
from bot.factory import setup_bot, setup_dispatcher
from logger import setup_logging


async def main() -> None:
    config = load_config().bot
    bot: Bot = setup_bot(config=config)
    dp: Dispatcher = setup_dispatcher()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    setup_logging()
    run(main())
