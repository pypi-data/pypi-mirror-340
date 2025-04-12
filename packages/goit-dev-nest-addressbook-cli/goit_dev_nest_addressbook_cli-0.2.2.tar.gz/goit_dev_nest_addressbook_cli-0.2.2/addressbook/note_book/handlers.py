from addressbook.note_book.note_book import NoteBook, Note
from addressbook.error_handler import input_error, EmailValidationError, EmailIsNotFound

@input_error
def add_note(args, notebook):
    if not args:
        return "Please provide the note title and text."
    title = args[0]
    text = " ".join(args[1:])
    if not text:
        return "Note text is required."
    note = Note(title, text)
    notebook.add_note(note)
    return "Note added."


@input_error
def edit_note(args, notebook):
    if len(args) < 2:
        return "Usage: edit-note [title] [new text]"
    title = args[0]
    new_text = " ".join(args[1:])
    notebook.change_note(title, new_text)
    return f"Note '{title}' updated."


@input_error
def delete_note(args, notebook):
    if not args:
        return "Usage: delete-note [title]"
    title = args[0]
    notebook.delete_note(title)
    return f"Note '{title}' deleted."


@input_error
def search_note(args, notebook):
    if not args:
        return "Please provide a title."
    title = args[0]
    result = notebook.find_note_by_title(title)
    if not result:
        return "No notes found."
    return result

@input_error
def find_note_by_tag(args, notebook):
    if not args:
        return "Please provide a tag to search."
    tag = args[0]
    results = notebook.find_notes_by_tag(tag)
    if not results:
        return f"No notes with tag '{tag}' found."
    return "\n".join(str(note) for note in results)

def list_notes(args, notebook):
    if not notebook.notes:
        return "No notes available."
    return "\n".join(f"{i}: {note}" for i, note in enumerate(notebook.notes))

@input_error
def add_tag(args, notebook):
    if len(args) < 2:
        return "Usage: add-tag [note_title] [tag]"
    title = args[0]
    tag_value = args[1]
    return notebook.add_tag_to_note(title, tag_value)

@input_error
def remove_tag(args, notebook):
    if len(args) < 2:
        return "Usage: remove-tag [note_title] [tag]"
    title = args[0]
    tag_value = args[1]
    return notebook.remove_tag_from_note(title, tag_value)