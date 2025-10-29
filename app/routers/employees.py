# app/routers/employees.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/employees", tags=["Employees"])

# ------------------ Mitarbeiter anlegen ------------------
@router.post("", response_model=schemas.EmployeeOut)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_employee(db, employee)
    except IntegrityError as e:
        db.rollback()
        msg = str(e.orig)
        if "uq_emp_fullname_ci" in msg:
            detail = "Ein Mitarbeiter mit diesem Vor- und Nachnamen ist bereits vorhanden."
        elif "employees_email_key" in msg:
            detail = "Diese E-Mail-Adresse ist bereits registriert."
        elif "employees_phone_number_key" in msg:
            detail = "Diese Telefonnummer ist bereits registriert."
        else:
            detail = "Fehler beim Speichern der Daten (möglicherweise doppelt oder ungültig)."
        raise HTTPException(status_code=409, detail=detail)

# ------------------ Alle Mitarbeiter abrufen ------------------
@router.get("", response_model=list[schemas.EmployeeOut])
def read_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db)

# ------------------ Einen Mitarbeiter nach ID abrufen ------------------
@router.get("/{employee_id}", response_model=schemas.EmployeeOut)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = crud.get_employee_by_id(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Mitarbeiter wurde nicht gefunden.")
    return emp

# ------------------ Mitarbeiter vollständig aktualisieren (PUT) ------------------
@router.put("/{employee_id}", response_model=schemas.EmployeeOut)
def replace_employee_put(
    employee_id: int,
    data: schemas.EmployeePut,
    db: Session = Depends(get_db)
):
    try:
        emp = crud.replace_employee(db, employee_id, data)
        if not emp:
            raise HTTPException(status_code=404, detail="Mitarbeiter wurde nicht gefunden.")
        return emp

    except ValueError as e:
        
        raise HTTPException(status_code=422, detail=str(e))

    except IntegrityError as e:
        db.rollback()
        msg = str(e.orig)
        if "uq_emp_fullname_ci" in msg:
            detail = "Ein Mitarbeiter mit diesem Vor- und Nachnamen ist bereits vorhanden."
        elif "employees_email_key" in msg:
            detail = "Diese E-Mail-Adresse ist bereits registriert."
        elif "employees_phone_number_key" in msg:
            detail = "Diese Telefonnummer ist bereits registriert."
        else:
            detail = "Fehler beim Aktualisieren der Daten."
        raise HTTPException(status_code=409, detail=detail)
        

# ------------------ Mitarbeiter teilweise aktualisieren (PATCH) ------------------
@router.patch("/{employee_id}", response_model=schemas.EmployeeOut)
def update_employee_patch(employee_id: int, data: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    try:
        emp = crud.update_employee(db, employee_id, data)
        if not emp:
            raise HTTPException(status_code=404, detail="Mitarbeiter wurde nicht gefunden.")
        return emp
    except IntegrityError as e:
        db.rollback()
        msg = str(e.orig)
        if "uq_emp_fullname_ci" in msg:
            detail = "Ein Mitarbeiter mit diesem Vor- und Nachnamen ist bereits vorhanden."
        elif "employees_email_key" in msg:
            detail = "Diese E-Mail-Adresse ist bereits registriert."
        elif "employees_phone_number_key" in msg:
            detail = "Diese Telefonnummer ist bereits registriert."
        else:
            detail = "Fehler beim Aktualisieren der Daten."
        raise HTTPException(status_code=409, detail=detail)

# ------------------ Mitarbeiter löschen ------------------
@router.delete("/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_employee(db, employee_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Mitarbeiter wurde nicht gefunden.")
    return None
