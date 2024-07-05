from typing import Any, List

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import (
    Dialog,
    Window,
    DialogManager,
)
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import SwitchTo, Button
from aiogram_dialog.widgets.text import Const
from aiomysql import create_pool

from bot.utils import HHParser
from .states import SG
from ..data import load_config
from ..database.repositories import VacancyRepository

MENU = SwitchTo(Const("☰ Меню"), state=SG.MAIN, id="_menu")
config = load_config().mysql
HH_URL = "https://hh.ru/vacancy/"


async def create_db_pool():
    return await create_pool(
        host=config.HOST,
        port=config.PORT,
        user=config.USER,
        password=config.PASSWORD,
        db=config.DATABASE,
        autocommit=True
    )


async def _parse(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
) -> None:
    parser = HHParser()
    await parser.run()
    await manager.switch_to(SG.CHOOSE)


async def send_message(message: Message, vacancies: List[dict]) -> None:
    text = ""
    for vacancy in vacancies:
        text += (
            f"<b>Название:</b> {vacancy['name']}\n"
            f"{HH_URL}{vacancy['id']}\n"
            f"<b>Требования:</b> {vacancy['requirement']}\n"
            f"<b>Занятость:</b> {vacancy['employment']}\n"
            f"<b>Опыт:</b> {vacancy['experience']}\n\n"
        )
        if len(text) > 4096:
            await message.answer(text)
            text = ""

    if text:
        await message.answer(text)


async def query_vacancies_and_send_message(
        message: Message,
        query_function: callable,
        query_param: Any,
        pool: Any,
        manager: DialogManager
) -> None:
    try:
        repo = VacancyRepository(pool)
        vacancies = await query_function(repo, query_param)

        if vacancies:
            await send_message(message, vacancies)
        else:
            text = "<b>По вашему запросу ничего не найдено.</b>"
            await message.answer(text)
    finally:
        pool.close()
        await pool.wait_closed()
        await manager.done()


async def skills_success(
        message: Message,
        widget: Any,
        manager: DialogManager,
        *_,
) -> None:
    query = manager.find("skills").get_value()
    pool = await create_db_pool()
    await query_vacancies_and_send_message(
        message, VacancyRepository.find_by_skills, query, pool, manager
    )


async def job_success(
        message: Message,
        widget: Any,
        manager: DialogManager,
        *_,
) -> None:
    query = manager.find("job_title").get_value()
    pool = await create_db_pool()
    await query_vacancies_and_send_message(
        message, VacancyRepository.find_by_title, query, pool, manager
    )


async def employment_success(
        message: Message,
        widget: Any,
        manager: DialogManager,
        *_,
) -> None:
    query = manager.find("employment").get_value()
    pool = await create_db_pool()
    await query_vacancies_and_send_message(
        message, VacancyRepository.find_by_employment, query, pool, manager
    )


async def data_getter(dialog_manager: DialogManager, **kwargs):
    return {
        "job_title": dialog_manager.find("job_title").get_value(),
        "skills": dialog_manager.find("skills").get_value(),
        "employment": dialog_manager.find("employment").get_value(),
    }


main_window = Window(
    Const("Для парса вакансий нажмите кнопку ниже!"),
    Button(Const("Спарсить"), id="_parse", on_click=_parse),
    state=SG.MAIN,
)

choose_window = Window(
    Const("Данные успешно спаршены\n\n"
          "Выберите вид запроса для парсинга:"),
    SwitchTo(Const("Название должности"), id="_job_title", state=SG.JOB_TITLE),
    SwitchTo(Const("Навыки"), id="_skills", state=SG.SKILLS),
    SwitchTo(Const("Формат работы"), id="_employment", state=SG.EMPLOYMENT),
    state=SG.CHOOSE,
)

job_title_window = Window(
    Const("Введите название должности:\n\n"
          "Например: <code>Программист Python</code>"),
    TextInput(
        id="job_title",
        on_success=job_success,
        type_factory=str,
    ),
    MENU,
    getter=data_getter,
    state=SG.JOB_TITLE,
)

skills_window = Window(
    Const("Введите навыки:"),
    TextInput(
        id="skills",
        on_success=skills_success,
        type_factory=str,
    ),
    MENU,
    getter=data_getter,
    state=SG.SKILLS,
)

employment_window = Window(
    Const("Введите формат работы:\n\n"
          "Например: <code>Удаленная работа</code>"),
    TextInput(
        id="employment",
        on_success=employment_success,
        type_factory=str,
    ),
    MENU,
    getter=data_getter,
    state=SG.EMPLOYMENT,
)

dialog = Dialog(
    main_window,
    choose_window,
    job_title_window,
    skills_window,
    employment_window,
)
