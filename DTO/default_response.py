from pydantic import BaseModel


class Response(BaseModel):
    status : str
    detail : str