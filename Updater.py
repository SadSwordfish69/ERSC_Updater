from dotenv import load_dotenv
import os
import requests
import zipfile
import platform
from pathlib import Path
from tqdm import tqdm

load_dotenv()
API_KEY = os.getenv("NEXUS_API_KEY")
GAME_DOMAIN = "eldenring"
MOD_ID = 510
HEADERS = {"apikey": API_KEY, "Accept": "application/json"}

def get_downloads_folder():
    if platform.system() == "Windows":
        return Path(os.environ["USERPROFILE"]) / "Downloads"
    else:
        return Path.home() / "Downloads"

def fetch_latest_file_info():
    url = f"https://api.nexusmods.com/v1/games/{GAME_DOMAIN}/mods/{MOD_ID}/files.json"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        raise Exception("Fehler beim Abrufen der Mod-Dateien.")
    files = r.json().get("files", [])
    main_files = [f for f in files if f.get("category_name") == "MAIN"]
    if not main_files:
        raise Exception("Keine Hauptdatei gefunden.")
    return sorted(main_files, key=lambda x: x["file_id"], reverse=True)[0]  # neueste Datei

def fetch_download_url(file_id):
    url = f"https://api.nexusmods.com/v1/games/{GAME_DOMAIN}/mods/{MOD_ID}/files/{file_id}/download_link.json"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        raise Exception("Fehler beim Abrufen des Download-Links.")
    links = r.json()
    return links[0]["URI"]  # erster Mirror-Link

def download_file(url, target_path):
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        raise Exception("Download fehlgeschlagen.")
    total = int(r.headers.get('content-length', 0))
    with open(target_path, 'wb') as file, tqdm(
        desc=target_path.name,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in r.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def main():
    try:
        print("Mod wird gesucht...")
        file_info = fetch_latest_file_info()
        file_id = file_info["file_id"]
        file_name = file_info["file_name"]
        print(f"Gefunden: {file_name}")

        print("🔗 Download-Link wird geholt...")
        download_url = fetch_download_url(file_id)

        downloads_dir = get_downloads_folder()
        zip_path = downloads_dir / file_name
        print(f"Lade herunter nach: {zip_path}")
        download_file(download_url, zip_path)

        print("Entpacke ZIP...")
        unzip_file(zip_path, downloads_dir)
        print("Fertig! Mod ist im Downloads-Ordner entpackt.")
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    main()
