import uuid
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from src.core.models import VacancyStatus
from src.modules.companies.schemas import CompanySchema, AddCompanySchema
from src.modules.ai.schemas import AnalyseSchema


class AddVacancySchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(..., min_length=1, max_length=255)
    salary: Optional[int] = None
    status: VacancyStatus = VacancyStatus.APPLIED
    company_id: Optional[uuid.UUID] = None
    new_company: Optional["AddCompanySchema"] = None


class UpdateVacancySchema(AddVacancySchema):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    salary: Optional[int] = None
    status: Optional[VacancyStatus] = None

    model_config = ConfigDict(from_attributes=True)


class VacancySchema(BaseModel):
    title: str
    description: str
    salary: Optional[int] = None
    status: VacancyStatus
    company: Optional["CompanySchema"]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VacancyListSchema(VacancySchema):
    analyses_count: int = 0


class VacancyDetailSchema(VacancySchema):
    analysis: list["AnalyseSchema"] = []


class VacancyResponseSchema(BaseModel):
    items: list["VacancyListSchema"]
    total: int
    page: int
    size: int
