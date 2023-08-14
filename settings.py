from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", default="secret_key")
ALGORITHM = os.getenv("ALGORITHM", default="HS256")
TOKEN = os.getenv("TOKEN", default="6509073218:AAG2HIp0rMMXFGZTnw7A6Ie-f-QYDnR2bto")

