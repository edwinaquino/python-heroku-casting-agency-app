# [OK] PYCODESTYLE COMPLETED
import os
import socket
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# DATABASE SETUP AND SECRET KEY

DATABASE_URL = os.environ.get("DATABASE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")
ASSISTANT_TOKEN = os.environ.get("ASSISTANT_TOKEN")
PRODUCER_TOKEN = os.environ.get("PRODUCER_TOKEN")
DIRECTOR_TOKEN = os.environ.get("DIRECTOR_TOKEN")

# print(DIRECTOR_TOKEN)
# GET JWT TOKENS FROM .env file
# array elements must match the array elements use din test_app.py
bearer_tokens = {
    "casting_assistant": "Bearer " + ASSISTANT_TOKEN + "",
    "casting_producer": "Bearer " + PRODUCER_TOKEN + "",
    "casting_director": "Bearer " + DIRECTOR_TOKEN + "",
}

# DETERMINE IF APP IS RUNNING REMOTELY IN HEROKU OR LOCALLY
DOMAIN_NAME = socket.getfqdn()
if "heroku.com" in DOMAIN_NAME:
    APP_ENV = "remote"
    database_path = os.environ.get('HORUKO_DATABASE_URL')
else:
    APP_ENV = "local"
    database_path = os.environ.get('DATABASE_URL')
