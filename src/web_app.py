import datetime
from typing import Dict

import fastapi

from model import CountLettersResponse, ReadNoteResponce, GetNoteInfoResponse, ShowNotesResponse, NoteCreationResponse, \
    UpdateNoteResponse

import os

api_router = fastapi.APIRouter()

notesDir = "Notes/"



class Note:
    content = ''

    def __init__(self, id):
        self.createdAt = datetime.datetime.now()
        self.updatedAt = self.createdAt
        self.id = id
    def ChangeText(self, text):
        content = text

def commitNote(note: Note):
    name = notesDir + str(note.id) + '.txt'
    text_file = open(name, 'w')
    text_file.write(note.content)

notes = []


def removeNote(id: int):
    for i in range(len(notes)):
        if (notes[i].id == id):
            notes.pop(i)
            return


def getNoteById(id: int):
    global notes
    for note in notes:
        if (note.id == id):
            return note
    return -1;


def getIds():
    global notes
    s = []
    for idx, note in enumerate(notes):
        s.append(str(idx) + ": " + str(note.id))
    return s;


# Обрати внимание на @api_router.get <- get - тип HTTP метода!
# Для того, чтобы создать put метод, необходимо написать @api_router.put
# /sum - url относительно сервера, по которму будет доступен метод.
# Обрати внимание на response_model <- описывает схему ответа сервера.
# В данном случае ответ сервера = число
@api_router.get("/sum", response_model=float)
def sum_(a: float, b: float):
    """
    Метод выполняет сложение 2х чисел (integer или float) и возвращает результат
    """
    return a + b


@api_router.post("/post", response_model=NoteCreationResponse)
def PostNote(a: int):
    note = Note(a)
    notes.append(note)

    commitNote(note)

    return NoteCreationResponse(
        id=str(note.id),
    )


@api_router.get("/get", response_model=ReadNoteResponce)
def GetNote(a: int):
    note = getNoteById(a)
    return ReadNoteResponce(
        id=str(note.id),
        text=note.content
    )


@api_router.get("/getInfo", response_model=GetNoteInfoResponse)
def GetInfo(a: int):
    note = getNoteById(a)
    return GetNoteInfoResponse(
        created_at=note.createdAt,
        updated_at=note.updatedAt
    )


@api_router.get("/GetNotesIds", response_model=ShowNotesResponse)
def GetIds():
    d = {}
    for idx, i in enumerate(notes):
        d.update({idx : i.id})
    return ShowNotesResponse(
        note_list=d
    )


@api_router.delete("/DeleteNote", status_code= 204)
def DeleteNoteById(id: int):
    removeNote(id)


@api_router.patch("/changeNote", response_model=UpdateNoteResponse)
def ChangeNote(id: int, Text: str):
    note = getNoteById(id)
    oldText = note.content
    note.content = Text
    note.updatedAt = datetime.datetime.now()
    commitNote(note)
    return UpdateNoteResponse(
        id=str(note.id),
        old_text=oldText,
        new_text=note.content
    )


# Обрати внимание на response_model <- описывает схему ответа сервера
@api_router.get("/count_letters", response_model=CountLettersResponse)
def count_letters(text: str):
    """
    Метод выполняет выполняет подсчет количества букв в тексте и
    возвращает результат в виде словаря, состоящего из пар: буква и кол-во.
    Также этот метод возвращает дату и время по местному часовому поясу,
    когда был произведен подсчет.
    """
    letters_count = {}
    for letter in text:
        if letter in letters_count:
            letters_count[letter] += 1
        else:
            letters_count[letter] = 1
    return CountLettersResponse(
        counted_at=datetime.datetime.now(),
        counters=letters_count
    )
