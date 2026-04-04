import uuid
from src.core.models import VacancyStatus
from fastapi import Query, Depends
from typing import Optional, Annotated

from src.core.deps import BaseSort


class VacancyFilter:
    def __init__(
        self,
        status: Optional[VacancyStatus] = Query(None),
        company_id: Optional[uuid.UUID] = Query(None),
    ):
        self.status = status
        self.company_id = company_id


class VacancySort(BaseSort):
    def __init__(
        self,
        sort_by: Optional[str] = Query(default="created_at"),
        order: Optional[str] = Query(default="asc"),
    ):
        super().__init__(sort_by, order)


VacancyFilterDep = Annotated[VacancyFilter, Depends(VacancyFilter)]
VacancySortDep = Annotated[VacancySort, Depends(VacancySort)]
