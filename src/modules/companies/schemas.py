from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class CompanySchema(BaseModel):
    name: str
    website: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AddCompanySchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    website: Optional[str] = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(..., min_length=1, max_length=255)


class UpdateCompanySchema(BaseModel):
    name: str = Field(None, min_length=1, max_length=255)
    website: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1, max_length=255)

    model_config = ConfigDict(from_attributes=True)
