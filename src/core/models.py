from sqlalchemy import text, UUID, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated
import uuid
from enum import Enum

from src.core.database import Default


str_unique = Annotated[str, mapped_column(unique=True, nullable=False, index=True)]


class User(Default):
    __tablename__ = "users"

    username: Mapped[str_unique]
    email: Mapped[str_unique]
    password: Mapped[str] = mapped_column(nullable=False)
    skills: Mapped[str | None]
    experience_level: Mapped[str | None]
    desired_salary: Mapped[int | None]
    about: Mapped[str | None]
    is_admin: Mapped[bool] = mapped_column(
        default=False, server_default=text("false"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        default=True, server_default=text("true"), nullable=False
    )

    vacancies: Mapped[list["Vacancy"]] = relationship("Vacancy", back_populates="user")
    companies: Mapped[list["Company"]] = relationship("Company", back_populates="user")


class Company(Default):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(nullable=False, index=True)
    website: Mapped[str | None]
    description: Mapped[str | None]
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    vacancies: Mapped[list["Vacancy"]] = relationship(
        "Vacancy", back_populates="company"
    )
    user: Mapped["User"] = relationship("User", back_populates="companies")


class VacancyStatus(Enum):
    APPLIED = "applied"
    INTERVIEW = "interview"
    REJECTED = "rejected"
    OFFER = "offer"


class Vacancy(Default):
    __tablename__ = "vacancies"

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None]
    salary: Mapped[int | None]
    status: Mapped[VacancyStatus] = mapped_column(SAEnum(VacancyStatus))
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="SET NULL"),
        nullable=True,
    )

    user: Mapped["User"] = relationship("User", back_populates="vacancies")
    company: Mapped["Company"] = relationship("Company", back_populates="vacancies")
    notes: Mapped[list["Note"]] = relationship("Note", back_populates="vacancy")
    analysis: Mapped[list["AiAnalysis"]] = relationship(
        "AiAnalysis", back_populates="vacancy"
    )


class Note(Default):
    __tablename__ = "notes"

    text: Mapped[str]
    vacancy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("vacancies.id", ondelete="CASCADE"),
        nullable=False,
    )

    vacancy: Mapped["Vacancy"] = relationship("Vacancy", back_populates="notes")


class AiAnalysis(Default):
    __tablename__ = "ai_analysis"

    score: Mapped[float]
    summary: Mapped[str]
    vacancy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("vacancies.id", ondelete="CASCADE"),
        nullable=False,
    )

    vacancy: Mapped["Vacancy"] = relationship("Vacancy", back_populates="analysis")
