#!/usr/bin/env python3
"""
Hauptmodul des File Organizer.

Startpunkt des Programms, das die Verzeichnisüberwachung initialisiert
und die Dateiorganisation koordiniert.
"""

import argparse
import logging
import sys
import os
from pathlib import Path

from .config import Config
from .handler import FileHandler
from .watcher import FileWatcher
from .service import (install_windows_service, uninstall_windows_service, 
                     start_windows_service, stop_windows_service, get_service_status)
from .tray import run_tray_app
from .autostart import (create_file_organizer_autostart, remove_file_organizer_autostart, 
                        get_autostart_status)


def setup_logging(log_level: str = "INFO", console_output: bool = True) -> None:
    """Konfiguriert das Logging-System."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    handlers = [
        logging.FileHandler(log_dir / "file_organizer.log")
    ]
    
    if console_output:
        handlers.append(logging.StreamHandler(sys.stdout))
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers
    )


def parse_arguments() -> argparse.Namespace:
    """Verarbeitet Kommandozeilenargumente."""
    parser = argparse.ArgumentParser(
        description="Automatisches Organisieren von Dateien nach Typen"
    )
    parser.add_argument(
        "--watch-dir",
        type=str,
        default=".",
        help="Zu überwachendes Verzeichnis (Standard: aktuelles Verzeichnis)"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Log-Level (Standard: INFO)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulation ohne tatsächliche Dateibewegungen"
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Im Hintergrund laufen (keine Konsolenausgabe)"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Nur einmal organisieren, dann beenden"
    )
    parser.add_argument(
        "--tray",
        action="store_true",
        help="System Tray GUI starten"
    )
    parser.add_argument(
        "--install-service",
        action="store_true",
        help="Windows-Dienst installieren"
    )
    parser.add_argument(
        "--uninstall-service",
        action="store_true",
        help="Windows-Dienst deinstallieren"
    )
    parser.add_argument(
        "--start-service",
        action="store_true",
        help="Windows-Dienst starten"
    )
    parser.add_argument(
        "--stop-service",
        action="store_true",
        help="Windows-Dienst stoppen"
    )
    parser.add_argument(
        "--service-status",
        action="store_true",
        help="Status des Windows-Dienstes anzeigen"
    )
    parser.add_argument(
        "--enable-autostart",
        action="store_true",
        help="Autostart beim Systemstart aktivieren"
    )
    parser.add_argument(
        "--disable-autostart",
        action="store_true",
        help="Autostart beim Systemstart deaktivieren"
    )
    parser.add_argument(
        "--autostart-status",
        action="store_true",
        help="Status des Autostart-Eintrags anzeigen"
    )
    return parser.parse_args()


def main() -> None:
    """Hauptfunktion des Programms."""
    args = parse_arguments()
    
    # Dienst-Operationen behandeln
    if args.install_service:
        success = install_windows_service()
        sys.exit(0 if success else 1)
    
    if args.uninstall_service:
        success = uninstall_windows_service()
        sys.exit(0 if success else 1)
    
    if args.start_service:
        success = start_windows_service()
        sys.exit(0 if success else 1)
    
    if args.stop_service:
        success = stop_windows_service()
        sys.exit(0 if success else 1)
    
    if args.service_status:
        status = get_service_status()
        print(f"Dienst-Status: {status}")
        sys.exit(0)
    
    # Autostart-Operationen behandeln
    if args.enable_autostart:
        success = create_file_organizer_autostart(args.watch_dir, daemon=True)
        print("Autostart aktiviert" if success else "Fehler beim Aktivieren des Autostart")
        sys.exit(0 if success else 1)
    
    if args.disable_autostart:
        success = remove_file_organizer_autostart()
        print("Autostart deaktiviert" if success else "Fehler beim Deaktivieren des Autostart")
        sys.exit(0 if success else 1)
    
    if args.autostart_status:
        status = get_autostart_status()
        print(f"Autostart-Status: {status}")
        sys.exit(0)
    
    # System Tray GUI starten
    if args.tray:
        watch_path = Path(args.watch_dir).resolve()
        run_tray_app(watch_path)
        return
    
    # Logging konfigurieren (im Daemon-Modus ohne Konsolenausgabe)
    setup_logging(args.log_level, console_output=not args.daemon)
    
    logger = logging.getLogger(__name__)
    
    if not args.daemon:
        logger.info("File Organizer wird gestartet")
    
    try:
        config = Config()
        watch_path = Path(args.watch_dir).resolve()
        
        if not args.daemon:
            logger.info(f"Überwache Verzeichnis: {watch_path}")
        
        if args.dry_run:
            logger.info("DRY-RUN Modus: Keine Dateien werden tatsächlich verschoben")
        
        if args.once:
            # Einmalige Organisation
            handler = FileHandler(config, dry_run=args.dry_run)
            handler.organize_directory(watch_path)
            if not args.daemon:
                logger.info("Einmalige Organisation abgeschlossen")
        else:
            # Kontinuierliche Überwachung
            watcher = FileWatcher(watch_path, config, dry_run=args.dry_run)
            
            if args.daemon:
                # Im Daemon-Modus als Hintergrundprozess laufen
                daemonize()
            
            watcher.run_forever()
        
    except KeyboardInterrupt:
        if not args.daemon:
            logger.info("Programm durch Benutzer unterbrochen")
    except Exception as e:
        logger.error(f"Fehler: {e}")
        if not args.daemon:
            sys.exit(1)


def daemonize() -> None:
    """
    Wandelt den Prozess in einen Daemon um (Unix/Linux).
    Für Windows wird der Prozess im Hintergrund weiterlaufen.
    """
    if os.name == 'nt':  # Windows
        # Unter Windows einfach den Prozess weiterlaufen lassen
        # Die Konsolenausgabe wurde bereits deaktiviert
        return
    
    # Unix/Linux Daemon-Implementierung
    try:
        pid = os.fork()
        if pid > 0:
            # Parent Prozess beenden
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"Fork fehlgeschlagen: {e}\n")
        sys.exit(1)
    
    # Umgebungsvariablen setzen
    os.chdir('/')
    os.setsid()
    os.umask(0)
    
    # Zweiten Fork machen
    try:
        pid = os.fork()
        if pid > 0:
            # Parent Prozess beenden
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"Zweiter Fork fehlgeschlagen: {e}\n")
        sys.exit(1)
    
    # Standard-File-Descriptors schließen
    sys.stdout.flush()
    sys.stderr.flush()
    si = open(os.devnull, 'r')
    so = open(os.devnull, 'a+')
    se = open(os.devnull, 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


if __name__ == "__main__":
    main()
