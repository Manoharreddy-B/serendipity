from fastapi import HTTPException
import jwt
import jwt.exceptions
import jwt.utils
from pydantic import BaseModel
import time
import os
from dotenv import load_dotenv

load_dotenv()

users = {
    "user1": {"id": 1, "username": "user1", "password": "password123"}
}

SECRET_AUTH_KEY = os.getenv("JWT_AUTH_TOKEN")

class TokenReponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
def create_access_token(user_id: int):
    payload = {
        "exp": time.time() + (60*60),
        "iat": time.time(),
        "sub": str(user_id)
    }
    
    # encoded_jwt = jwt.utils.b64encode(payload, SECRET_AUTH_KEY)
    encoded_jwt = jwt.encode(payload, SECRET_AUTH_KEY, algorithm="HS256")
    
    return encoded_jwt
    
def decode_access_token(token: str):
    try:
        # payload = jwt.utils.b64decode(token, SECRET_AUTH_KEY)
        payload = jwt.decode(token, SECRET_AUTH_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.ImmatureSignatureError:
        raise HTTPException(status_code=401, detail="Token not yet valid (iat issue)")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
