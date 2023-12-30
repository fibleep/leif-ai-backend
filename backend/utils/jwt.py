import time
import jwt
import jwt
from fastapi import Depends
import dotenv
import os

from backend.db.models.user_model import UserModel

JWT_SECRET = os.getenv("BACKEND_SECRET_KEY")
JWT_ALGORITHM = os.getenv("BACKEND_ALGORITHM")

def sign_jwt(user: UserModel):
    expiration_time = time.time() + (16 * 60 * 60)  # 16 hours (60 minutes * 60 seconds)
    payload = {
        "user_id": user.id,
        "user_email": user.email,
        "role": user.role,
        "expires": expiration_time
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token=token)


def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print(decoded_token);
        return decoded_token if decoded_token['expires'] >= time.time() else {}
    except:
        return {}


def token_response(token: str):
    return {
        "access": token
    }
