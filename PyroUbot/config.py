import os
from dotenv import load_dotenv

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

# URL MongoDB (pastikan sudah di-encode username/password)
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://fatcatVbot:Medan2018@cluster0.wih5v3o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Log channel bot
LOGS_MAKER_UBOT = os.getenv("LOGS_MAKER_UBOT", "-1003047431974")

# User group Telegram
USER_GROUP = os.getenv("USER_GROUP", "@cari_teman_virtual_online")
