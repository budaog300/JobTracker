from fastapi import APIRouter
import uuid

from src.auth.deps import UserDep, AdminUserDep
from src.core.deps import SessionDep
from src.modules.companies.schemas import (
    AddCompanySchema,
    CompanySchema,
    UpdateCompanySchema,
)
import src.modules.companies.crud as crud


router = APIRouter(prefix="/api/v1/companies", tags=["Компании"])


@router.get("/", summary="Все компании")
async def get_companies(user: UserDep, db: SessionDep) -> list[CompanySchema]:
    return await crud.get_companies(user, db)


@router.get("/{company_id}", summary="Компания по id")
async def get_company_by_id(
    company_id: uuid.UUID, user: UserDep, db: SessionDep
) -> CompanySchema:
    return await crud.get_company_by_id(company_id, user, db)


@router.post("/", summary="Создать компанию")
async def create_company(
    data: AddCompanySchema, user: UserDep, db: SessionDep
) -> CompanySchema:
    return await crud.create_company(data, user.id, db)


@router.patch("/{company_id}", summary="Изменить компанию")
async def update_company(
    company_id: uuid.UUID, data: UpdateCompanySchema, user: UserDep, db: SessionDep
) -> CompanySchema:
    return await crud.update_company(company_id, data, user, db)


@router.delete("/{company_id}", status_code=204, summary="Удалить компанию")
async def delete_company(company_id: uuid.UUID, user: UserDep, db: SessionDep):
    await crud.delete_company(company_id, user, db)
    return None
