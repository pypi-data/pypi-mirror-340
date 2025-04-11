from sqlmodel import Session, select
from pto_common_timesheet_mfdenison_hopkinsep.models import PTO

class PTOUpdateManager:
    def __init__(self, session: Session, employee_id: int, new_balance: int = None):
        self.session = session
        self.employee_id = employee_id
        self.new_balance = new_balance

    def get_current_balance(self):
        statement = select(PTO).where(PTO.employee_id == self.employee_id)
        pto = self.session.exec(statement).first()
        if pto is None:
            pto = PTO(employee_id=self.employee_id, balance=0)
            self.session.add(pto)
            self.session.commit()
            self.session.refresh(pto)
        return pto.balance

    def update_pto(self):
        try:
            statement = select(PTO).where(PTO.employee_id == self.employee_id)
            pto = self.session.exec(statement).first()
            if pto is None:
                pto = PTO(employee_id=self.employee_id, balance=0)
                self.session.add(pto)
            pto.balance = self.new_balance
            self.session.commit()
            self.session.refresh(pto)
            return {
                "result": "success",
                "message": f"PTO balance updated to {self.new_balance}"
            }
        except Exception as e:
            return {
                "result": "error",
                "message": str(e)
            }

    def subtract_pto(self, deduction: int):
        try:
            statement = select(PTO).where(PTO.employee_id == self.employee_id)
            pto = self.session.exec(statement).first()
            if pto is None:
                pto = PTO(employee_id=self.employee_id, balance=0)
                self.session.add(pto)
            new_balance = pto.balance - deduction
            pto.balance = new_balance
            self.session.commit()
            self.session.refresh(pto)
            return {
                "result": "success",
                "message": f"PTO balance updated to {new_balance}"
            }
        except Exception as e:
            return {
                "result": "error",
                "message": str(e)
            }
