import os
import requests
import zipfile
from dotenv import load_dotenv
import winshell
from win32com.client import Dispatch

load_dotenv()

def choose_target_directory():
    print("Möchten Sie den Zielordner selbst wählen? (y/n)")
    choice = input().strip().lower()
    if choice == 'y':
        return get_custom_directory()
    elif choice == 'n':
        return find_elden_ring_directory()
    else:
        print("Ungültige Eingabe. Bitte 'y' oder 'n' eingeben.")
        return None

def get_custom_directory():
    print("Bitte geben Sie den Zielordner an:")
    directory = input().strip()
    if os.path.exists(directory):
        return directory
    print(f"Der angegebene Ordner '{directory}' existiert nicht.")
    return None

def find_elden_ring_directory():
    steam_dirs = [
        "C:\\Program Files (x86)\\Steam",
        "C:\\Steam",
        "D:\\SteamLibrary",
        "D:\\Steam",
        "E:\\Steam",
        "F:\\Steam",
    ]
    target_subfolder = "steamapps\\common\\ELDEN RING\\Game"
    for steam_dir in steam_dirs:
        target_path = os.path.join(steam_dir, target_subfolder)
        if os.path.exists(target_path):
            print(f"Gefunden: {target_path}")
            return target_path
    print("Der Ordner 'steamapps\\common\\ELDEN RING\\Game' wurde in keinem der Standardverzeichnisse gefunden.")
    return None

def download_and_extract(download_url, filename, destination):
    response = requests.get(download_url)
    if response.status_code != 200:
        print(f"Fehler beim Download: {response.status_code}")
        return False

    zip_path = os.path.join(destination, filename)
    with open(zip_path, 'wb') as f:
        f.write(response.content)
    print(f"Download erfolgreich: {filename}")

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(destination)
        os.remove(zip_path)
        print(f"Entpackt nach: {destination}")
        return True
    except zipfile.BadZipFile:
        print("Fehler: Ungültige ZIP-Datei")
        return False

def update_ini_password(ini_path):
    if not os.path.isfile(ini_path):
        print(f"Datei nicht gefunden: {ini_path}")
        return

    print("Bitte neues Passwort eingeben:")
    new_password = input().strip()

    with open(ini_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(ini_path, 'w', encoding='utf-8') as f:
        for line in lines:
            if line.strip().startswith("cooppassword ="):
                f.write(f"cooppassword = {new_password}\n")
            else:
                f.write(line)

    print("Passwort erfolgreich aktualisiert.")

def create_desktop_shortcut(target_exe):
    if not os.path.isfile(target_exe):
        print(f"Datei nicht gefunden: {target_exe}")
        return

    desktop = winshell.desktop()
    shortcut_path = os.path.join(desktop, "Elden Ring Coopn.lnk")

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target_exe
    shortcut.WorkingDirectory = os.path.dirname(target_exe)
    shortcut.IconLocation = target_exe
    shortcut.Save()

    print(f"Verknüpfung erstellt: {shortcut_path}")

def main():
    target_dir = choose_target_directory()
    if not target_dir:
        return

    server_url = os.getenv('SERVER_URL')
    token = os.getenv('TOKEN')
    filename = "seamless-coop.zip"

    if not server_url or not token:
        print("Fehler: SERVER_URL oder TOKEN nicht in .env gefunden.")
        return

    download_url = f"{server_url}?token={token}&file={filename}"

    if download_and_extract(download_url, filename, target_dir):
        settings_path = os.path.join(target_dir, "SeamlessCoop", "ersc_settings.ini")
        update_ini_password(settings_path)

        launcher_path = os.path.join(target_dir, "ersc_launcher.exe")
        create_desktop_shortcut(launcher_path)

if __name__ == "__main__":
    main()
