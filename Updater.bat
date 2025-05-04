@echo off

set "TARGET_DIR=%ProgramFiles(x86)%\Steam\steamapps\common\ELDEN RING\Game"
set "SOURCE_DIR_FOLDER=%~dp0UpdaterContent\SeamlessCoop"
set "SOURCE_DIR_EXE=%~dp0UpdaterContent\ersc_launcher.exe"
set "DESKTOP_PATH=C:\Users\Public\Desktop"
set "SHORTCUT_PATH=%DESKTOP_PATH%\Elden Ring Coop.lnk"
set "GAME_EXE=%TARGET_DIR%\ersc_launcher.exe"

if not exist "%TARGET_DIR%" (
    echo Fehler: Zielverzeichnis existiert nicht.
    timeout /t 2 >nul
    exit /b 1
)

xcopy /Y /I /E "%SOURCE_DIR_EXE%" "%TARGET_DIR%"
xcopy /Y /I /E "%SOURCE_DIR_FOLDER%" "%TARGET_DIR%\SeamlessCoop"

rem Verknüpfung erstellen per PowerShell
powershell -NoProfile -Command ^
    $WshShell = New-Object -ComObject WScript.Shell; ^
    $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); ^
    $Shortcut.TargetPath = '%GAME_EXE%'; ^
    $Shortcut.IconLocation = '%GAME_EXE%'; ^
    $Shortcut.WorkingDirectory = '%TARGET_DIR%'; ^
    $Shortcut.Save()

echo Verknüpfung wurde auf dem Desktop erstellt.
timeout /t 2 >nul
exit