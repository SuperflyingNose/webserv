import datetime
import json

import fastapi

from model import CountLettersResponse

api_router = fastapi.APIRouter()


ID = 0
def getId():
    global ID
    ID += 1
    return ID - 1
class Note:

    def __init__(self, content):
        self.createdAt = datetime.datetime.now()
        self.updatedAt = self.createdAt
        self.id = getId()
        self.content = content
notes = []
def removeNote(id:int):
    for i in range(notes):
        if(notes[i].id == id):
            notes.pop(i)
def getNoteById(id: int):
    global notes
    for note in notes:
        if(note.id == id):
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

@api_router.post("/post", status_code = 201)
def PostNote(a: str):
    note = Note(a)
    notes.append(note)

@api_router.get("/get", response_model=json)
def GetNote(a: int):
    note = getNoteById(a)
    return json.dumps({'id': str(note.id), 'text': str(note.content)})

@api_router.get("/getInfo", response_model=json)
def GetInfo(a: int):
    note = getNoteById(a)
    return json.dumps({'created_at': str(note.createdAt), 'updated_at': str(note.updatedAt)})

@api_router.get("/GetNotesIds", response_model=json)
def GetIds():
    return json.dumps(getIds())

@api_router.delete("/DeleteNote", status_code = 204)
def DeleteNoteById(id: int):
    removeNote(id)

@api_router.patch("/changeNote", status_code = 201)
def ChangeNote(id: int, Text: str):
    note = getNoteById(id)
    note.content = Text
    note.updatedAt = datetime.datetime.now()

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
