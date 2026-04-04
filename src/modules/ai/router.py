from fastapi import APIRouter
import uuid

from src.core.deps import SessionDep
from src.auth.deps import UserDep
from src.modules.ai.schemas import AnalyseSchema
import src.modules.ai.crud as crud


router = APIRouter(prefix="/{vacancy_id}", tags=["AI анализатор"])


@router.post("/analyze", summary="Анализировать вакансию")
async def analyze(
    vacancy_id: uuid.UUID, user: UserDep, db: SessionDep, user_comment: str = None
) -> AnalyseSchema:
    return await crud.analyze_vacancy(vacancy_id, user, db, user_comment)
