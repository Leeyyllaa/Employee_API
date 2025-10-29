# Diese Klasse gehört zu Pydantic / FastAPI.
# Sie definiert nur die Struktur der JSON-Daten (Eingabe und Ausgabe).
# Sie erstellt KEINE echte Tabelle in der Datenbank!
# Sie prüft nur, ob die gesendeten oder empfangenen Daten richtig sind (z. B. Datentypen und Pflichtfelder).

from typing import Optional, Literal, Annotated
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import date, datetime

#Pattern: 
NAME_PATTERN = r"^[A-Za-zÄÖÜäöüß\- ]{1,100}$"
PHONE_PATTERN = r"^\+?[0-9]{6,20}$"

Gender = Literal["male", "female", "diverse"]


# ---------- Base: Grundstruktur für Mitarbeiter ----------
class EmployeePut(BaseModel):
    model_config = ConfigDict(extra="forbid") 

    first_name:   Annotated[str, Field(pattern=NAME_PATTERN, max_length=100)]
    last_name:    Annotated[str, Field(pattern=NAME_PATTERN, max_length=100)]
    age:          Annotated[int, Field(ge=16, le=120)]
    gender:       Gender
    email:        EmailStr
    birth_date:   date
    phone_number: Annotated[str, Field(pattern=PHONE_PATTERN, max_length=20)]

    @field_validator("birth_date")
    @classmethod
    def birth_must_be_past(cls, v: date):
        if v < date(1900, 1, 1):
            raise ValueError("birth_date must be after 1900-01-01")
        if v >= date.today():
            raise ValueError("birth_date must be in the past")
        return v

# ---------- Create: Schema für Erstellung eines Mitarbeiters ----------
class EmployeeCreate(BaseModel):
    first_name:   Annotated[str, Field(pattern=NAME_PATTERN, max_length=100)]
    last_name:    Annotated[str, Field(pattern=NAME_PATTERN, max_length=100)]
    email:        EmailStr


# ---------- Update: Schema für Aktualisierung eines Mitarbeiters ----------
class EmployeeUpdate(BaseModel):
    first_name:   Optional[Annotated[str, Field(pattern=NAME_PATTERN, max_length=100)]] = None
    last_name:    Optional[Annotated[str, Field(pattern=NAME_PATTERN, max_length=100)]] = None
    age:          Optional[int] = Field(default=None, ge=16, le=120)
    gender:       Optional[Gender] = None
    email:        Optional[EmailStr] = None
    birth_date:   Optional[date] = None
    phone_number: Optional[Annotated[str, Field(pattern=PHONE_PATTERN, max_length=20)]] = None

    @field_validator("birth_date")
    @classmethod
    def birth_must_be_past(cls, v: Optional[date]):
        if v is None:
            return v
        if v < date(1900, 1, 1):
            raise ValueError("birth_date must be after 1900-01-01")
        if v >= date.today():
            raise ValueError("birth_date must be in the past")
        return v

# ---------- Output: Schema für Rückgabe eines Mitarbeiters ----------
class EmployeeOut(BaseModel):
    id:           int
    first_name:   str
    last_name:    str
    age:          Optional[int] = None
    gender:       Optional[Gender] = None
    email:        EmailStr
    birth_date:   Optional[date] = None
    phone_number: Optional[str] = None
    created_at:   datetime
    updated_at:   Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
