from typing import Optional, List


class VacancyRepository:
    def __init__(self, pool):
        self._pool = pool

    async def _execute_query(self, query, params=None) -> List[dict]:
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)
                results = await cursor.fetchall()
                vacancies = []
                for row in results:
                    vacancy = {
                        "id": row[0],
                        "name": row[1],
                        "employment": row[2],
                        "requirement": row[3],
                        "experience": row[4]
                    }
                    vacancies.append(vacancy)
                return vacancies

    async def add_vacancy(self, vacancy_data: dict) -> Optional[dict]:
        query = """
        INSERT INTO vacancy (id, name, employment, requirement, experience)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            employment = VALUES(employment),
            requirement = VALUES(requirement),
            experience = VALUES(experience)
        """
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (
                    vacancy_data["id"],
                    vacancy_data["name"],
                    vacancy_data["employment"],
                    vacancy_data["requirement"],
                    vacancy_data["experience"]
                ))
                await conn.commit()
        return vacancy_data

    async def find_by_title(self, name: str) -> List[dict]:
        query = "SELECT * FROM vacancy WHERE name LIKE %s OR requirement LIKE %s"
        param = f"%{name}%"
        return await self._execute_query(query, (param, param))

    async def find_by_skills(self, skills: List[str]) -> List[dict]:
        placeholders = ', '.join(['%s'] * len(skills))
        query = f"SELECT * FROM vacancy WHERE requirement LIKE ANY (ARRAY[{placeholders}])"
        params = tuple(skills)
        return await self._execute_query(query, params)

    async def find_by_employment(self, employment: str) -> List[dict]:
        query = "SELECT * FROM vacancy WHERE employment = %s"
        return await self._execute_query(query, (employment,))
