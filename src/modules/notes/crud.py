import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from src.core.models import *
from src.modules.notes.schemas import AddNoteSchema
from src.exceptions import ItemNotFoundException, ForbiddenException


async def create_note(
    vacancy_id: uuid.UUID, note_data: AddNoteSchema, user: User, db: AsyncSession
):
    vacancy = await db.get(Vacancy, vacancy_id)
    if not vacancy:
        raise ItemNotFoundException("Вакансия не найдена")
    if vacancy.user_id != user.id:
        raise ForbiddenException("У вас нет прав на создание заметок к этой вакансии")
    new_note = Note(**note_data.model_dump(), vacancy_id=vacancy_id)
    db.add(new_note)
    try:
        await db.commit()
        await db.refresh(new_note)
        return new_note
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


async def get_vacancy_notes(vacancy_id: uuid.UUID, user: User, db: AsyncSession):
    vacancy = await db.get(Vacancy, vacancy_id)
    if not vacancy:
        raise ItemNotFoundException("Вакансия не найдена")
    if vacancy.user_id != user.id:
        raise ForbiddenException("У вас нет прав на просмотр заметок к этой вакансии")
    query = (
        select(Note)
        .where(Note.vacancy_id == vacancy_id)
        .order_by(Note.created_at.desc())
    )
    try:
        result = await db.execute(query)
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise e
