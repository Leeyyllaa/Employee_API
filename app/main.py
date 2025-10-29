# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.database import engine
from app import models
from app.routers.employees import router as employees_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee API")


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    msg = str(getattr(exc, "orig", exc))

    if "uq_emp_fullname_ci" in msg:
        detail = "Ein Mitarbeiter mit diesem Vor- und Nachnamen ist bereits vorhanden."
    elif "employees_email_key" in msg:
        detail = "Diese E-Mail-Adresse ist bereits registriert."
    elif "employees_phone_number_key" in msg:
        detail = "Diese Telefonnummer ist bereits registriert."
    else:
        detail = "Fehler beim Speichern der Daten (möglicherweise doppelt oder ungültig)."

    return JSONResponse(status_code=409, content={"detail": detail})

@app.get("/")
def root():
    return {"message": "✅ Verbindung zur Datenbank erfolgreich!"}

app.include_router(employees_router)
