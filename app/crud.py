# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas

REQUIRED_PUT_FIELDS = {
    "first_name", "last_name", "age", "gender", "email", "birth_date", "phone_number"
}

# ---------- CREATE ----------
def create_employee(db: Session, employee: schemas.EmployeeCreate):
    
    try:
        data = employee.model_dump()
    except AttributeError:
        data = employee.dict()

    obj = models.Employee(**data)
    db.add(obj)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        
        raise e
    db.refresh(obj)  
    return obj

# ---------- READ (list) ----------
def get_employees(db: Session):
    return db.query(models.Employee).all()

# ---------- READ (by id) ----------
def get_employee_by_id(db: Session, employee_id: int):
    return db.get(models.Employee, employee_id)

# ---------- UPDATE (partial/full) ----------
def update_employee(db: Session, employee_id: int, data: schemas.EmployeeUpdate):
    emp = db.get(models.Employee, employee_id)
    if not emp:
        return None

    try:
        payload = data.model_dump(exclude_unset=True, exclude_none=True)
    except AttributeError:
        payload = data.dict(exclude_unset=True, exclude_none=True)

    for field, value in payload.items():
        setattr(emp, field, value)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise e
    db.refresh(emp)
    return emp

# ---------- DELETE ----------
def delete_employee(db: Session, employee_id: int) -> bool:
    emp = db.get(models.Employee, employee_id)
    if not emp:
        return False
    db.delete(emp)
    db.commit()
    return True


# ---------- REPLACE (full update for PUT) ----------
def replace_employee(db: Session, employee_id: int, data: schemas.EmployeePut):
    emp = db.get(models.Employee, employee_id)
    if not emp:
        return None

    payload = data.model_dump()

    # 1) همه کلیدها باید باشند
    missing_keys = REQUIRED_PUT_FIELDS - set(payload.keys())
    if missing_keys:
        # این حالت عملاً با اسکیمای بالا رخ نمی‌دهد، ولی محکم‌کاری
        raise ValueError(f"Missing required fields: {', '.join(sorted(missing_keys))}")

    # 2) هیچ‌کدام نباید None/خالی باشد
    empty = [k for k, v in payload.items() if v is None or (isinstance(v, str) and v.strip() == "")]
    if empty:
        raise ValueError(f"Fields must not be empty: {', '.join(sorted(empty))}")

    for field, value in payload.items():
        setattr(emp, field, value)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise e

    db.refresh(emp)
    return emp