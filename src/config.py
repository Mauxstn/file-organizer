"""
Konfigurationsmodul des File Organizer.

Definiert Dateitypen, Zielordner und andere Konfigurationsoptionen.
"""

from pathlib import Path
from typing import Dict, List


class Config:
    """Konfigurationsklasse für den File Organizer."""
    
    def __init__(self):
        """Initialisiert die Standardkonfiguration."""
        self.file_types = self._get_default_file_types()
        self.target_directories = self._get_default_directories()
    
    def _get_default_file_types(self) -> Dict[str, List[str]]:
        """
        Gibt die Standard-Dateitypzuordnungen zurück.
        
        Returns:
            Dict mit Ordnernamen als Schlüssel und Dateiendungen als Listen.
        """
        return {
            "Bilder": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg"],
            "Dokumente": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".pages"],
            "Tabellen": [".xls", ".xlsx", ".csv", ".ods", ".numbers"],
            "Präsentationen": [".ppt", ".pptx", ".odp", ".key"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
            "Archiv": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".go", ".rs"],
            "Ausführbare": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"],
            "E-Books": [".epub", ".mobi", ".azw", ".azw3"],
            "3D-Modelle": [".blend", ".obj", ".fbx", ".dae", ".3ds", ".stl", ".ply", ".x3d"]
        }
    
    def _get_default_directories(self) -> Dict[str, str]:
        """
        Gibt die Standard-Zielverzeichnisse zurück.
        
        Returns:
            Dict mit Ordnernamen als Schlüssel und Pfadnamen als Werte.
        """
        return {
            folder_name: folder_name.lower() 
            for folder_name in self.file_types.keys()
        }
    
    def get_folder_for_file(self, file_path: Path) -> str:
        """
        Ermittelt den Zielordner für eine Datei basierend auf ihrer Endung.
        
        Args:
            file_path: Pfad zur Datei
            
        Returns:
            Name des Zielordners oder "Sonstiges" wenn kein Typ passt
        """
        file_extension = file_path.suffix.lower()
        
        for folder_name, extensions in self.file_types.items():
            if file_extension in extensions:
                return folder_name
        
        return "Sonstiges"
    
    def get_target_path(self, source_path: Path, base_dir: Path) -> Path:
        """
        Erstellt den vollständigen Zielpfad für eine Datei.
        
        Args:
            source_path: Ursprünglicher Dateipfad
            base_dir: Basisverzeichnis für die Organisation
            
        Returns:
            Vollständiger Zielpfad
        """
        folder_name = self.get_folder_for_file(source_path)
        target_dir = base_dir / self.target_directories.get(folder_name, folder_name.lower())
        
        # Dateinamen beibehalten, bei Konflikten Nummer hinzufügen
        target_path = target_dir / source_path.name
        counter = 1
        
        while target_path.exists():
            stem = source_path.stem
            suffix = source_path.suffix
            target_path = target_dir / f"{stem}_{counter}{suffix}"
            counter += 1
        
        return target_path
    
    def add_file_type(self, folder_name: str, extensions: List[str]) -> None:
        """
        Fügt einen neuen Dateityp hinzu.
        
        Args:
            folder_name: Name des Zielordners
            extensions: Liste der Dateiendungen
        """
        self.file_types[folder_name] = [ext.lower() for ext in extensions]
        self.target_directories[folder_name] = folder_name.lower()
    
    def remove_file_type(self, folder_name: str) -> None:
        """
        Entfernt einen Dateityp aus der Konfiguration.
        
        Args:
            folder_name: Name des zu entfernenden Ordners
        """
        self.file_types.pop(folder_name, None)
        self.target_directories.pop(folder_name, None)
