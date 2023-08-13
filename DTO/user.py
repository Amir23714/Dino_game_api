from pydantic import BaseModel


class User(BaseModel):
    telegram_id: str

    username: str

    status: str

    experience: int

    isAdmin: bool
