import uuid
from typing import Annotated, Optional
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.models import VacancyStatus
from src.core.database import get_db


class Pagination:
    def __init__(
        self,
        page: int = Query(default=1, ge=1),
        size: int = Query(default=5, ge=1, le=100),
    ):
        self.page = page
        self.size = size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size


class BaseSort:
    def __init__(self, sort_by: str, order: str):
        self.sort_by = sort_by
        self.order = order

    def apply(self, model):
        if self.sort_by:
            sort_column = getattr(model, self.sort_by, model.created_at)
            return sort_column.desc() if self.order == "desc" else sort_column.asc()


SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[Pagination, Depends(Pagination)]
