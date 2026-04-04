from fastapi import APIRouter
import uuid
from src.core.deps import SessionDep
from src.auth.deps import UserDep, AdminUserDep
import src.modules.notes.crud as crud
from src.modules.notes.schemas import AddNoteSchema, NoteSchema


router = APIRouter(prefix="/{vacancy_id}/notes", tags=["Заметки для вакансий"])


@router.post("/", summary="Добавить заметку к вакансии")
async def create_note(
    vacancy_id: uuid.UUID, note_data: AddNoteSchema, user: UserDep, db: SessionDep
) -> NoteSchema:
    return await crud.create_note(vacancy_id, note_data, user, db)


@router.get("/", summary="Заметки у вакансии")
async def get_vacancy_notes(
    vacancy_id: uuid.UUID, user: UserDep, db: SessionDep
) -> list[NoteSchema]:
    return await crud.get_vacancy_notes(vacancy_id, user, db)
