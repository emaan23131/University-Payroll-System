
from models import Faculty
from models import Staff


class PayrollSystem:

    def __init__(self):

        self.employees = []

    def add_faculty(
        self,
        employee_id,
        name,
        email,
        phone,
        department,
        qualification,
        research_allowance
    ):

        faculty = Faculty(
            employee_id,
            name,
            email,
            phone,
            department,
            qualification,
            research_allowance
        )

        self.employees.append(faculty)

    def add_staff(
        self,
        employee_id,
        name,
        email,
        phone,
        department,
        designation,
        performance_bonus
    ):

        staff = Staff(
            employee_id,
            name,
            email,
            phone,
            department,
            designation,
            performance_bonus
        )

        self.employees.append(staff)

    def get_employee(
        self,
        employee_id
    ):

        for emp in self.employees:

            if emp.employee_id == employee_id:
                return emp

        return None

    def remove_employee(
        self,
        employee_id
    ):

        self.employees = [

            emp
            for emp in self.employees

            if emp.employee_id != employee_id

        ]

    def get_all_employees(self):

        return self.employees