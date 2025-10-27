# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas

# ---------- CREATE ----------
def create_employee(db: Session, employee: schemas.EmployeeCreate):
    # Pydantic v2 / v1 سازگاری
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
        # مهم: همان IntegrityError را بالا بده تا Router/handler آن را به 409 تبدیل کند
        raise e
    db.refresh(obj)  # تا id/created_at را داشته باشیم
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

    # فقط فیلدهای ست‌شده و غیر None را اعمال کن
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
