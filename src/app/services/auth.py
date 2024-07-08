import jwt
import boto3
import json
import pytz
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from botocore.exceptions import ClientError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class Auth:
    @staticmethod
    def get_secret():
        secret_name = "traffic-violations/secret"
        region_name = "us-east-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            secret = json.loads(get_secret_value_response["SecretString"])
            return secret["SECRET_KEY"]
        except ClientError as e:
            raise HTTPException(
                status_code=500, detail=f"Error retrieving secret: {str(e)}"
            )

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        SECRET_KEY = Auth.get_secret()
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(pytz.utc) + expires_delta
        else:
            expire = datetime.now(pytz.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
        return encoded_jwt

    @staticmethod
    def validate_token(token: str = Depends(oauth2_scheme)):
        SECRET_KEY = Auth.get_secret()
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            officer_id = payload.get("sub")
            if officer_id is None:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            return officer_id
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))
