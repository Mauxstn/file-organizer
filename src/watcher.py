"""
Watcher-Modul des File Organizer.

Implementiert die Überwachung von Dateisystemereignissen mit watchdog.
"""

import logging
import time
from pathlib import Path
from typing import Optional

from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

from .config import Config
from .handler import FileHandler


class FileOrganizerEventHandler(FileSystemEventHandler):
    """Event-Handler für Dateisystemereignisse."""
    
    def __init__(self, handler: FileHandler, watch_dir: Path):
        """
        Initialisiert den Event-Handler.
        
        Args:
            handler: FileHandler für die Dateiorganisation
            watch_dir: Zu überwachendes Verzeichnis
        """
        super().__init__()
        self.handler = handler
        self.watch_dir = watch_dir
        self.logger = logging.getLogger(__name__)
        self.debounce_time = 1.0  # Sekunden
        self.pending_files = {}
    
    def on_created(self, event: FileSystemEvent) -> None:
        """Wird aufgerufen, wenn eine Datei erstellt wird."""
        if not event.is_directory:
            self._schedule_organization(Path(event.src_path))
    
    def on_moved(self, event: FileSystemEvent) -> None:
        """Wird aufgerufen, wenn eine Datei verschoben wird."""
        if not event.is_directory:
            self._schedule_organization(Path(event.dest_path))
    
    def _schedule_organization(self, file_path: Path) -> None:
        """
        Plant die Organisation einer Datei mit Verzögerung (Debouncing).
        
        Args:
            file_path: Zu organisierende Datei
        """
        # Überspringen, wenn die Datei im Zielverzeichnis liegt
        if self._is_in_target_directory(file_path):
            return
        
        # Überspringen von versteckten und temporären Dateien
        if file_path.name.startswith('.') or file_path.name.startswith('~'):
            return
        
        # Datei zur Warteschlange hinzufügen
        self.pending_files[str(file_path)] = time.time()
        
        # Kurze Verzögerung, um sicherzustellen, dass die Datei vollständig geschrieben ist
        time.sleep(self.debounce_time)
        
        # Prüfen, ob die Datei noch existiert und in der Warteschlange ist
        if str(file_path) in self.pending_files:
            if file_path.exists():
                self._organize_file_safely(file_path)
            del self.pending_files[str(file_path)]
    
    def _is_in_target_directory(self, file_path: Path) -> bool:
        """
        Prüft, ob eine Datei bereits in einem Zielverzeichnis liegt.
        
        Args:
            file_path: Zu prüfende Datei
            
        Returns:
            True, wenn die Datei in einem Zielverzeichnis liegt
        """
        parent_name = file_path.parent.name.lower()
        target_dirs = set(self.handler.config.target_directories.values())
        return parent_name in target_dirs
    
    def _organize_file_safely(self, file_path: Path) -> None:
        """
        Organisiert eine Datei sicher mit Fehlerbehandlung.
        
        Args:
            file_path: Zu organisierende Datei
        """
        try:
            # Warten, bis die Datei vollständig geschrieben ist
            self._wait_for_file_complete(file_path)
            
            # Datei organisieren
            self.handler._organize_file(file_path, self.watch_dir)
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Organisation von {file_path}: {e}")
    
    def _wait_for_file_complete(self, file_path: Path, timeout: int = 10) -> None:
        """
        Wartet, bis eine Datei vollständig geschrieben ist.
        
        Args:
            file_path: Zu überwachende Datei
            timeout: Maximale Wartezeit in Sekunden
        """
        start_time = time.time()
        last_size = -1
        
        while time.time() - start_time < timeout:
            try:
                current_size = file_path.stat().st_size
                
                if current_size == last_size and current_size > 0:
                    # Dateigröße hat sich nicht geändert, wahrscheinlich vollständig
                    time.sleep(0.5)  # Zusätzliche kurze Wartezeit
                    return
                
                last_size = current_size
                time.sleep(0.5)
                
            except (OSError, FileNotFoundError):
                # Datei existiert noch nicht oder ist nicht zugreifbar
                time.sleep(0.5)
        
        self.logger.warning(f"Timeout beim Warten auf vervollständigte Datei: {file_path}")


class FileWatcher:
    """Hauptklasse für die Dateisystemüberwachung."""
    
    def __init__(self, watch_dir: Path, config: Config, dry_run: bool = False):
        """
        Initialisiert den FileWatcher.
        
        Args:
            watch_dir: Zu überwachendes Verzeichnis
            config: Konfigurationsobjekt
            dry_run: Wenn True, werden keine Dateien tatsächlich verschoben
        """
        self.watch_dir = watch_dir.resolve()
        self.config = config
        self.dry_run = dry_run
        self.observer = Observer()
        self.handler = FileHandler(config, dry_run)
        self.event_handler = FileOrganizerEventHandler(self.handler, self.watch_dir)
        self.logger = logging.getLogger(__name__)
    
    def start_watching(self) -> None:
        """Startet die Überwachung des Verzeichnisses."""
        if not self.watch_dir.exists():
            raise FileNotFoundError(f"Verzeichnis existiert nicht: {self.watch_dir}")
        
        if not self.watch_dir.is_dir():
            raise NotADirectoryError(f"Pfad ist kein Verzeichnis: {self.watch_dir}")
        
        # Observer starten
        self.observer.schedule(
            self.event_handler,
            str(self.watch_dir),
            recursive=False  # Nur das Hauptverzeichnis überwachen
        )
        
        self.observer.start()
        self.logger.info(f"Überwachung gestartet für: {self.watch_dir}")
        
        # Zuerst vorhandene Dateien organisieren
        self.logger.info("Organisiere vorhandene Dateien...")
        self.handler.organize_directory(self.watch_dir)
    
    def stop_watching(self) -> None:
        """Stoppt die Überwachung."""
        if self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
            self.logger.info("Überwachung gestoppt")
    
    def run_forever(self) -> None:
        """Lässt den Watcher im Hintergrund laufen."""
        try:
            self.start_watching()
            
            # Haupt-Loop
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.logger.info("Überwachung durch Benutzer unterbrochen")
        except Exception as e:
            self.logger.error(f"Fehler in der Überwachung: {e}")
        finally:
            self.stop_watching()
    
    def is_running(self) -> bool:
        """Prüft, ob die Überwachung aktiv ist."""
        return self.observer.is_alive()
