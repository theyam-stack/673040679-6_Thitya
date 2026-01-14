# --- Test Cases for all classes ---
from P2_inherpoly import Person, Staff, Professor, Administrator, Student, UndergraduateStudent, GraduateStudent

print("\n---- Testing Staff Class ----")
staff_1 = Staff("Dr. Preeya", 47, "1979-03-15", "O-", True, "Computer Science", 2007)
staff_1.set_salary(65000.00)
staff_1.display_info()

print("\n---- Testing Professor Class ----")
prof1 = Professor("Dr. Sarun", 40, "1986-01-20", "AB+", True, "Mathematics", 2013, 1)  # Assistant Prof, No Admin
staff_1.set_salary(52000.90)
prof1.display_info()
print()

prof2 = Professor("Dr. Witcha", 50, "1976-07-07", "B-", False, "Game Design", 2002, 3, 1) # Full Prof, Admin Position
prof2.display_info()

print("\n---- Testing Administrator Class ----")
admin1 = Administrator("Yin Anan Wong", 56, "1970-10-01", "A-", True, "Registrar", 1999, 4) # Director level
admin1.display_info()
print()

admin2 = Administrator("War Wanarat", 32, "1994-06-23", "B+", True, "HR", 2018, 1) # Professional level
admin2.display_info()

print("\n---- Testing Student Class ----")
student1 = Student("Mary Nanthaphat", 20, "2006-05-14", "A+", False, 2025, "Law", "undergraduate", [(3, 'A'), (3, 'B'), (2, 'A')], 3.80 , "Unknow")
student1.display_info()

print("\n---- Testing UndergraduateStudent Class ----")
ug_student1 = UndergraduateStudent("Eva Green", 19, "2005-01-15", "O+", False, 2023, "Biology", "undergraduate", [(3, 'A'), (3, 'B')], "Chess Club", ["Bio 101", "Chem 101"])
print("\n---- Original ----")
ug_student1.display_info()
print("\n---- After Registered ----")
ug_student1.register_course("Math 101")
ug_student1.register_course("Bio 101") # Should show already registered
ug_student1.display_info()
print()

ug_student2 = UndergraduateStudent("Mike Ross", 21, "2003-04-22", "AB", False, 2021, "Law", "undergraduate", [(4, 'A'), (3, 'B'), (3, 'C+')], "Debate Society")
ug_student2.register_course("Criminal Law")
ug_student2.display_info()
print()

print("\n---- Testing GraduateStudent Class ----")
grad_student1_grades = [(3, 'A'), (3, 'C+'), (3, 'B+'), (1, 'B'), (3, 'A')]
grad_student1 = GraduateStudent("Amon Os Hackle", 29, "1997-12-21", "A+", True, 2024, "Computer Science", "graduate", "Dr. Alex", grad_student1_grades, "Advanced AI Algorithms", "2025-06-01")
grad_student1.display_info()
print()

grad_student2 = GraduateStudent("Mia Wong", 26, "1998-09-10", "B+", False, 2024, "Physics", "graduate", "Dr. Sarah")
print("\n--- Original Format ---")
grad_student2.display_info()
print("\n--- Updated Format ---")
grad_student2.set_thesis_name("Quantum Computing Applications")
grad_student2.set_proposal_date("2026-01-15")
print()
grad_student2.display_info()
print()

print(f"Leo King's proposal date: {grad_student1.get_proposal_date()}")
print(f"Mia Wong's proposal date: {grad_student2.get_proposal_date()}")
