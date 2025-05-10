from dotenv import load_dotenv
import os
load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PORT = os.environ.get("DB_PORT")
VITE_IP_HOST = os.environ.get("VITE_IP_HOST")
VITE_API_PORT = os.environ.get("VITE_API_PORT")
