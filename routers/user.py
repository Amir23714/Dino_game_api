from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.models import get_db

from DTO.user import User as UserDTO
from DTO.default_response import Response as DefaultResponse
from services import user as UserServices

from Authentification.authentification import AuthHandler

router = APIRouter()

Auth = AuthHandler()


@router.post("/user", response_model=DefaultResponse, status_code=200)
async def register(data: UserDTO = None, db: Session = Depends(get_db)):
    """Endpoint for user registration"""
    if UserServices.get_user(data.telegram_id, db) is not None:
        raise HTTPException(status_code=400, detail="User with this telegram_id already exists")

    user = UserServices.create_user(data, db)

    token = Auth.get_token(user)

    return {"status": "OK", "detail": str(token)}


@router.get("", response_model=UserDTO, status_code=200)
async def get_user(access_token: Annotated[str, Depends(Auth.get_apikeyHeader())], db: Session = Depends(get_db)):
    """This endpoint is used to get full user's information"""
    user = Auth.authentificate_user(access_token, db)

    return user
