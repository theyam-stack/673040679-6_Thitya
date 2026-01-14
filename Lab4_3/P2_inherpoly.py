#Lab 4-3 P2
from datetime import datetime, timedelta
class Person:
    # attributes
    _current_running_num = 0
    _last_id_year = None

    def __init__(self, name, age, bd, blood, status):
        self.name = name
        self.age = age
        self._birthdate = bd 
        self.__bloodgroup = blood
        self.__is_married = status 
        self._id = self._generate_id() 

    # Private instance method
    def _generate_id(self):
        current_y = datetime.now().year
        
        if Person._last_id_year != current_y:
            Person._current_running_num = 0
            Person._last_id_year = current_y
        
        Person._current_running_num += 1
        return f"{current_y}{Person._current_running_num:03d}"

    # Public method
    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"ID: {self._id}")
        print(f"Birth date: {self._birthdate}")
        print(f"Blood group: {self.__bloodgroup}")
        print(f"Matital status: {'Yes, Married.' if self.__is_married else 'No.'}")
        # Cannot directly access __bloodgroup or __is_married here, need getter methods

    def get_bloodgroup(self):
        return self.__bloodgroup

    def get_marital_status(self):
        return self.__is_married

class Staff(Person):
    # attr
    def __init__(self, name, age, bd, blood, status, dept, start_y):
        super().__init__(name, age, bd, blood, status)
        self.dept = dept
        self.start_year = start_y
        self.work_year = self._tenure_year()
  
    # Private instance method
    def _tenure_year(self):
        return datetime.now().year - self.start_year

    # Pub methods
    def get_salary(self):
        return self.__salary

    def set_salary(self, salary):
        if isinstance(salary, float) and salary > 0.0:
          self.__salary = salary
        else:
            print("Salary cannot be negative.")

    def display_info(self):
        super().display_info()
        print(f"Department: {self.dept}")
        print(f"Start year: {self.start_year}")
        print(f"Tenure year: {self.work_year}")
        print(f"Salary: {self.__salary:.2f}")

class Student(Person):
    _GRADE_STANDARD = {
      'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0,
      'B+': 3.5, 'C+': 2.5, 'D+': 1.5 }
    #attr
    def __init__(self, name, age, bd, blood, status, start_y, major, level, g_list=None, gpa=0.0, grad_date=None):
        super().__init__(name, age, bd, blood, status)
        self.start_year = start_y
        self.major = major
        self.level = level
        self.grade_list = g_list
        self.gpa = self.calc_gpa(self.grade_list) if self.grade_list else 0
        self.__grad_date = self._calc_grad_date()

    # methods
    @staticmethod
    def calc_gpa(inlist_of_cr_and_grade):
        total_scores = 0.0
        total_credits = 0.0
        for credit, grade in inlist_of_cr_and_grade:
          grade = grade.upper()
          if grade in Student._GRADE_STANDARD:
            total_scores += Student._GRADE_STANDARD[grade] * credit
            total_credits += credit
          else:
            print(f"Invalid grade: {grade}")
        return total_scores / total_credits if total_credits > 0 else 0.0

    #instancemethod
    def _calc_gpa_instance(self):
        self.gpa = Student.calc_gpa(self.grade_list)
        return self.gpa

    def _calc_grad_date(self):
        if self.level.lower() == "undergraduate":
            return self.start_year + 4
        elif self.level.lower() == "graduate":
            return self.start_year + 2
        else:
            return None

    def get_grad_date(self):
        return self.__grad_date

    def display_info(self):
        super().display_info()
        print(f"Start year: {self.start_year}")
        print(f"Major: {self.major}")
        print(f"Level: {self.level}")
        print(f"Grade list: {self.grade_list}") 
        print(f"GPA: {self.gpa:.2f}")
        print(f"Graduation date: {self.__grad_date}")

