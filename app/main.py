# Beschreibung:
# Hauptdatei der Employee-API.
# Diese Datei startet die FastAPI-Anwendung,
# verbindet sie mit der Datenbank und bindet
# alle Router (z. B. für Mitarbeiter) ein.

from fastapi import FastAPI
from app.database import engine
from . import models
from app.routers.employees import router as employees_router

# Erstellt automatisch alle Tabellen in der Datenbank, falls sie noch nicht existieren
models.Base.metadata.create_all(bind=engine)

#Erstellt die Hauptanwendung
app = FastAPI(title="Employee API")

#Einfache Test-Route zum Überprüfen der Verbindung
@app.get("/")
def root():
    return {"message": "✅ Verbindung zur Datenbank erfolgreich!"}

# Bindet den Mitarbeiter-Router ein (alle Endpunkte für Employees)
app.include_router(employees_router)



# #Abhängigkeit für die Datenbankverbindung
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Create new employee
# @app.post("/employees", response_model=schemas.EmployeeOut)
# def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
#     return crud.create_employee(db=db, employee=employee)


# # Alle Mitarbeiter abrufen
# @app.get("/employees", response_model=list[schemas.EmployeeOut])
# def read_employees(db: Session = Depends(get_db)):
#     return crud.get_employees(db)


# # Einzelnen Mitarbeiter per ID abrufen
# @app.get("/employees/{employee_id}", response_model=schemas.EmployeeOut)
# def read_employee(employee_id: int, db: Session = Depends(get_db)):
#     emp = crud.get_employee_by_id(db, employee_id)
#     if not emp:
#         raise HTTPException(status_code=404, detail="Employee not found")
#     return emp


# # UPDATE (PUT)
# # @app.put("/employees/{employee_id}", response_model=schemas.EmployeeOut)
# # def update_employee(employee_id: int, data: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
# #     try:
# #         emp = crud.update_employee(db, employee_id, data)
# #     except IntegrityError:
# #         raise HTTPException(status_code=409, detail="Email or phone_number already exists")
# #     if not emp:
# #         raise HTTPException(status_code=404, detail="Employee not found")
# #     return emp

# # UPDATE (PATCH)
# @app.patch("/employees/{employee_id}", response_model=schemas.EmployeeOut)
# def patch_employee(employee_id: int, data: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
#     emp = crud.update_employee(db, employee_id, data)
#     if not emp:
#         raise HTTPException(status_code=404, detail="Employee not found")
#     return emp

# # DELETE
# @app.delete("/employees/{employee_id}", status_code=204)
# def delete_employee(employee_id: int, db: Session = Depends(get_db)):
#     ok = crud.delete_employee(db, employee_id)
#     if not ok:
#         raise HTTPException(status_code=404, detail="Employee not found")
#     return None



