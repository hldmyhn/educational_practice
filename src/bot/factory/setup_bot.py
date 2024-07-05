from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import LinkPreviewOptions

from bot.data import load_config


def setup_bot(config: load_config()) -> Bot:
    bot: Bot = Bot(
        token=config.TOKEN,
        default=DefaultBotProperties(
            link_preview=LinkPreviewOptions(
                is_disabled=True,
            ),
            parse_mode=ParseMode.HTML,
        ),
    )
    return bot


__all__ = ["setup_bot",]
