#P1 Lab 4-3
from datetime import datetime
class LibraryItem:
    def __init__(self, title, item_id):
        self.title = title
        self._id = item_id
        self._checked_out = False
    
    def get_status(self):
        return "Checked out" if self._checked_out else "Available"
    
    def check_out(self):
        # if checked_out is False (item still in lib)
        if not self._checked_out:
            self._checked_out = True
            return True
        # can't check out if item not in lib
        return False

    def return_item(self): #1.1.1
        if self._checked_out:
            self._checked_out = False
            return True
        return False

    def display_info(self): #1.1.2
        print(f"Title: {self.title}")
        print(f"ID: {self._id}")
        print(f"Status: {self.get_status()}")

# implement 3 classes here
class Book(LibraryItem): #1.2.1
    def __init__(self, title, item_id, author):
        super().__init__(title, item_id)
        self.author = author
        self.pages_count = 0 # Add pages_count as a non-parameter instance attribute
    
    def set_page_count(self, pages):
        if isinstance(pages, int) and pages >= 0:
            self.pages_count = pages
        else:
            print("Invalid page count.")

    def display_info(self):
        super().display_info()
        print(f"Author: {self.author}")
        if self.pages_count > 0:
            print(f"Pages: {self.pages_count}")
        else:
            print("Pages: Not Avalible")

class TextBook(Book): #1.2.2
    def __init__(self, title, item_id, author, subject, grade_level):
        super().__init__(title, item_id, author)
        self.subject = subject
        self.grade_level = grade_level
    
    def display_info(self):
        super().display_info() # This super it's already print display_info that ประกาศไว้ all above
        print(f"Subject: {self.subject}")
        print(f"Grade Level: {self.grade_level}")
        print()

class Magazine(LibraryItem): #1.2.3
    def __init__(self, title, item_id, issue_num):
        super().__init__(title, item_id)
        self.issue_num = issue_num
        now = datetime.now()
        self.month = now.strftime("%B")   # e.g., "January"
        self.year = now.year              # e.g., 2026

    def display_info(self):
        super().display_info()
        print(f"Issue Number: {self.issue_num}")
        print(f"Month: {self.month}")
        print(f"Year: {self.year}")
