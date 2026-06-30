import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    APP_NAME=os.getenv("APP_NAME")
    APP_VERSION=os.getenv("APP_VERSION")
    APP_DESCRIPTION=os.getenv("APP_DESCRIPTION")
    DEBUG=os.getenv("DEBUG")

settings=Settings()