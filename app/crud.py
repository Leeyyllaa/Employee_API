#app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas


# Create new employee
def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# Alle Mitarbeiter abrufen (READ)
def get_employees(db: Session):
    return db.query(models.Employee).all()


# Einen Mitarbeiter per ID abrufen(READ)
def get_employee_by_id(db: Session, employee_id: int):
    return db.get(models.Employee, employee_id) 


# Update
def update_employee(db: Session, employee_id: int, data: schemas.EmployeeUpdate):
    emp = db.get(models.Employee, employee_id)
    if not emp:
        return None

    payload = data.dict(exclude_unset=True, exclude_none=True)

    for field, value in payload.items():
        setattr(emp, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(emp)
    return emp

# Einen Mitarbeiter per ID löschen (DELETE)
def delete_employee(db: Session, employee_id: int) -> bool:
    emp = db.get(models.Employee, employee_id)
    if not emp:
        return False
    db.delete(emp)
    db.commit()
    return True