from fastapi import APIRouter, HTTPException, status
from typing import List
from src.app import schemas
from src.app.services.officer import Officer
# import redis

router = APIRouter()

# redis_host = "master.my-redis.ubhjx9.use1.cache.amazonaws.com"
# redis_password = "thistokenisforredis777"
# redis_client = redis.StrictRedis(
#         host=redis_host,
#         port=6379,
#         password=redis_password,
#         decode_responses=True,
#         ssl=True,
#         ssl_cert_reqs=None
#     )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(officer: schemas.Officer):
    try:
        existing_officer = Officer.get_officer_by_identification(officer.identification)
        if existing_officer:
            raise HTTPException(
                status_code=400,
                detail="Officer with this identification already exists",
            )
        Officer.create_officer(officer)
        return officer
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{officer_id}", status_code=status.HTTP_200_OK)
def read(officer_id: str):
    try:
        officer = Officer.get_officer(officer_id)
        if officer:
            return officer
        else:
            raise HTTPException(status_code=404, detail="Officer not found")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{officer_id}", status_code=status.HTTP_200_OK)
def update(officer_id: str, officer: schemas.Officer):
    try:
        officer = Officer.update_officer(officer_id, officer)
        if officer == "ConditionalCheckFailedException":
            raise HTTPException(status_code=404, detail="Officer not found")
        officer.officer_id = officer_id
        return officer
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{officer_id}", status_code=status.HTTP_200_OK)
def delete(officer_id: str):
    try:
        officer = Officer.delete_officer(officer_id)
        if officer == "ConditionalCheckFailedException":
            raise HTTPException(status_code=404, detail="Officer not found")
        return {"officer_id": officer_id}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[schemas.Officer], status_code=status.HTTP_200_OK)
def get_officers():
    try:
        officers = Officer.get_all_officers()
        if not officers:
            raise HTTPException(status_code=404, detail="No officers found")
        return officers
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
