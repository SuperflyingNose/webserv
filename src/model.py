from typing import Dict

from pydantic import BaseModel
from datetime import datetime


# Класс, который описывает структуру ответа сервера для метода,
# который подсчитывает символы в строке.
# Данный класс обязательно должен быть наследован от pydantic.BaseModel!
class CountLettersResponse(BaseModel):
    counted_at: datetime
    counters: Dict[str, int]

class NoteCreationResponse(BaseModel):
    id: int

class ReadNoteResponce(BaseModel):
    id: int
    text: str

class GetNoteInfoResponse(BaseModel):
    created_at: datetime
    updated_at: datetime

class UpdateNoteResponse(BaseModel):
    id: int
    old_text: str
    new_text: str

class ShowNotesResponse(BaseModel):
    note_list: Dict[int, int]
