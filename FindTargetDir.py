import os
import string

def find_elden_ring():
    # Standard Steam-Bibliothekspfad
    steam_path = "Program Files (x86)\\Steam\\steamapps\\common"
    game_folder = "ELDEN RING"

    # Alle Laufwerke (z.B. C:, D:, etc.) auf dem Windows-System durchsuchen
    for drive in string.ascii_uppercase:
        drive_path = f"{drive}:\\"

        # Prüfen, ob das Laufwerk existiert
        if os.path.exists(drive_path):
            # Vollständiger Pfad zur Steam-Bibliothek auf diesem Laufwerk
            search_path = os.path.join(drive_path, steam_path)
            
            # Prüfen, ob der "common"-Ordner existiert
            if os.path.exists(search_path):
                # Prüfen, ob der "ELDEN RING"-Ordner existiert
                elden_ring_path = os.path.join(search_path, game_folder)
                if os.path.isdir(elden_ring_path):
                    return elden_ring_path

    # Falls der Ordner nicht gefunden wurde
    return None

# Aufruf der Funktion und Ausgabe
elden_ring = find_elden_ring()
if elden_ring:
    print(f"ELDEN RING wurde gefunden in: {elden_ring}")
else:
    print("ELDEN RING wurde nicht gefunden.")
