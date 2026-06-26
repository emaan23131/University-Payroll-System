class PaymentDepartment:

    def __init__(self):
        self.history = []

    def generate_payment_slip(
        self,
        employee,
        amount
    ):

        payment = {
            "employee_id": employee.employee_id,
            "employee_name": employee.name,
            "amount": amount,
            "date": str(datetime.now())
        }

        self.history.append(payment)

        return payment

    def get_history(self):
        return self.history