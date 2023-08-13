from fastapi import FastAPI
from routers.user import router as UserRouter
app = FastAPI()

app.include_router(UserRouter, prefix="/api")