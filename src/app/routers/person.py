from fastapi import APIRouter, HTTPException, status
from src.app import schemas
from src.app.services.person import Person
from typing import List

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(person: schemas.Person):
    try:
        existing_person = Person.get_person_by_email(person.email)
        if existing_person:
            raise HTTPException(
                status_code=400, detail="Person with this email already exists"
            )
        Person.create_person(person)
        return person
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{person_id}", status_code=status.HTTP_200_OK)
def read(person_id: str):
    try:
        person = Person.get_person(person_id)
        if person:
            return person
        else:
            raise HTTPException(status_code=404, detail="Person not found")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{person_id}", status_code=status.HTTP_200_OK)
def update(person_id: str, person: schemas.Person):
    try:
        person = Person.update_person(person_id, person)
        if person == "ConditionalCheckFailedException":
            raise HTTPException(status_code=404, detail="Person not found")
        person.person_id = person_id
        return person
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{person_id}", status_code=status.HTTP_200_OK)
def delete(person_id: str):
    try:
        person = Person.delete_person(person_id)
        if person == "ConditionalCheckFailedException":
            raise HTTPException(status_code=404, detail="Person not found")
        return {"person_id": person_id}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[schemas.Person], status_code=status.HTTP_200_OK)
def get_persons():
    try:
        persons = Person.get_all_persons()
        if not persons:
            raise HTTPException(status_code=404, detail="No persons found")
        return persons
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
