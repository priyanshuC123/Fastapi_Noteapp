async function createNote() {
    let title = document.getElementById('title').value;
    let content = document.getElementById('content').value;

    await fetch('/notes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: title, content: content })
    });

    document.getElementById('title').value = '';
    document.getElementById('content').value = '';
    loadNotes();
}

async function loadNotes() {
    let response = await fetch('/notes/');
    let notes = await response.json();
    let notesContainer = document.getElementById('notes');
    notesContainer.innerHTML = '';

    notes.forEach(note => {
        let noteDiv = document.createElement('div');
        noteDiv.className = 'note';
        noteDiv.innerHTML = `<strong>${note.title}</strong><p>${note.content}</p><button onclick="deleteNote('${note.id}')">Delete</button>`;
        notesContainer.appendChild(noteDiv);
    });
}

async function deleteNote(noteId) {
    await fetch('/notes/' + noteId, { method: 'DELETE' });
    loadNotes();
}

window.onload = loadNotes;
