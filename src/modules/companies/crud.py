import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError
from sqlalchemy.orm.exc import ObjectDeletedError

from src.core.models import *
from src.modules.companies.schemas import AddCompanySchema, UpdateCompanySchema
from src.exceptions import ItemNotFoundException, ForbiddenException


async def get_companies(user: User, db: AsyncSession):
    query = (
        select(Company)
        .options(selectinload(Company.vacancies))
        .where(Vacancy.user_id == user.id)
    )
    try:
        result = await db.execute(query)
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise e


async def get_company_by_id(company_id: uuid.UUID, user: User, db: AsyncSession):
    query = (
        select(Company)
        .options(selectinload(Company.vacancies))
        .where(and_(Company.id == company_id, Company.user_id == user.id))
    )
    try:
        result = await db.execute(query)
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise e


async def create_company(
    company_data: AddCompanySchema,
    user_id: uuid.UUID,
    db: AsyncSession,
    commit: bool = True,
):
    new_company = Company(**company_data.model_dump(), user_id=user_id)
    db.add(new_company)
    try:
        if commit:
            await db.commit()
            await db.refresh(new_company)
        else:
            await db.flush()
        return new_company
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


async def update_company(
    company_id: uuid.UUID,
    company_data: UpdateCompanySchema,
    user: User,
    db: AsyncSession,
):
    company = await db.get(Company, company_id)
    if not company:
        raise ItemNotFoundException("Компания не найдена!")
    if company.user_id != user.id:
        raise ForbiddenException("У вас нет прав на изменение этой компании!")

    company_data_dict = company_data.model_dump(exclude_unset=True)
    if not company_data_dict:
        return company

    for key, value in company_data_dict.items():
        setattr(company, key, value)
    try:
        await db.commit()
        try:
            await db.refresh(company)
        except (ObjectDeletedError, InvalidRequestError):
            raise ItemNotFoundException("Компания была удалена другим пользователем!")
        return company
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


async def delete_company(company_id: uuid.UUID, user: User, db: AsyncSession):
    company = await db.get(Company, company_id)
    if not company:
        raise ItemNotFoundException("Компания не найдена!")
    if company.user_id != user.id:
        raise ForbiddenException("У вас нет прав на удаление этой компании!")
    try:
        await db.delete(company)
        await db.commit()
        return company_id
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
