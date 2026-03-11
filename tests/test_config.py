"""
Tests für das Konfigurationsmodul.
"""

import unittest
from pathlib import Path

from src.config import Config


class TestConfig(unittest.TestCase):
    """Testklasse für die Config-Klasse."""
    
    def setUp(self):
        """Wird vor jedem Test ausgeführt."""
        self.config = Config()
    
    def test_get_folder_for_file(self):
        """Testet die Ordnererkennung für verschiedene Dateitypen."""
        # Bilder
        self.assertEqual(self.config.get_folder_for_file(Path("test.jpg")), "Bilder")
        self.assertEqual(self.config.get_folder_for_file(Path("photo.PNG")), "Bilder")
        
        # Dokumente
        self.assertEqual(self.config.get_folder_for_file(Path("document.pdf")), "Dokumente")
        self.assertEqual(self.config.get_folder_for_file(Path("notes.txt")), "Dokumente")
        
        # Videos
        self.assertEqual(self.config.get_folder_for_file(Path("movie.mp4")), "Videos")
        
        # Unbekannter Typ
        self.assertEqual(self.config.get_folder_for_file(Path("unknown.xyz")), "Sonstiges")
    
    def test_get_target_path(self):
        """Testet die Erstellung von Zielpfaden."""
        base_dir = Path("/test")
        source_file = Path("test.jpg")
        
        target_path = self.config.get_target_path(source_file, base_dir)
        expected = base_dir / "bilder" / "test.jpg"
        self.assertEqual(target_path, expected)
    
    def test_add_file_type(self):
        """Testet das Hinzufügen neuer Dateitypen."""
        self.config.add_file_type("TestTyp", [".test", ".example"])
        
        self.assertIn("TestTyp", self.config.file_types)
        self.assertEqual(self.config.get_folder_for_file(Path("file.test")), "TestTyp")
    
    def test_remove_file_type(self):
        """Testet das Entfernen von Dateitypen."""
        self.config.remove_file_type("Bilder")
        
        self.assertNotIn("Bilder", self.config.file_types)
        self.assertEqual(self.config.get_folder_for_file(Path("test.jpg")), "Sonstiges")


if __name__ == "__main__":
    unittest.main()
