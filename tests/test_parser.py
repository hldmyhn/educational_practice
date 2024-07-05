from unittest.mock import AsyncMock, MagicMock

import pytest
from aiohttp import ClientSession

from bot.database.repositories import VacancyRepository
from bot.utils import HHParser


@pytest.mark.asyncio
async def test_parse_vacancies():
    mock_vacancy = {
        "id": "123",
        "name": "Python Developer",
        "snippet": {"requirement": "<highlighttext>Python skills</highlighttext> required"},
        "employment": {"name": "Full-time"},
        "experience": {"name": "2 years"}
    }
    data = {"items": [mock_vacancy]}

    repo = MagicMock(VacancyRepository)
    repo.add_vacancy = AsyncMock()

    mock_session = AsyncMock(ClientSession)
    mock_session.__aenter__.return_value.get = AsyncMock(return_value=data)

    parser = HHParser()

    await parser._parse_vacancies(mock_session, repo)

    repo.add_vacancy.assert_called_once_with({
        "id": "123",
        "name": "Python Developer",
        "employment": "Full-time",
        "requirement": "Python skills required",
        "experience": "2 years"
    })
