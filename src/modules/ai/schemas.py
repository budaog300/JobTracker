from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class AnalyseInputSchema(BaseModel):
    username: str | None
    skills: str | None
    experience_level: str | None
    desired_salary: int | None
    about: str | None

    title: str | None
    description: str | None
    salary: int | None


class AnalyseSchema(BaseModel):
    score: float
    summary: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
