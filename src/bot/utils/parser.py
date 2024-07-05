import re

from aiohttp import ClientSession
from aiomysql import create_pool

from bot.data import load_config
from bot.database.repositories import VacancyRepository

BASE_URL = "https://api.hh.ru/vacancies"
PAGE_LIMIT = 5
config = load_config().mysql


class HHParser:
    def __init__(self):
        self.url = BASE_URL
        self.params = {
            # area - Москва (https://api.hh.ru/areas/1)
            "area": 1,
            # text - это текст для запроса
            "text": "Разработчик",
            # per_page - кол-во вакансий на одной странице
            "per_page": 100,
            # начальная страница, далее идем до 5 и получаем 500 вакансий
            "page": 0
        }
        self.page_limit = PAGE_LIMIT

    async def _fetch_data(self, session: ClientSession, params: dict) -> dict:
        async with session.get(self.url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return {}

    async def _parse_vacancies(self, session: ClientSession, repo: VacancyRepository) -> None:
        for page in range(self.page_limit):
            self.params["page"] = page
            data = await self._fetch_data(session, self.params)
            if data and "items" in data:
                vacancies = data["items"]
                for vacancy in vacancies:
                    requirement = vacancy.get("snippet", {}).get("requirement", None)

                    if requirement:
                        requirement = re.sub(r"</?highlighttext>", "", requirement)

                    vacancy_data = {
                        "id": vacancy.get("id"),
                        "name": vacancy.get("name"),
                        "employment": vacancy.get("employment", {}).get("name"),
                        "requirement": requirement,
                        "experience": vacancy.get("experience", {}).get("name"),
                    }
                    await repo.add_vacancy(vacancy_data)
            else:
                break

    async def run(self):
        _config = load_config().mysql
        async with ClientSession() as session:
            pool = await create_pool(
                host=_config.HOST,
                port=_config.PORT,
                user=_config.USER,
                password=_config.PASSWORD,
                db=_config.DATABASE,
                autocommit=True
            )
            vacancy_repo = VacancyRepository(pool)
            await self._parse_vacancies(session, vacancy_repo)
