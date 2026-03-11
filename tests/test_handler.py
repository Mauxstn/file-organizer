"""
Tests für das Handler-Modul.
"""

import unittest
import tempfile
import shutil
from pathlib import Path

from src.config import Config
from src.handler import FileHandler


class TestFileHandler(unittest.TestCase):
    """Testklasse für die FileHandler-Klasse."""
    
    def setUp(self):
        """Wird vor jedem Test ausgeführt."""
        self.config = Config()
        self.temp_dir = Path(tempfile.mkdtemp())
        self.handler = FileHandler(self.config, dry_run=True)
    
    def tearDown(self):
        """Wird nach jedem Test ausgeführt."""
        shutil.rmtree(self.temp_dir)
    
    def test_organize_directory_empty(self):
        """Testet die Organisation eines leeren Verzeichnisses."""
        self.handler.organize_directory(self.temp_dir)
        # Sollte keine Fehler werfen
    
    def test_organize_directory_with_files(self):
        """Testet die Organisation mit Testdateien."""
        # Testdateien erstellen
        (self.temp_dir / "test.jpg").touch()
        (self.temp_dir / "document.pdf").touch()
        (self.temp_dir / "movie.mp4").touch()
        
        # Organisation durchführen (dry run)
        self.handler.organize_directory(self.temp_dir)
        
        # Dateien sollten noch vorhanden sein (dry run)
        self.assertTrue((self.temp_dir / "test.jpg").exists())
        self.assertTrue((self.temp_dir / "document.pdf").exists())
        self.assertTrue((self.temp_dir / "movie.mp4").exists())
    
    def test_get_organization_preview(self):
        """Testet die Erstellung einer Organisationsvorschau."""
        # Testdateien erstellen
        (self.temp_dir / "test.jpg").touch()
        (self.temp_dir / "document.pdf").touch()
        
        preview = self.handler.get_organization_preview(self.temp_dir)
        
        self.assertEqual(len(preview), 2)
        self.assertEqual(preview[0]["folder"], "Bilder")
        self.assertEqual(preview[1]["folder"], "Dokumente")
    
    def test_skip_hidden_files(self):
        """Testet dass versteckte Dateien übersprungen werden."""
        # Versteckte Datei erstellen
        (self.temp_dir / ".hidden").touch()
        (self.temp_dir / "normal.txt").touch()
        
        preview = self.handler.get_organization_preview(self.temp_dir)
        
        # Nur die normale Datei sollte in der Vorschau sein
        self.assertEqual(len(preview), 1)
        self.assertEqual(preview[0]["source"], str(self.temp_dir / "normal.txt"))


if __name__ == "__main__":
    unittest.main()
