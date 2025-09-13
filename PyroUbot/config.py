import os
from dotenv import load_dotenv

load_dotenv(".env")

MAX_BOT = int(os.getenv("MAX_BOT", "100"))

DEVS = list(map(int, os.getenv("DEVS", "1815592994").split()))

API_ID = int(os.getenv("API_ID", "25453211"))

API_HASH = os.getenv("API_HASH", "141cef82dd3e88877dab990125721079")

BOT_TOKEN = os.getenv("BOT_TOKEN", "7300174040:AAGnaM3oiGIMWW1peUQWRjo347pTKBZToe8")

OWNER_ID = int(os.getenv("OWNER_ID", "1815592994"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002125842026 -1002053287763 -1002044997044 -1002022625433 -1002050846285 -1002400165299 -1002416419679 -1001473548283").split()))

RMBG_API = os.getenv("RMBG_API", "KsPwpgY1Mncmr98ncrWpwZ22")

MONGO_URL = os.getenv("MONGO_URL = "mongodb+srv://Veluebot:Medan2018@cluster0.daj2n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

LOGS_MAKER_UBOT = os.getenv("LOGS_MAKER_UBOT", "-1003047431974")


USER_GROUP = os.getenv("USER_GROUP", "@cari_teman_virtual_online")
