# Diese Klasse gehört zu Pydantic / FastAPI.
# Sie definiert nur die Struktur der JSON-Daten (Eingabe und Ausgabe).
# Sie erstellt KEINE echte Tabelle in der Datenbank!
# Sie prüft nur, ob die gesendeten oder empfangenen Daten richtig sind (z. B. Datentypen und Pflichtfelder).

from typing import Optional, Literal, Annotated
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date, datetime  # <-- ich nutze "date" für Geburtstage

#Pattern für die Validierung der Eingaben
NAME_PATTERN = r"^[A-Za-zÄÖÜäöüß\- ]{1,100}$"
PHONE_PATTERN = r"^\+?[0-9]{6,20}$"

Gender = Literal["male", "female", "diverse"]

# ---------- Base: Grundstruktur für Mitarbeiter ----------
class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    birth_date: Optional[date] = None   # nur Datum, kein Zeitstempel
    phone_number: Optional[str] = None

# ---------- Create: Schema für Erstellung eines Mitarbeiters ----------
class EmployeeCreate(EmployeeBase):
    first_name: str
    last_name: str
    email: EmailStr

# ---------- Update: Schema für Aktualisierung eines Mitarbeiters ----------
class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    birth_date: Optional[date] = None   # hier nur Datum
    phone_number: Optional[str] = None

# ---------- Output: Schema für Rückgabe eines Mitarbeiters ----------
class EmployeeOut(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  #korrekt für Pydantic v2

