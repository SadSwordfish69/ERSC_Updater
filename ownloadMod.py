import os
import requests
from tqdm import tqdm
import zipfile
from dotenv import load_dotenv

url = "https://apk.nexusmods.com/"

load_dotenv()
APK_KEY = os.getenv("APK_KEY")
if not APK_KEY:
    raise ValueError("APK_KEY environment variable is not set. Please set it in your .env file.")

def download_ersc(target_dir: str) -> None:
    