from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class AddNoteSchema(BaseModel):
    text: str = Field(..., min_length=1, max_length=255)


class UpdateNoteSchema(BaseModel):
    text: str = Field(..., min_length=1, max_length=255)


class NoteSchema(BaseModel):
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