# Classes that inherit from Staff:
class Professor(Staff):
    PROFESSORSHIP_TITLES = {
        0: 'Lecturer',
        1: 'Assistant Prof',
        2: 'Assoc Prof',
        3: 'Full Prof',
        4: 'Highest Full Prof'
    }

    def __init__(self, name, age, bd, blood, status, dept, start_y, professor_lev, admin_position_status=0):
        super().__init__(name, age, bd, blood, status, dept, start_y)
        self.professorship_level = professor_lev
        self.admin_position_status = admin_position_status
        self.set_salary() 

    def set_salary(self):
        salary = 30000 + self.work_year * 1000 + self.professorship_level * 10000 + self.admin_position_status * 10000
        self._Staff__salary = salary

    def display_info(self):
        super().display_info()
        professor_title = Professor.PROFESSORSHIP_TITLES.get(self.professorship_level, 'Unknown')
        if self.admin_position_status == 1:
          admin_status_str = 'Has Admin Position'
        elif self.admin_position_status == 0:
          admin_status_str = 'No Admin Position'
        else:
          admin_status_str = 'Unknown'

        print(f"Professorship: {professor_title}")
        print(f"Admin Position: {admin_status_str}")


class Administrator(Staff):
    ADMIN_POSITION_TITLES = {
        0: 'Entry',
        1: 'Professional',
        2: 'Expert',
        3: 'Manager',
        4: 'Director'
    }

    def __init__(self, name, age, bd, blood, status, dept, start_y, admin_position_lev):
        super().__init__(name, age, bd, blood, status, dept, start_y)
        self.admin_position_level = admin_position_lev
        self.set_salary()

    def set_salary(self):
        salary = 15000 + self.work_year * 800 + self.admin_position_level * 5000
        self._Staff__salary = salary

    def display_info(self):
        super().display_info()
        admin_title = Administrator.ADMIN_POSITION_TITLES.get(self.admin_position_level, 'Unknown')
        print(f"Admin Position: {admin_title}")

# class that inherit from Student:
class UndergraduateStudent(Student):
    def __init__(self, name, age, bd, blood, status, start_y, major, level, g_list=None, club=None, course_list=None):
        super().__init__(name, age, bd, blood, status, start_y, major, level, g_list)
        self.club = club if club is not None else "None"
        self.course_list = course_list if course_list is not None else []

    def register_course(self, course_name):
        if course_name not in self.course_list:
            self.course_list.append(course_name)
            print(f"{self.name} registered for {course_name}.")
        else:
            print(f"{self.name} is already registered for {course_name}.")

    def display_info(self):
        super().display_info()
        print(f"Club: {self.club}")
        print(f"Courses: {', '.join(self.course_list) if self.course_list else 'None'}")

class GraduateStudent(Student):
    def __init__(self, name, age, bd, blood, status, start_y, major, level, advisor_name, g_list=None, thesis_name=None, proposal_date=None):
        self.__proposal_date = None
        super().__init__(name, age, bd, blood, status, start_y, major, level, g_list)
        self.advisor_name = advisor_name
        self.thesis_name = thesis_name

        if proposal_date:
            self.set_proposal_date(proposal_date) # This will also update graduation_date

    def _calc_grad_date(self): # Override parent method
        if self.__proposal_date:
            # Graduation date is 1 year from proposal date
            return (self.__proposal_date + timedelta(days=365)).year
        else:
            # Graduation date is 2 years from today
            return (datetime.now() + timedelta(days=2*365)).year

    def set_thesis_name(self, thesis):
        self.thesis_name = thesis
        print(f"Thesis name set to: {self.thesis_name}")

    def set_proposal_date(self, prop_date_str):
        try:
            # Assuming proposal_date is in 'YYYY-MM-DD' format
            self.__proposal_date = datetime.strptime(prop_date_str, '%Y-%m-%d')
            self._Student__graduation_date = self._calc_grad_date() # Update graduation date
            print(f"Proposal date set to: {self.__proposal_date.strftime('%Y-%m-%d')}")
            print(f"Graduation date updated to: {self._Student__graduation_date}")
        except ValueError:
            print("Invalid date format for proposal date. Please use YYYY-MM-DD.")

    def get_proposal_date(self):
        return self.__proposal_date.strftime('%Y-%m-%d') if self.__proposal_date else "Not set"

    def display_info(self):
        super().display_info()
        print(f"Advisor: {self.advisor_name}")
        print(f"Thesis Name: {self.thesis_name if self.thesis_name else 'Not set'}")
        print(f"Proposal Date: {self.get_proposal_date()}")
