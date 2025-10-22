from fastapi import APIRouter

router = APIRouter(prefix='/employees', tags=['Employees'])

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, crud

@router.post("", response_model=schemas.EmployeeOut)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)

@router.get("", response_model=list[schemas.EmployeeOut])
def read_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db)

@router.get("/{employee_id}", response_model=schemas.EmployeeOut)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = crud.get_employee_by_id(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.put("/{employee_id}", response_model=schemas.EmployeeOut)
def update_employee_put(employee_id: int, data: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    emp = crud.update_employee(db, employee_id, data)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.patch("/{employee_id}", response_model=schemas.EmployeeOut)
def update_employee_patch(employee_id: int, data: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    emp = crud.update_employee(db, employee_id, data)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.delete("/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_employee(db, employee_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Employee not found")
    return None
