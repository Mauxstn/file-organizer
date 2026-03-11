"""
Service-Modul für Windows-Dienst-Integration.

Ermöglicht die Installation und Ausführung als Windows-Dienst.
"""

import logging
import sys
import time
from pathlib import Path

try:
    import win32serviceutil
    import win32service
    import win32event
    import servicemanager
    WINDOWS_SERVICE_AVAILABLE = True
except ImportError:
    WINDOWS_SERVICE_AVAILABLE = False

from .config import Config
from .watcher import FileWatcher


if WINDOWS_SERVICE_AVAILABLE:
    class FileOrganizerWindowsService(win32serviceutil.ServiceFramework):
        """Windows-Dienst für den File Organizer."""
        
        _svc_name_ = "FileOrganizer"
        _svc_display_name_ = "File Organizer Service"
        _svc_description_ = "Automatisches Organisieren von Dateien nach Typen"
        
        def __init__(self, args):
            """Initialisiert den Windows-Dienst."""
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            self.is_alive = True
            self.watcher = None
            self.logger = self._setup_service_logging()
        
        def _setup_service_logging(self) -> logging.Logger:
            """Richtet das Logging für den Dienst ein."""
            logger = logging.getLogger("FileOrganizerService")
            logger.setLevel(logging.INFO)
            
            # Log-Verzeichnis erstellen
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            # File-Handler
            handler = logging.FileHandler(log_dir / "service.log")
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
            return logger
        
        def SvcStop(self) -> None:
            """Wird aufgerufen, wenn der Dienst gestoppt wird."""
            self.logger.info("File Organizer Dienst wird gestoppt")
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            win32event.SetEvent(self.hWaitStop)
            self.is_alive = False
            
            if self.watcher:
                self.watcher.stop_watching()
        
        def SvcDoRun(self) -> None:
            """Hauptmethode des Dienstes."""
            try:
                self.logger.info("File Organizer Dienst wird gestartet")
                servicemanager.LogMsg(
                    servicemanager.EVENTLOG_INFORMATION_TYPE,
                    servicemanager.PYS_SERVICE_STARTED,
                    (self._svc_name_, '')
                )
                
                # Konfiguration laden
                config = Config()
                
                # Standard-Überwachungsverzeichnis (Downloads)
                watch_dir = Path.home() / "Downloads"
                if not watch_dir.exists():
                    watch_dir = Path.cwd()
                
                self.logger.info(f"Überwache Verzeichnis: {watch_dir}")
                
                # Watcher starten
                self.watcher = FileWatcher(watch_dir, config, dry_run=False)
                self.watcher.start_watching()
                
                # Haupt-Loop
                while self.is_alive:
                    # Warten auf Stop-Ereignis oder Timeout
                    win32event.WaitForSingleObject(self.hWaitStop, 1000)
                
            except Exception as e:
                self.logger.error(f"Fehler im Dienst: {e}")
                servicemanager.LogErrorMsg(f"Dienst-Fehler: {e}")


def install_windows_service() -> bool:
    """
    Installiert den Windows-Dienst.
    
    Returns:
        True bei Erfolg, False bei Fehler
    """
    if not WINDOWS_SERVICE_AVAILABLE:
        print("Windows-Dienst-Module nicht verfügbar. Installieren Sie pywin32.")
        return False
    
    try:
        win32serviceutil.InstallService(
            FileOrganizerWindowsService._svc_name_,
            FileOrganizerWindowsService._svc_display_name_,
            FileOrganizerWindowsService._svc_description_,
            startType=win32service.SERVICE_AUTO_START
        )
        print(f"Dienst '{FileOrganizerWindowsService._svc_display_name_}' erfolgreich installiert")
        return True
    except Exception as e:
        print(f"Fehler bei der Installation des Dienstes: {e}")
        return False


def uninstall_windows_service() -> bool:
    """
    Deinstalliert den Windows-Dienst.
    
    Returns:
        True bei Erfolg, False bei Fehler
    """
    if not WINDOWS_SERVICE_AVAILABLE:
        print("Windows-Dienst-Module nicht verfügbar.")
        return False
    
    try:
        win32serviceutil.RemoveService(FileOrganizerWindowsService._svc_name_)
        print(f"Dienst '{FileOrganizerWindowsService._svc_display_name_}' erfolgreich deinstalliert")
        return True
    except Exception as e:
        print(f"Fehler bei der Deinstallation des Dienstes: {e}")
        return False


def start_windows_service() -> bool:
    """
    Startet den Windows-Dienst.
    
    Returns:
        True bei Erfolg, False bei Fehler
    """
    if not WINDOWS_SERVICE_AVAILABLE:
        print("Windows-Dienst-Module nicht verfügbar.")
        return False
    
    try:
        win32serviceutil.StartService(FileOrganizerWindowsService._svc_name_)
        print("Dienst erfolgreich gestartet")
        return True
    except Exception as e:
        print(f"Fehler beim Starten des Dienstes: {e}")
        return False


def stop_windows_service() -> bool:
    """
    Stoppt den Windows-Dienst.
    
    Returns:
        True bei Erfolg, False bei Fehler
    """
    if not WINDOWS_SERVICE_AVAILABLE:
        print("Windows-Dienst-Module nicht verfügbar.")
        return False
    
    try:
        win32serviceutil.StopService(FileOrganizerWindowsService._svc_name_)
        print("Dienst erfolgreich gestoppt")
        return True
    except Exception as e:
        print(f"Fehler beim Stoppen des Dienstes: {e}")
        return False


def get_service_status() -> str:
    """
    Gibt den Status des Windows-Dienstes zurück.
    
    Returns:
        Status als String
    """
    if not WINDOWS_SERVICE_AVAILABLE:
        return "Windows-Dienst-Module nicht verfügbar"
    
    try:
        status = win32serviceutil.QueryServiceStatus(FileOrganizerWindowsService._svc_name_)
        status_map = {
            win32service.SERVICE_STOPPED: "Gestoppt",
            win32service.SERVICE_START_PENDING: "Wird gestartet",
            win32service.SERVICE_STOP_PENDING: "Wird gestoppt",
            win32service.SERVICE_RUNNING: "Läuft",
            win32service.SERVICE_CONTINUE_PENDING: "Wird fortgesetzt",
            win32service.SERVICE_PAUSE_PENDING: "Wird pausiert",
            win32service.SERVICE_PAUSED: "Pausiert"
        }
        return status_map.get(status[1], "Unbekannter Status")
    except Exception as e:
        return f"Fehler: {e}"
