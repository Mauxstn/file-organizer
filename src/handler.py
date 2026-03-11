"""
Handler-Modul des File Organizer.

Enthält die Logik für das Verschieben und Organisieren von Dateien.
"""

import logging
import shutil
from pathlib import Path
from typing import List

from .config import Config


class FileHandler:
    """Handler-Klasse für die Dateiorganisation."""
    
    def __init__(self, config: Config, dry_run: bool = False):
        """
        Initialisiert den FileHandler.
        
        Args:
            config: Konfigurationsobjekt
            dry_run: Wenn True, werden keine Dateien tatsächlich verschoben
        """
        self.config = config
        self.dry_run = dry_run
        self.logger = logging.getLogger(__name__)
    
    def organize_directory(self, directory: Path) -> None:
        """
        Organisiert alle Dateien in einem Verzeichnis.
        
        Args:
            directory: Zu organisierendes Verzeichnis
        """
        if not directory.exists():
            self.logger.error(f"Verzeichnis existiert nicht: {directory}")
            return
        
        if not directory.is_dir():
            self.logger.error(f"Pfad ist kein Verzeichnis: {directory}")
            return
        
        self.logger.info(f"Starte Organisation von: {directory}")
        
        # Alle Dateien im Verzeichnis durchgehen
        for file_path in directory.iterdir():
            if file_path.is_file():
                self._organize_file(file_path, directory)
        
        self.logger.info("Organisation abgeschlossen")
    
    def _organize_file(self, file_path: Path, base_dir: Path) -> None:
        """
        Organisiert eine einzelne Datei.
        
        Args:
            file_path: Zu organisierende Datei
            base_dir: Basisverzeichnis für die Organisation
        """
        try:
            # Systemdateien und versteckte Dateien überspringen
            if file_path.name.startswith('.'):
                self.logger.debug(f"Überspringe versteckte Datei: {file_path}")
                return
            
            # Zielordner ermitteln
            folder_name = self.config.get_folder_for_file(file_path)
            target_path = self.config.get_target_path(file_path, base_dir)
            
            # Zielverzeichnis erstellen
            target_dir = target_path.parent
            if not self.dry_run:
                target_dir.mkdir(exist_ok=True)
            
            # Datei verschieben
            if self.dry_run:
                self.logger.info(f"[DRY-RUN] Würde verschieben: {file_path} -> {target_path}")
            else:
                shutil.move(str(file_path), str(target_path))
                self.logger.info(f"Verschoben: {file_path.name} -> {folder_name}/{target_path.name}")
        
        except Exception as e:
            self.logger.error(f"Fehler beim Organisieren von {file_path}: {e}")
    
    def get_organization_preview(self, directory: Path) -> List[dict]:
        """
        Erstellt eine Vorschau der bevorstehenden Organisation.
        
        Args:
            directory: Zu analysierendes Verzeichnis
            
        Returns:
            Liste von Dictionaries mit Quell- und Zielpfaden
        """
        preview = []
        
        if not directory.exists() or not directory.is_dir():
            return preview
        
        for file_path in directory.iterdir():
            if file_path.is_file() and not file_path.name.startswith('.'):
                target_path = self.config.get_target_path(file_path, directory)
                folder_name = self.config.get_folder_for_file(file_path)
                
                preview.append({
                    "source": str(file_path),
                    "target": str(target_path),
                    "folder": folder_name,
                    "action": "move" if file_path != target_path else "keep"
                })
        
        return preview
    
    def create_missing_directories(self, base_dir: Path) -> None:
        """
        Erstellt alle Zielverzeichnisse basierend auf der Konfiguration.
        
        Args:
            base_dir: Basisverzeichnis
        """
        for folder_name in self.config.file_types.keys():
            target_dir = base_dir / self.config.target_directories[folder_name]
            if not self.dry_run:
                target_dir.mkdir(exist_ok=True)
                self.logger.info(f"Verzeichnis erstellt: {target_dir}")
            else:
                self.logger.info(f"[DRY-RUN] Würde erstellen: {target_dir}")
    
    def undo_last_organization(self, base_dir: Path, log_file: Path = None) -> None:
        """
        Macht die letzte Organisation rückgängig (falls Log vorhanden).
        
        Args:
            base_dir: Basisverzeichnis
            log_file: Pfad zur Log-Datei mit Bewegungshistorie
        """
        # TODO: Implementieren basierend auf Log-Datei
        self.logger.warning("Undo-Funktion noch nicht implementiert")
