from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import uuid

class Note(BaseModel):
    id: Optional[str] = None
    title: str
    content: str

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

notes = {
    uuid.uuid4().hex: {"id": uuid.uuid4().hex, "title": "Maths Homework", "content": "Discuss integration Q1-Q23."},
    uuid.uuid4().hex: {"id": uuid.uuid4().hex, "title": "Lab Quiz", "content": "Test on 3rd Feb."}
}

@app.get("/")
def get_all_notes():
    return list(notes.values())

@app.post("/notes/")
def create_note(note: Note):
    if note.id is None:
        note.id = uuid.uuid4().hex 
    notes[note.id] = note.dict()
    return note

@app.get("/searchnote/", response_model=List[Note])
def get_notes(title: Optional[str] = None):  
    if title:
        filtered_notes = [note for note in notes.values() if title.lower() in note['title'].lower()]
    else:
        filtered_notes = list(notes.values())

    return filtered_notes

@app.delete("/notes/{note_id}")
def delete_note(note_id: str):
    if note_id in notes:
        del notes[note_id]
        return {"message": "Note deleted"}
    return {"error": "Note not found"}



