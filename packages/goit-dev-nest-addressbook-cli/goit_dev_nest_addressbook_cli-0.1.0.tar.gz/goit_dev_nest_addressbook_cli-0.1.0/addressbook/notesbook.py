class Title:
    def __init__(self, value):
        if not value:
            raise ValueError("Note title cannot be empty.")
        if len(value) > 100:
            raise ValueError("Note title cannot exceed 100 characters.")
        self.value = value

    def __str__(self):
        return str(self.value)
    

class Content: 
    def __init__(self, value):
        if value is None:
            value = ""
        if len (value) > 500:
            raise ValueError("Note content cannot exceed 500 characters.")
        self.value = value

    def __str__(self):
        return str(self.value)
        

class Note:
    def __init__(self, title, content=None):
        if not title:
            raise ValueError("Title is required")
        self.title = Title(title)
        self.content = Content(content)
    
    def __str__(self):
        title_str = f"Title: {self.title.value}"
        content_str = f"Content: {self.content.value}" if self.content else ""
        return "\n".join(filter(None, [title_str, content_str]))
    

class NotesBook:
    def __init__(self):
        self.notes = []

    def add_note(self, title, content = None):
        if self.find_note_by_title(title):
            raise ValueError("Note with this title already exists")
        note = Note(title, content)
        self.notes.append(note)
        return "Note added successfully :)"

    def find_note_by_title(self, title):
        if not title or title.strip() == "":
            raise ValueError("Title is required. Please, let me know what to look for")
        
        title_lower = title.lower()
        for note in self.notes:
            if note.title.value.lower() == title_lower:
                return note
        
        return None
    
    def show_note(self, title):
        note = self.find_note_by_title(title)
        if note:
            print(f"Found note: {note}")
        else:
            print("Note not found")
    
    def change_note(self, title, new_content):
        note = self.find_note_by_title(title)
        if note: 
            note.content = Content(new_content) if new_content else note.content
            return "Note updated successfully"
        else:
            return "Note not found"
        
    def delete_note(self, title):
        note = self.find_note_by_title(title)
        if note:
            self.notes.remove(note)
            return "Note deleted successfully"
        else:
            return "Note not found"
        
    def show_all_notes(self):
        if not self.notes:
            return "You do not have any notes yet..."
        
        divider = "=" * 50
        return "\n".join(f"{divider}\n{note}\n{divider}" for note in self.notes)
        


#Check the code. This part will be delated before sending our mentor :)

# title1 = Title ("Ромашка")
# print(title1)
# content1 = Content("")
# print(content1)
# note1 = Note ("Test the title! secont part, 123", "Check the content. Second part of the note is printed")
# print(note1)
# nb = NotesBook()
# print(nb.notes) 


#notes_book = NotesBook()
#print(notes_book.add_note("First Note", "This is the content of the first note."))
#print(notes_book.add_note("Second Note", "This is the content of the second note."))
# print(notes_book.show_all_notes())
#note = notes_book.find_note_by_title("First note")

#print(notes_book.change_note("First Note", "Updated content for the first note."))
#print(notes_book.show_all_notes())

#print(notes_book.delete_note("Second Note"))
#print(notes_book.show_all_notes())

#print(notes_book.delete_note("Third Note"))