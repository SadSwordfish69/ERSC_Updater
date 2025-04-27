import os
import shutil
import platform
import winshell

def copy_file_to_dir(source_file, target_dir):
    if not os.path.isfile(source_file):
        raise FileNotFoundError(f"Source file '{source_file}' does not exist.")
    if not os.path.isdir(target_dir):
        raise NotADirectoryError(f"Target directory '{target_dir}' does not exist.")
    
    shutil.copy(source_file, target_dir)

def create_shortcut_to_desktop(target_file):
    if not os.path.isfile(target_file):
        raise FileNotFoundError(f"Target file '{target_file}' does not exist.")
        
    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.isdir(desktop_dir):
        raise NotADirectoryError("Desktop directory does not exist.")
        
    shortcut_name = os.path.splitext(os.path.basename(target_file))[0] + ".lnk"
    shortcut_path = os.path.join(desktop_dir, shortcut_name)
    
    if platform.system() == "Windows":
        with winshell.shortcut(shortcut_path) as shortcut:
            shortcut.path = target_file
            shortcut.working_directory = os.path.dirname(target_file)
            shortcut.description = f"Shortcut to {os.path.basename(target_file)}"
    else:
        raise NotImplementedError("Shortcut creation is only supported on Windows.")