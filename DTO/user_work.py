from pydantic import BaseModel


class UserWork(BaseModel):
    telegram_id: str
    working_status: str
    finish: int
