from fastapi import APIRouter, HTTPException, status
from src.app import schemas
from src.app.services.vehicle import Vehicle
from src.app.services.person import Person
from typing import List

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(vehicle: schemas.Vehicle):
    try:
        existing_vehicle = Vehicle.get_vehicle_by_license_plate(vehicle.license_plate)
        if existing_vehicle:
            raise HTTPException(
                status_code=400, detail="Vehicle with this license plate already exists"
            )
        existing_person = Person.get_person(vehicle.person_id)
        if not existing_person:
            raise HTTPException(status_code=404, detail="Person not found")

        Vehicle.create_vehicle(vehicle)
        return vehicle
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{vehicle_id}", status_code=status.HTTP_200_OK)
def read(vehicle_id: str):
    try:
        vehicle = Vehicle.get_vehicle(vehicle_id)
        if vehicle:
            return vehicle
        else:
            raise HTTPException(status_code=404, detail="Vehicle not found")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{vehicle_id}", status_code=status.HTTP_200_OK)
def update(vehicle_id: str, vehicle: schemas.Vehicle):
    try:
        vehicle = Vehicle.update_vehicle(vehicle_id, vehicle)
        if vehicle == "ConditionalCheckFailedException":
            raise HTTPException(status_code=404, detail="Vehicle not found")
        vehicle.vehicle_id = vehicle_id
        return vehicle
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{vehicle_id}", status_code=status.HTTP_200_OK)
def delete(vehicle_id: str):
    try:
        vehicle = Vehicle.delete_vehicle(vehicle_id)
        if vehicle == "ConditionalCheckFailedException":
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return {"vehicle_id": vehicle_id}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[schemas.Vehicle], status_code=status.HTTP_200_OK)
def get_vehicles():
    try:
        vehicles = Vehicle.get_all_vehicles()
        if not vehicles:
            raise HTTPException(status_code=404, detail="No vehicles found")
        return vehicles
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
