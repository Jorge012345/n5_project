from fastapi import APIRouter, HTTPException
from src.app.services.auth import Auth
from datetime import timedelta
from src.app.services.officer import Officer

router = APIRouter()


@router.post("/token")
def login_officer(officer_id: str):
    try:
        officer = Officer.get_officer(officer_id)
        if not officer:
            raise HTTPException(status_code=404, detail="Officer not found")

        access_token_expires = timedelta(minutes=30)
        access_token = Auth.create_access_token(
            data={"sub": officer_id}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
