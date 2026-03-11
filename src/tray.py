"""
System Tray GUI für den File Organizer.

Bietet eine einfache GUI zur Steuerung des File Organizers über das System Tray.
"""

import logging
import sys
import threading
from pathlib import Path

try:
    import pystray
    from pystray import MenuItem, Menu
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False

from .config import Config
from .watcher import FileWatcher


class FileOrganizerTray:
    """System Tray GUI für den File Organizer."""
    
    def __init__(self, watch_dir: Path = None):
        """
        Initialisiert die System Tray GUI.
        
        Args:
            watch_dir: Zu überwachendes Verzeichnis
        """
        if not TRAY_AVAILABLE:
            raise ImportError("pystray und PIL sind für die System Tray GUI erforderlich")
        
        self.watch_dir = watch_dir or Path.home() / "Downloads"
        self.config = Config()
        self.watcher = None
        self.is_running = False
        self.logger = self._setup_logging()
        
        # Icon erstellen
        self.icon = self._create_icon()
        
        # Menu erstellen
        self.menu = Menu(
            MenuItem("Starten", self.start_watching, enabled=lambda item: not self.is_running),
            MenuItem("Stoppen", self.stop_watching, enabled=lambda item: self.is_running),
            Menu.SEPARATOR,
            MenuItem("Überwachungsverzeichnis", self.show_watch_dir),
            MenuItem("Konfiguration", self.show_config),
            Menu.SEPARATOR,
            MenuItem("Beenden", self.quit_application)
        )
    
    def _setup_logging(self) -> logging.Logger:
        """Richtet das Logging für die Tray-Anwendung ein."""
        logger = logging.getLogger("FileOrganizerTray")
        logger.setLevel(logging.INFO)
        
        # Log-Verzeichnis erstellen
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # File-Handler
        handler = logging.FileHandler(log_dir / "tray.log")
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def _create_icon(self) -> Image.Image:
        """Erstellt ein einfaches Icon für den System Tray."""
        # Erstellt ein einfaches Ordner-Icon
        image = Image.new('RGB', (64, 64), color='white')
        draw = ImageDraw.Draw(image)
        
        # Ordner-Form zeichnen
        draw.rectangle([8, 20, 56, 48], fill='blue', outline='darkblue')
        draw.rectangle([8, 12, 32, 20], fill='darkblue')
        
        return image
    
    def start_watching(self, icon=None, item=None) -> None:
        """Startet die Dateiüberwachung."""
        if self.is_running:
            return
        
        try:
            self.logger.info("Starte Überwachung aus System Tray")
            self.watcher = FileWatcher(self.watch_dir, self.config, dry_run=False)
            
            # In eigenem Thread starten
            self.watcher_thread = threading.Thread(target=self.watcher.run_forever, daemon=True)
            self.watcher_thread.start()
            
            self.is_running = True
            self.icon.notify("Überwachung gestartet", f"Überwache: {self.watch_dir}")
            
        except Exception as e:
            self.logger.error(f"Fehler beim Starten der Überwachung: {e}")
            self.icon.notify(f"Fehler: {e}", "File Organizer")
    
    def stop_watching(self, icon=None, item=None) -> None:
        """Stoppt die Dateiüberwachung."""
        if not self.is_running:
            return
        
        try:
            self.logger.info("Stoppe Überwachung aus System Tray")
            
            if self.watcher:
                self.watcher.stop_watching()
                self.watcher = None
            
            self.is_running = False
            self.icon.notify("Überwachung gestoppt", "File Organizer")
            
        except Exception as e:
            self.logger.error(f"Fehler beim Stoppen der Überwachung: {e}")
            self.icon.notify(f"Fehler: {e}", "File Organizer")
    
    def show_watch_dir(self, icon=None, item=None) -> None:
        """Zeigt das Überwachungsverzeichnis an."""
        self.icon.notify(f"Überwachungsverzeichnis: {self.watch_dir}", "File Organizer")
    
    def show_config(self, icon=None, item=None) -> None:
        """Zeigt Konfigurationsinformationen an."""
        config_info = f"Dateitypen: {len(self.config.file_types)}\n"
        config_info += f"Zielordner: {len(self.config.target_directories)}"
        
        self.icon.notify(config_info, "Konfiguration")
    
    def quit_application(self, icon=None, item=None) -> None:
        """Beendet die Anwendung."""
        try:
            if self.is_running:
                self.stop_watching()
            
            self.icon.stop()
            
        except Exception as e:
            self.logger.error(f"Fehler beim Beenden: {e}")
    
    def run(self) -> None:
        """Startet die System Tray GUI."""
        self.icon = pystray.Icon(
            "file_organizer",
            self._create_icon(),
            "File Organizer",
            self.menu
        )
        
        self.logger.info("System Tray GUI gestartet")
        self.icon.run()


def create_tray_app(watch_dir: Path = None) -> FileOrganizerTray:
    """
    Erstellt die System Tray Anwendung.
    
    Args:
        watch_dir: Zu überwachendes Verzeichnis
        
    Returns:
        FileOrganizerTray Instanz
    """
    if not TRAY_AVAILABLE:
        print("System Tray nicht verfügbar. Installieren Sie pystray und Pillow:")
        print("pip install pystray Pillow")
        return None
    
    return FileOrganizerTray(watch_dir)


def run_tray_app(watch_dir: Path = None) -> None:
    """
    Startet die System Tray Anwendung.
    
    Args:
        watch_dir: Zu überwachendes Verzeichnis
    """
    tray_app = create_tray_app(watch_dir)
    if tray_app:
        tray_app.run()
