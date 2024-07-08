from pydantic import BaseModel, constr


class Person(BaseModel):
    person_id: str = ""
    name: str
    email: str


class Vehicle(BaseModel):
    vehicle_id: str = ""
    license_plate: str
    brand: str
    color: str
    person_id: str


class Officer(BaseModel):
    officer_id: str = ""
    name: str
    identification: str


class Infraction(BaseModel):
    infraction_id: str = ""
    license_plate: str
    timestamp: str = ""
    comments: constr(max_length=255)
