from P1_inherpoly import LibraryItem
from P1_inherpoly import Book
from P1_inherpoly import TextBook
from P1_inherpoly import Magazine

print("\n---- Testing TextBook Class ----")
textbook1 = TextBook("Python Programming", "TB001", "John Doe", "Computer Science", 10)
textbook1.set_page_count(500)
textbook1.display_info()
textbook1.check_out()
print(f"Status after checkout: {textbook1.get_status()}\n")
textbook1.display_info()
textbook1.return_item()
print(f"Status after return: {textbook1.get_status()}")

print("\n--- Another TextBook ---")
textbook2 = TextBook("Advanced Calculus", "TB002", "Jane Smith", "Mathematics", "University")
textbook2.set_page_count(750)
textbook2.display_info()

print("---- Testing Magazine Class ----")
magazine = Magazine("National Geographic", "M001", 210)
magazine.display_info()
magazine.check_out()
print(f"Status after checkout: {magazine.get_status()}")
print()
magazine.display_info()
magazine.return_item()
print()
magazine.display_info()

# This is just an example. You should test a lot more than this.
print("\n---- Testing Book Class ----")
book = Book("Harry Potter", "B001", "J.K. Rowling")
print(book.get_status())  # Should print: Available
book.check_out()
print(book.get_status())  # Should print: Checked out