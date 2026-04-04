import uuid
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.core.models import *
from src.exceptions import ItemNotFoundException, ForbiddenException
from src.modules.ai.service import build_prompt, call_llm
from src.modules.ai.schemas import AnalyseInputSchema


async def analyze_vacancy(
    vacancy_id: uuid.UUID, user: User, db: AsyncSession, user_comment: str = None
):
    vacancy = await db.get(Vacancy, vacancy_id)
    if not vacancy:
        raise ItemNotFoundException("Вакансия не найдена!")
    if vacancy.user_id != user.id:
        raise ForbiddenException("У вас нет прав анализировать эту вакансию!")

    prompt_data = AnalyseInputSchema(
        username=user.username,
        skills=user.skills,
        experience_level=user.experience_level,
        desired_salary=user.desired_salary,
        about=user.about,
        title=vacancy.title,
        description=vacancy.description,
        salary=vacancy.salary,
    )
    prompt = build_prompt(prompt_data, user_comment)
    response = await call_llm(prompt)
    if response:
        response_json = json.loads(response)
        new_analyze = AiAnalysis(**response_json, vacancy_id=vacancy_id)
        db.add(new_analyze)
        try:
            await db.commit()
            await db.refresh(new_analyze)
            return new_analyze
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
