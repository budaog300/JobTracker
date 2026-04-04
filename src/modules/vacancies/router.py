from fastapi import APIRouter
import uuid
from src.core.deps import SessionDep, PaginationDep
from src.modules.vacancies.deps import VacancySortDep, VacancyFilterDep
from src.auth.deps import UserDep, AdminUserDep
import src.modules.vacancies.crud as crud
from src.modules.vacancies.schemas import (
    AddVacancySchema,
    VacancySchema,
    VacancyListSchema,
    VacancyDetailSchema,
    UpdateVacancySchema,
    VacancyResponseSchema,
)
from src.modules.notes.router import router as router_notes
from src.modules.ai.router import router as router_ai


router = APIRouter(prefix="/api/v1/vacancies", tags=["Вакансии"])
router.include_router(router_notes)
router.include_router(router_ai)


@router.get("/", response_model=VacancyResponseSchema, summary="Все вакансии")
async def get_vacancies(
    user: UserDep,
    db: SessionDep,
    pagination: PaginationDep,
    filter_dep: VacancyFilterDep,
    sort_dep: VacancySortDep,
) -> VacancyResponseSchema:
    return await crud.get_vacancies(user, db, pagination, filter_dep, sort_dep)


@router.get("/{vacancy_id}", summary="Вакансия по id")
async def get_vacancy_by_id(
    vacancy_id: uuid.UUID, user: UserDep, db: SessionDep
) -> VacancyDetailSchema:
    return await crud.get_vacancy_by_id(vacancy_id, user, db)


@router.post("/", summary="Создать вакансию")
async def create_vacancy(
    data: AddVacancySchema, user: UserDep, db: SessionDep
) -> VacancySchema:
    return await crud.create_vacancy(data, user, db)


@router.patch("/{vacancy_id}", summary="Изменить вакансию")
async def update_vacancy(
    vacancy_id: uuid.UUID, data: UpdateVacancySchema, user: UserDep, db: SessionDep
) -> VacancySchema:
    return await crud.update_vacancy(vacancy_id, data, user, db)


@router.delete("/{vacancy_id}", status_code=204, summary="Удалить вакансию")
async def delete_vacancy(vacancy_id: uuid.UUID, user: UserDep, db: SessionDep):
    await crud.delete_vacancy(vacancy_id, user, db)
    return None
