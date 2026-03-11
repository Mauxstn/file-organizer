"""
Autostart-Modul für den File Organizer.

Ermöglicht die automatische Ausführung beim Systemstart.
"""

import os
import sys
from pathlib import Path


def get_autostart_path() -> Path:
    """
    Gibt den Pfad zum Autostart-Verzeichnis zurück.
    
    Returns:
        Pfad zum Autostart-Verzeichnis
    """
    if os.name == 'nt':  # Windows
        return Path(os.environ['APPDATA']) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Startup'
    else:  # Linux/Unix
        return Path.home() / '.config' / 'autostart'


def create_autostart_entry(name: str, command: str, description: str = "") -> bool:
    """
    Erstellt einen Autostart-Eintrag.
    
    Args:
        name: Name des Eintrags
        command: Auszuführender Befehl
        description: Beschreibung
        
    Returns:
        True bei Erfolg, False bei Fehler
    """
    try:
        autostart_dir = get_autostart_path()
        autostart_dir.mkdir(parents=True, exist_ok=True)
        
        if os.name == 'nt':  # Windows
            # Batch-Datei erstellen
            batch_file = autostart_dir / f"{name}.bat"
            with open(batch_file, 'w', encoding='utf-8') as f:
                f.write(f'@echo off\n{command}\n')
        else:  # Linux/Unix
            # .desktop-Datei erstellen
            desktop_file = autostart_dir / f"{name}.desktop"
            with open(desktop_file, 'w', encoding='utf-8') as f:
                f.write(f'''[Desktop Entry]
Type=Application
Name={name}
Exec={command}
Comment={description}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
''')
        
        return True
    except Exception as e:
        print(f"Fehler beim Erstellen des Autostart-Eintrags: {e}")
        return False


def remove_autostart_entry(name: str) -> bool:
    """
    Entfernt einen Autostart-Eintrag.
    
    Args:
        name: Name des Eintrags
        
    Returns:
        True bei Erfolg, False bei Fehler
    """
    try:
        autostart_dir = get_autostart_path()
        
        if os.name == 'nt':  # Windows
            batch_file = autostart_dir / f"{name}.bat"
            if batch_file.exists():
                batch_file.unlink()
        else:  # Linux/Unix
            desktop_file = autostart_dir / f"{name}.desktop"
            if desktop_file.exists():
                desktop_file.unlink()
        
        return True
    except Exception as e:
        print(f"Fehler beim Entfernen des Autostart-Eintrags: {e}")
        return False


def is_autostart_enabled(name: str) -> bool:
    """
    Prüft, ob ein Autostart-Eintrag existiert.
    
    Args:
        name: Name des Eintrags
        
    Returns:
        True wenn der Eintrag existiert, False sonst
    """
    try:
        autostart_dir = get_autostart_path()
        
        if os.name == 'nt':  # Windows
            batch_file = autostart_dir / f"{name}.bat"
            return batch_file.exists()
        else:  # Linux/Unix
            desktop_file = autostart_dir / f"{name}.desktop"
            return desktop_file.exists()
    except Exception:
        return False


def create_file_organizer_autostart(watch_dir: str = None, daemon: bool = True) -> bool:
    """
    Erstellt einen Autostart-Eintrag für den File Organizer.
    
    Args:
        watch_dir: Zu überwachendes Verzeichnis
        daemon: Ob im Daemon-Modus gestartet werden soll
        
    Returns:
        True bei Erfolg, False bei Fehler
    """
    try:
        # Python-Pfad und Skript-Pfad ermitteln
        python_exe = sys.executable
        script_path = Path(__file__).parent / "main.py"
        
        # Befehl zusammenbauen
        command = f'"{python_exe}" -m src.main'
        
        if watch_dir:
            command += f' --watch-dir "{watch_dir}"'
        
        if daemon:
            command += " --daemon"
        
        # Autostart-Eintrag erstellen
        return create_autostart_entry(
            "FileOrganizer",
            command,
            "Automatisches Organisieren von Dateien"
        )
    except Exception as e:
        print(f"Fehler beim Erstellen des Autostart-Eintrags: {e}")
        return False


def remove_file_organizer_autostart() -> bool:
    """
    Entfernt den Autostart-Eintrag für den File Organizer.
    
    Returns:
        True bei Erfolg, False bei Fehler
    """
    return remove_autostart_entry("FileOrganizer")


def get_autostart_status() -> str:
    """
    Gibt den Status des Autostart-Eintrags zurück.
    
    Returns:
        Status als String
    """
    if is_autostart_enabled("FileOrganizer"):
        return "Autostart ist aktiviert"
    else:
        return "Autostart ist deaktiviert"
