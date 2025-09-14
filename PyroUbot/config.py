import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv(".env")

# Maksimum bot yang berjalan
MAX_BOT = int(os.getenv("MAX_BOT", "100"))

# Daftar developer
DEVS = list(map(int, os.getenv("DEVS", "1815592994").split()))

# Telegram API
API_ID = int(os.getenv("API_ID", "25453211"))
API_HASH = os.getenv("API_HASH", "141cef82dd3e88877dab990125721079")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7300174040:AAGnaM3oiGIMWW1peUQWRjo347pTKBZToe8")

# Owner ID
OWNER_ID = int(os.getenv("OWNER_ID", "1815592994"))

# Daftar chat yang diblacklist
BLACKLIST_CHAT = list(map(int, os.getenv(
    "BLACKLIST_CHAT", 
    "-1002125842026 -1002053287763 -1002044997044 -1002022625433 -1002050846285 -1002400165299 -1002416419679 -1001473548283"
).split()))

# API untuk remove bg
RMBG_API = os.getenv("RMBG_API", "KsPwpgY1Mncmr98ncrWpwZ22")

# MongoDB Credentials
MONGO_USER = os.getenv("MONGO_USER", "fatcatVbot")
MONGO_PASS = os.getenv("MONGO_PASS", "Medan2018")  # encode otomatis
MONGO_DB   = os.getenv("MONGO_DB", "fatcatdb")
MONGO_HOST = os.getenv("MONGO_HOST", "cluster0.wih5v3o.mongodb.net")

# Encode username/password agar aman di URL
MONGO_URL = f"mongodb+srv://{quote_plus(MONGO_USER)}:{quote_plus(MONGO_PASS)}@{MONGO_HOST}/{MONGO_DB}?retryWrites=true&w=majority&appName=Cluster0"

# Log channel bot
LOGS_MAKER_UBOT = os.getenv("LOGS_MAKER_UBOT", "-1002985186376")

# User group Telegram
USER_GROUP = os.getenv("USER_GROUP", "@FatCatMart")
