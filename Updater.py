import os
import requests
import zipfile
from dotenv import load_dotenv
import winshell
from win32com.client import Dispatch

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
            "D:\\SteamLibrary",
            "D:\\Steam",
            "E:\\Steam",
            "F:\\Steam",
        ]
        target_folder = "steamapps\\common\\ELDEN RING\\Game"
        for steam_dir in steam_directories:
            if os.path.exists(steam_dir):                
                target_path = os.path.join(steam_dir, target_folder)
                if os.path.exists(target_path):
                    print(f"Gefunden: {target_path}")
                    return target_path
        print("Der Ordner 'steamapps\\common\\ELDEN RING\\Game' wurde in keinem der Standardverzeichnisse gefunden.")
        return None
    else:
        print("Ungültige Eingabe. Bitte 'y' oder 'n' eingeben.")
        return None

def download_and_extract_file(download_url, filename, extract_to):
    response = requests.get(download_url)
    if response.status_code == 200:
        print(f"Download erfolgreich: {filename}")
        zip_path = os.path.join(extract_to, filename)
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            print(f"Entpackt nach: {extract_to}")
            os.remove(zip_path)  # ZIP löschen nach dem Entpacken
        except zipfile.BadZipFile:
            print("Fehler: Ungültige ZIP-Datei")
    else:
        print(f"Fehler beim Download: {response.status_code}")

def update_settings_ini(ini_path):
    if not os.path.isfile(ini_path):
        print(f"Datei nicht gefunden: {ini_path}")
        return

    print("Bitte neues Passwort eingeben:")
    new_password = input().strip()

    updated_lines = []
    with open(ini_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith("cooppassword ="):
                updated_lines.append(f"cooppassword = {new_password}\n")
            else:
                updated_lines.append(line)

    with open(ini_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

    print("Passwort erfolgreich aktualisiert.")

def create_shortcut_to_launcher(launcher_path):
    if not os.path.isfile(launcher_path):
        print(f"Datei nicht gefunden: {launcher_path}")
        return

    desktop = winshell.desktop()
    shortcut_path = os.path.join(desktop, "Elden Ring Coopn.lnk")

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = launcher_path
    shortcut.WorkingDirectory = os.path.dirname(launcher_path)
    shortcut.IconLocation = launcher_path  # Optional: Icon von .exe
    shortcut.Save()

    print(f"Verknüpfung erstellt: {shortcut_path}")

if __name__ == "__main__":
    target_dir = determine_target_directory()
    if target_dir:
        filename = "seamless-coop.zip"
        server_url = os.getenv('SERVER_URL')
        token = os.getenv('TOKEN')
        if not server_url or not token:
            print("Fehler: SERVER_URL oder TOKEN nicht in .env gefunden.")
        else:
            download_url = f"{server_url}?token={token}&file={filename}"
            download_and_extract_file(download_url, filename, target_dir)
        settings_path = os.path.join(target_dir, "SeamlessCoop", "ersc_settings.ini")
        update_settings_ini(settings_path)
        launcher_path = os.path.join(target_dir, "ersc_launcher.exe")
        create_shortcut_to_launcher(launcher_path)


