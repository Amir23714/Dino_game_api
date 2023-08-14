import fastapi.security
import jwt
from fastapi import HTTPException

from jwt import ExpiredSignatureError
from passlib.context import CryptContext

import settings
from DTO.user import User as UserDTO
from services import user as UserServices


class AuthHandler():
    def get_token(self, user: UserDTO):

        data = {"sub": user.telegram_id, "isAdmin": user.isAdmin}

        encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return encoded_jwt

    def decode_token(self, token: str, db):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

            return payload

        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid access token")

    def authentificate_admin(self, access_token, db):
        payload = self.decode_token(access_token, db)

        tg_id = payload.get("sub")
        isAdmin = payload.get("isAdmin")

        user = UserServices.get_user(tg_id, db)

        if not user or not user.isAdmin or user.isAdmin != isAdmin:
            raise HTTPException(status_code=403, detail="You do not have access")

        return user

    def authentificate_user(self, access_token, db):

        payload = self.decode_token(access_token, db)

        tg_id = payload.get("sub")
        print(tg_id)
        isAdmin = payload.get("isAdmin")

        user = UserServices.get_user(tg_id, db)

        if user is None:
            raise HTTPException(status_code=403, detail="You do not have access")

        return user

    def get_apikeyHeader(self, autoerror=True):
        return fastapi.security.APIKeyHeader(name="Authorization", auto_error=autoerror)
