from fastapi import APIRouter, HTTPException, status, Depends
from src.app import schemas
from src.app.services.infraction import Infraction
from src.app.services.vehicle import Vehicle
from src.app.services.auth import Auth
from src.app.services.person import Person

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def charge_infraction(
    infraction: schemas.Infraction, token: str = Depends(Auth.validate_token)
):
    try:
        vehicle = Vehicle.get_vehicle_by_license_plate(infraction.license_plate)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")

        Infraction.create_infraction(infraction)
        return infraction
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{person_email}", status_code=status.HTTP_200_OK)
def generate_report(person_email: str):
    try:
        person = Person.get_person_by_email(person_email)
        if not person:
            raise HTTPException(status_code=404, detail="Person not found")
        print("....person: ", person)
        vehicles = Vehicle.get_vehicles_by_person_id(person.person_id)
        if not vehicles:
            raise HTTPException(status_code=404, detail="Vehicles not found")
        print("....vehicles: ", vehicles)
        license_plates = [vehicle.license_plate for vehicle in vehicles]
        print("....license_plates: ", license_plates)
        infractions = Infraction.get_infractions_by_license_plates(license_plates)
        if infractions:
            return infractions
        else:
            raise HTTPException(status_code=404, detail="Infractions not found")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
