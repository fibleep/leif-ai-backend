"""
https://python.plainenglish.io/building-a-restful-api-with-fastapi-secure-signup-and-login-functionality-included-45cdbcb36106
"""

from docutils.nodes import status
from fastapi import APIRouter, Depends, HTTPException
import dotenv
import os
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.exc import SQLAlchemyError

from backend.db.dao.user_dao import UserDAO
from backend.db.models.user_model import UserModel
from backend.models.security_models import User, Token, TokenData
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from backend.models.user import ResUser, NewUser, Login
from backend.utils.hasher import hash_password, verify_hashed_password
from backend.utils.jwt import sign_jwt

router = APIRouter()
dotenv.load_dotenv()

SECRET_KEY = os.getenv("BACKEND_SECRET_KEY")
ALGORITHM = os.getenv("BACKEND_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# Endpoint for creating a new user
@router.post('/signup/', status_code=status.HTTP_201_CREATED, )
async def create_a_user(user: NewUser, user_dao: UserDAO = Depends()):
    try:
        # Hash the user's password
        hashed_password = await hash_password(user.password)

        # Create a new user object
        new_user = UserModel(
            email=user.email,
            password=hashed_password,
        )

        # Check if a user with the same email already exists
        db_item = await user_dao.get_user_by_email(user.email)

        if db_item is not None:
            raise HTTPException(status_code=400,
                                detail="User with the email already exists")

        # Add the new user to the database
        await user_dao.save(new_user)
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=500,
                            detail="An error occurred while creating the user")


# Endpoint for user login
@router.post('/login/')
async def login_a_user(login: Login, user_dao: UserDAO = Depends()):
    try:
        db_user = await user_dao.get_user_by_email(login.email)

        if db_user is not None:
            # Verify the user's password
            is_password_valid = await verify_hashed_password(login.password,
                                                             db_user.password)

            if not is_password_valid:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="You have entered a wrong password")

            if is_password_valid:
                # Generate a JWT access token for authentication
                token = sign_jwt(db_user)
                return token
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="You have entered a wrong password")
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found in the database")

@router.get("/users/")
async def get_all_users(token: str = Depends(oauth2_scheme), user_dao: UserDAO = Depends()):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        return user_dao.get_all()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid email or password")
