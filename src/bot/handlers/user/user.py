from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from bot.dialogs.states import SG

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    text = (
        f"Привет, <b>{message.from_user.first_name}</b>!\n\n"
        "Чтобы начать взаимодействие с ботом напишите /search"
    )
    await message.answer(text)


@router.message(Command("search"))
async def menu_handler(
        message: Message,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(SG.MAIN, mode=StartMode.RESET_STACK)


@router.message(Command("filters"))
async def menu_handler(
        message: Message,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(SG.CHOOSE, mode=StartMode.RESET_STACK)
