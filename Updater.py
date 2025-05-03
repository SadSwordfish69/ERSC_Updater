import os
import requests
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv()

def determine_target_directory():
    print("Möchten Sie den Zielordner selbst wählen? (y/n)")
    choice = input().strip().lower()
    if choice == 'y':
        print("Bitte geben Sie den Zielordner an:")
        target_directory = input().strip()
        if not os.path.exists(target_directory):
            print(f"Der angegebene Ordner '{target_directory}' existiert nicht.")
            return None
        return target_directory
    elif choice == 'n':
        # Mögliche Standard-Installationsverzeichnisse von Steam
        steam_directories = [
            "C:\\Program Files (x86)\\Steam",
            "C:\\Steam",
            "D:\\Program Files (x86)\\Steam",
            "D:\\Steam",
            "E:\\Steam",
            "F:\\Steam",
            # Weitere Laufwerke und Verzeichnisse können hier hinzugefügt werden
        ]
        # Zielordner, nach dem gesucht werden soll
        target_folder = "steamapps\\common\\ELDEN RING\\Game"

        for steam_dir in steam_directories:
            # Überprüfen, ob das Steam-Verzeichnis existiert
            if os.path.exists(steam_dir):
                # Pfad zum "steamapps" Ordner
                steamapps_path = os.path.join(steam_dir, "steamapps")
                if os.path.exists(steamapps_path):
                    # Überprüfen, ob der Zielordner vorhanden ist
                    target_path = os.path.join(steamapps_path, target_folder)
                    if os.path.exists(target_path):
                        print(f"Gefunden: {target_path}")
                        return target_path
        print("Der Ordner 'steamapps\\common\\ELDEN RING\\Game' wurde in keinem der Standard-Installationsverzeichnisse gefunden.")
        return None
    else:
        print("Ungültige Eingabe. Bitte 'y' oder 'n' eingeben.")
        return None

# Datei herunterladen
def download_file(url, filename):

    # Die URL und das Token aus der .env-Datei
    server_url = os.getenv('SERVER_URL')
    token = os.getenv('TOKEN')

    # Der Dateiname, den du herunterladen möchtest
    filename = "seamless-coop.zip"

    # URL zum Download erstellen
    download_url = f"{server_url}?token={token}&file={filename}"

    response = requests.get(url)

    if response.status_code == 200:
        print(f"Download erfolgreich: {filename}")
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Fehler beim Download: {response.status_code}")

# Hauptlogik ausführen
if __name__ == "__main__":
    download_file(download_url, filename)
