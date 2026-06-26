from datetime import datetime


class Deduction:

    def __init__(self, tax=0, insurance=0, loan=0):
        self.tax = tax
        self.insurance = insurance
        self.loan = loan

    def total_deductions(self):
        return self.tax + self.insurance + self.loan


class Salary:

    def __init__(
        self,
        basic_salary=0,
        allowance=0,
        bonus=0,
        deduction=None
    ):

        self.basic_salary = basic_salary
        self.allowance = allowance
        self.bonus = bonus

        self.deduction = deduction or Deduction()

    def gross_salary(self):
        return (
            self.basic_salary
            + self.allowance
            + self.bonus
        )

    def net_salary(self):
        return (
            self.gross_salary()
            - self.deduction.total_deductions()
        )


class Employee:

    def __init__(
        self,
        employee_id,
        name,
        email,
        phone,
        department
    ):

        self.employee_id = employee_id
        self.name = name
        self.email = email
        self.phone = phone
        self.department = department

        self.salary = Salary()

    def display(self):

        return {
            "ID": self.employee_id,
            "Name": self.name,
            "Email": self.email,
            "Phone": self.phone,
            "Department": self.department
        }


class Faculty(Employee):

    def __init__(
        self,
        employee_id,
        name,
        email,
        phone,
        department,
        qualification,
        research_allowance=0
    ):

        super().__init__(
            employee_id,
            name,
            email,
            phone,
            department
        )

        self.qualification = qualification
        self.research_allowance = research_allowance

    def employee_type(self):
        return "Faculty"


class Staff(Employee):

    def __init__(
        self,
        employee_id,
        name,
        email,
        phone,
        department,
        designation,
        performance_bonus=0
    ):

        super().__init__(
            employee_id,
            name,
            email,
            phone,
            department
        )

        self.designation = designation
        self.performance_bonus = performance_bonus

    def employee_type(self):
        return "Staff"