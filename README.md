# File Organizer

Ein Python-Tool zur automatischen Organisation von Dateien nach Typen.

## Beschreibung

Der File Organizer überwacht ein Verzeichnis und verschiebt Dateien automatisch in entsprechende Unterordner basierend auf ihrem Dateityp. Das Tool hilft dabei, Ordnung in chaotische Download-Ordner oder andere Verzeichnisse zu bringen.

## Funktionen

- **Automatische Dateierkennung**: Erkennt Dateitypen anhand ihrer Endungen
- **Flexible Konfiguration**: Dateitypzuordnungen können angepasst werden
- **Dry-Run Modus**: Simulation ohne tatsächliche Dateibewegungen
- **Logging**: Detaillierte Protokollierung aller Aktionen
- **Erweiterbar**: Leicht um neue Dateitypen erweiterbar

## Installation

### 1. Repository klonen

```bash
git clone https://github.com/Mauxstn/file-organizer.git
cd file-organizer
```

### 2. Virtuelle Umgebung erstellen

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

## Verwendung

### Grundlegende Nutzung

```bash
# Aktuelles Verzeichnis organisieren
python -m src.main

# Spezifisches Verzeichnis organisieren
python -m src.main --watch-dir /pfad/zum/verzeichnis

# Dry-Run Modus (Simulation)
python -m src.main --dry-run

# Ausführliches Logging
python -m src.main --log-level DEBUG
```

### Hintergrundbetrieb

```bash
# Im Hintergrund laufen (keine Konsolenausgabe)
python -m src.main --daemon

# Nur einmal organisieren, dann beenden
python -m src.main --once

# System Tray GUI starten
python -m src.main --tray
```

### Windows-Dienst

```bash
# Windows-Dienst installieren
python -m src.main --install-service

# Dienst starten
python -m src.main --start-service

# Dienst stoppen
python -m src.main --stop-service

# Dienst deinstallieren
python -m src.main --uninstall-service

# Dienst-Status anzeigen
python -m src.main --service-status
```

### Autostart

```bash
# Autostart aktivieren
python -m src.main --enable-autostart

# Autostart deaktivieren
python -m src.main --disable-autostart

# Autostart-Status anzeigen
python -m src.main --autostart-status
```

### Kommandozeilenoptionen

- `--watch-dir`: Zu überwachendes Verzeichnis (Standard: aktuelles Verzeichnis)
- `--log-level`: Log-Level (DEBUG, INFO, WARNING, ERROR)
- `--dry-run`: Simulation ohne tatsächliche Dateibewegungen
- `--daemon`: Im Hintergrund laufen (keine Konsolenausgabe)
- `--once`: Nur einmal organisieren, dann beenden
- `--tray`: System Tray GUI starten
- `--install-service`: Windows-Dienst installieren
- `--uninstall-service`: Windows-Dienst deinstallieren
- `--start-service`: Windows-Dienst starten
- `--stop-service`: Windows-Dienst stoppen
- `--service-status`: Status des Windows-Dienstes anzeigen
- `--enable-autostart`: Autostart beim Systemstart aktivieren
- `--disable-autostart`: Autostart beim Systemstart deaktivieren
- `--autostart-status`: Status des Autostart-Eintrags anzeigen

## Standard-Dateitypzuordnungen

| Ordner | Dateiendungen |
|--------|---------------|
| Bilder | .jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp, .svg |
| Dokumente | .pdf, .doc, .docx, .txt, .rtf, .odt, .pages |
| Tabellen | .xls, .xlsx, .csv, .ods, .numbers |
| Präsentationen | .ppt, .pptx, .odp, .key |
| Videos | .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm |
| Audio | .mp3, .wav, .flac, .aac, .ogg, .m4a |
| Archiv | .zip, .rar, .7z, .tar, .gz, .bz2 |
| Code | .py, .js, .html, .css, .java, .cpp, .c, .go, .rs |
| Ausführbare | .exe, .msi, .dmg, .pkg, .deb, .rpm |
| E-Books | .epub, .mobi, .azw, .azw3 |
| Sonstige | Alle anderen Dateien |

## Projektstruktur

```
file-organizer/
├── src/                # Der eigentliche Quellcode
│   ├── __init__.py     # Macht den Ordner zum Python-Paket
│   ├── main.py         # Startpunkt des Programms
│   ├── handler.py      # Logik für das Verschieben der Dateien
│   ├── config.py       # Definition der Dateitypen und Pfade
│   ├── watcher.py      # Dateisystemüberwachung mit watchdog
│   ├── service.py      # Windows-Dienst-Integration
│   ├── tray.py         # System Tray GUI
│   └── autostart.py    # Autostart-Funktionalität
├── logs/               # Speicherort für Aktivitäts-Logs
├── tests/            [⭐ Star auf GitHub](https://github.com/Mauxstn/file-organizer) | 
[🐛 Bug melden](https://github.com/Mauxstn/file-organizer/issues) | 
[💡 Feature vorschlagen](https://github.com/Mauxstn/file-organizer/issues)
├── .gitignore          # Schließt venv/ und __pycache__ aus
├── requirements.txt    # Liste der Abhängigkeiten
└── README.md           # Dokumentation
```

## Entwicklung

### Tests ausführen

```bash
python -m pytest tests/
```

### Code-Style

Das Projekt folgt den PEP 8 Richtlinien. Zur Überprüfung kann `flake8` verwendet werden:
```bash
flake8 src/
```

## Konfiguration anpassen

Die Dateitypzuordnungen können in der `src/config.py` angepasst werden:

```python
# Neuen Dateityp hinzufügen
config.add_file_type("3D-Modelle", [".obj", ".fbx", ".blend"])

# Dateityp entfernen
config.remove_file_type("Ausführbare")
```

## Sicherheit

- Das Tool überspringt versteckte Dateien (beginnend mit '.')
- Bei Dateinamenkonflikten werden automatisch Nummern hinzugefügt
- Dry-Run Modus zur Überprüfung vor der Ausführung
- Detailliertes Logging zur Nachverfolgung aller Aktionen

## Lizenz

MIT License

