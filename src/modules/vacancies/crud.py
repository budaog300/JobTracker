from sqlalchemy import select, insert, update, delete, and_, func, desc, asc
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.orm.exc import ObjectDeletedError
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from src.core.models import *
from src.core.deps import Pagination
from src.modules.vacancies.deps import VacancySort, VacancyFilter
from src.modules.vacancies.schemas import AddVacancySchema, UpdateVacancySchema
from src.exceptions import ItemNotFoundException, ForbiddenException
from src.modules.companies.crud import create_company


async def get_vacancies(
    user: User,
    db: AsyncSession,
    pagination: Pagination = None,
    filter_dep: VacancyFilter = None,
    sort_dep: VacancySort = None,
):
    filters = [Vacancy.user_id == user.id]
    if filter_dep.status:
        filters.append(Vacancy.status == filter_dep.status)
    if filter_dep.company_id:
        filters.append(Vacancy.company_id == filter_dep.company_id)
    count_query = select(func.count(Vacancy.id)).where(*filters)

    analyses_count_subquery = (
        select(func.count(AiAnalysis.id))
        .where(AiAnalysis.vacancy_id == Vacancy.id)
        .scalar_subquery()
        .label("analyses_count")
    )
    query = (
        select(Vacancy, analyses_count_subquery)
        .options(joinedload(Vacancy.company))
        .where(*filters)
    )

    if sort_dep:
        query = query.order_by(sort_dep.apply(Vacancy))

    if pagination:
        query = query.limit(pagination.size).offset(pagination.offset)

    try:
        total_rows = await db.execute(count_query)
        total = total_rows.scalar()
        result = await db.execute(query)
        vacancies = []
        for vacancy_obj, ai_count in result.all():
            vacancy_obj.analyses_count = ai_count
            vacancies.append(vacancy_obj)

        return {
            "items": vacancies,
            "total": total,
            "page": pagination.page if pagination else 1,
            "size": pagination.size if pagination else len(vacancies),
        }
    except SQLAlchemyError as e:
        raise e


async def get_vacancy_by_id(vacancy_id: uuid.UUID, user: User, db: AsyncSession):
    query = (
        select(Vacancy)
        .options(joinedload(Vacancy.company), selectinload(Vacancy.analysis))
        .where(and_(Vacancy.id == vacancy_id, Vacancy.user_id == user.id))
    )
    try:
        result = await db.execute(query)
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise e


async def create_vacancy(vacancy_data: AddVacancySchema, user: User, db: AsyncSession):
    company_id = vacancy_data.company_id
    if vacancy_data.new_company is not None:
        new_company = await create_company(
            vacancy_data.new_company, user.id, db, commit=False
        )
        company_id = new_company.id
    new_vacancy = Vacancy(
        **vacancy_data.model_dump(exclude={"new_company", "company_id"}),
        user_id=user.id,
        company_id=company_id
    )
    db.add(new_vacancy)
    try:
        await db.commit()
        query = select(Vacancy).where(Vacancy.id == new_vacancy.id)
        if new_vacancy.company_id is not None:
            query = query.options(joinedload(Vacancy.company))
        res = await db.execute(query)
        result = res.scalar_one_or_none()
        if not result:
            raise ItemNotFoundException(
                "Вакансия не найдена либо была удалена в момент создания!"
            )
        return result
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


async def update_vacancy(
    vacancy_id: uuid.UUID,
    vacancy_data: UpdateVacancySchema,
    user: User,
    db: AsyncSession,
):
    vacancy = await db.get(Vacancy, vacancy_id)
    if not vacancy:
        raise ItemNotFoundException("Вакансия не найдена!")
    if vacancy.user_id != user.id:
        raise ForbiddenException("У вас нет прав на изменение этой вакансии!")

    vacancy_data_dict = vacancy_data.model_dump(exclude_unset=True)
    if not vacancy_data_dict:
        return vacancy

    for key, value in vacancy_data_dict.items():
        setattr(vacancy, key, value)
    try:
        await db.commit()
        try:
            await db.refresh(vacancy)
        except (ObjectDeletedError, InvalidRequestError):
            raise ItemNotFoundException(
                "Вакансия не найдена либо была удалена в момент изменения!"
            )
        return vacancy
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


async def delete_vacancy(vacancy_id: uuid.UUID, user: User, db: AsyncSession):
    vacancy = await db.get(Vacancy, vacancy_id)
    if not vacancy:
        raise ItemNotFoundException("Вакансия не найдена!")
    if vacancy.user_id != user.id:
        raise ForbiddenException("У вас нет прав на удаление этой вакансии!")
    try:
        await db.delete(vacancy)
        await db.commit()
        return "Deleted"
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
