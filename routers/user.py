from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.models import get_db

from DTO.user import User as UserDTO
from DTO.default_response import Response as DefaultResponse
from DTO.user_work import UserWork as UserWorkDTO
from services import user as UserServices

from Authentification.authentification import AuthHandler

import threading

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


@router.get("/user", response_model=UserDTO, status_code=200)
async def get_user(access_token: Annotated[str, Depends(Auth.get_apikeyHeader())], db: Session = Depends(get_db)):
    """This endpoint is used to get full user's information"""
    user = Auth.authentificate_user(access_token, db)

    return user


@router.post("/user/work", response_model=DefaultResponse, status_code=200)
async def make_user_work(data: UserWorkDTO, access_token: Annotated[str, Depends(Auth.get_apikeyHeader())],
                         db: Session = Depends(get_db)):
    user = Auth.authentificate_user(access_token, db)

    if user.telegram_id != data.telegram_id:
        raise HTTPException(status_code=403, detail="FORBIDDEN")

    work, ok = UserServices.make_user_work(data.telegram_id, data.working_status, data.finish, db)

    if ok:
        task = threading.Thread(target=UserServices.delete_user_work, args=(data.telegram_id, 200, db))

        task.start()
        return {"status": "OK", "detail": str(work.finish)}

    return {"status": "BAD", "detail": str(work.finish)}

# @router.delete("/user/work", response_model=DefaultResponse, status_code=200)
# async def make_user_work(access_token: Annotated[str, Depends(Auth.get_apikeyHeader())],
#                          db: Session = Depends(get_db)):
#     user = Auth.authentificate_user(access_token, db)
#
#     status = UserServices.delete_user_work(user.telegram_id,db)
#
#     if status:
#         return {"status": "OK", "detail": str(user.experience)}
#
#     return {"status": "BAD", "detail": "User is not working now"}
