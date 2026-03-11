#!/usr/bin/env python3
"""
Minimale Version des File Organizer - nur mit watchdog.
"""

import argparse
import logging
import sys
import time
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False

from .config import Config
from .handler import FileHandler


class MinimalFileHandler(FileSystemEventHandler):
    """Minimaler Event-Handler für Dateisystemereignisse."""
    
    def __init__(self, file_handler: FileHandler, watch_dir: Path):
        super().__init__()
        self.file_handler = file_handler
        self.watch_dir = watch_dir
        self.logger = logging.getLogger(__name__)
    
    def on_created(self, event):
        """Wird aufgerufen, wenn eine Datei erstellt wird."""
        if not event.is_directory:
            file_path = Path(event.src_path)
            # Kurze Wartezeit, damit die Datei vollständig geschrieben wird
            time.sleep(1)
            if file_path.exists():
                self.file_handler._organize_file(file_path, self.watch_dir)


def main_minimal():
    """Minimale Hauptfunktion."""
    if not WATCHDOG_AVAILABLE:
        print("watchdog ist nicht installiert. Installiere mit:")
        print("pip install watchdog")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="Minimaler File Organizer")
    parser.add_argument("--watch-dir", default=".", help="Zu überwachendes Verzeichnis")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], 
                       default="INFO", help="Log-Level")
    parser.add_argument("--daemon", action="store_true", help="Im Hintergrund laufen")
    
    args = parser.parse_args()
    
    # Logging einrichten
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper()),
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout if not args.daemon else None)]
    )
    
    logger = logging.getLogger(__name__)
    
    try:
        config = Config()
        file_handler = FileHandler(config, dry_run=False)
        watch_dir = Path(args.watch_dir).resolve()
        
        logger.info(f"Überwache: {watch_dir}")
        
        # Zuerst vorhandene Dateien organisieren
        file_handler.organize_directory(watch_dir)
        
        # Überwachung starten
        event_handler = MinimalFileHandler(file_handler, watch_dir)
        observer = Observer()
        observer.schedule(event_handler, str(watch_dir), recursive=False)
        observer.start()
        
        if args.daemon:
            print(f"File Organizer läuft im Hintergrund für: {watch_dir}")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stoppe Überwachung...")
            observer.stop()
        
        observer.join()
        
    except Exception as e:
        logger.error(f"Fehler: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main_minimal()
