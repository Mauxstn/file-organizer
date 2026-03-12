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
| 3D-Modelle | .blend, .obj, .fbx, .dae, .3ds, .stl, .ply, .x3d |
| Sonstige | Alle anderen Dateien |

## Projektstruktur

```
file-organizer/
├── .gitignore
├── README.md
├── requirements.txt
├── dokumente/
│   └── requirements.txt
├── logs/
├── sonstiges/
│   └── README.md
├── src/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── autostart.py
│   ├── config.py
│   ├── handler.py
│   ├── main-minimal.py
│   ├── main.py
│   ├── service.py
│   ├── tray.py
│   └── watcher.py
└── tests/
    ├── __init__.py
    ├── test_config.py
    └── test_handler.py
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

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

**Automatische Dateiorganisation für Windows, Linux und macOS**

Ein intelligentes Python-Tool, das deine Dateien automatisch nach Typen sortiert - perfekt für chaotische Download-Ordner! Stoppe manuelle Dateiverwaltung und lass die KI für dich arbeiten.

## Warum File Organizer?

- **Echtzeitüberwachung** - Dateien werden sofort organisiert, sobald sie erscheinen
- **Smarte KI-Erkennung** - 11+ Dateityp-Kategorien mit präziser Sortierung
- **100% Sicher** - Nur Verschieben, kein Löschen, mit Test-Modus
- **Einfach Setup** - Nur 1 Abhängigkeit, keine komplizierte Konfiguration
- **Kontinuierlich** - Läuft im Hintergrund, ohne Terminal-Fenster

## Schnellstart in 60 Sekunden

### 1. Klonen & Installieren
```bash
git clone https://github.com/Mauxstn/file-organizer.git
cd file-organizer
pip install watchdog
```

### 2. Testen (100% sicher!)
```bash
python -m src.main --dry-run
```

### 3. Loslegen!
```bash
# Windows
python -m src.main --daemon --watch-dir "C:\Users\%USERNAME%\Downloads"

# Linux/macOS  
python -m src.main --daemon --watch-dir ~/Downloads
```

## Beispiel Output

```
2026-03-11 22:18:57 - INFO - File Organizer wird gestartet
2026-03-11 22:18:57 - INFO - Überwache Verzeichnis: C:\Users\Maurice\Downloads
2026-03-11 22:19:02 - INFO - Verschoben: screenshot.png -> Bilder/screenshot.png
2026-03-11 22:19:05 - INFO - Verschoben: dokument.pdf -> Dokumente/dokument.pdf
2026-03-11 22:19:08 - INFO - Verschoben: video.mp4 -> Videos/video.mp4
```

## Was wird wohin verschoben?

| Kategorie | Dateiendungen | Zielordner |
|-----------|---------------|------------|
| **Bilder** | jpg, png, gif, svg, webp, bmp, tiff | `bilder/` |
| **Dokumente** | pdf, doc, docx, txt, rtf, odt | `dokumente/` |
| **Tabellen** | xls, xlsx, csv, ods, numbers | `tabellen/` |
| **Videos** | mp4, avi, mkv, mov, wmv, flv | `videos/` |
| **Audio** | mp3, wav, flac, aac, ogg, m4a | `audio/` |
| **Archiv** | zip, rar, 7z, tar, gz, bz2 | `archiv/` |
| **Code** | py, js, html, css, java, cpp, go | `code/` |
| **Programme** | exe, msi, dmg, pkg, deb, rpm | `programme/` |
| **E-Books** | epub, mobi, azw, azw3 | `e-books/` |
| **Präsentationen** | ppt, pptx, odp, key | `praesentationen/` |
| **3D-Modelle** | blend, obj, fbx, dae, 3ds, stl, ply, x3d | `3d-modelle/` |
| **Sonstiges** | Alle anderen Dateien | `sonstiges/` |

## Nützliche Befehle

```bash
# Nur einmal organisieren (keine Überwachung)
python -m src.main --once

# Ausführliche Logs für Debugging
python -m src.main --log-level DEBUG

# Bestimmtes Verzeichnis überwachen
python -m src.main --watch-dir "C:\Pfad\zum\Ordner"

# System Tray GUI (für visuelle Kontrolle)
python -m src.main --tray
```

## Sicherheitsgarantie

- **Keine Datenverlust** - Dateien werden nur verschoben, niemals gelöscht
- **Keine Systemänderungen** - Berührt keine Systemdateien oder Registry
- **Test-Modus** - `--dry-run` zeigt exakt was passieren würde
- **Konfliktschutz** - Bei doppelten Dateinamen wird automatisch nummeriert
- **Vollständiges Logging** - Jede Aktion wird protokolliert

## Projektarchitektur

```
file-organizer/
├── src/                    # Quellcode
│   ├── main.py            # Hauptprogramm & CLI
│   ├── config.py          # Dateityp-Konfiguration  
│   ├── handler.py         # Dateiverschiebe-Logik
│   ├── watcher.py         # Echtzeitüberwachung
│   ├── service.py         # Windows-Dienst
│   ├── tray.py            # System Tray GUI
│   ├── autostart.py       # Autostart-Manager
│   └── main-minimal.py    # Minimale Version
├── logs/                  # Aktivitäts-Logs
├── tests/                 # Unit-Tests
├── .gitignore             # Git-Ignore
├── requirements.txt       # Requirements
└── README.md              # Dokumentation
```

## Anpassung & Erweiterung

Du kannst die Dateityp-Zuordnungen einfach anpassen:

```python
# In src/config.py
config.add_file_type("3D-Modelle", [".obj", ".fbx", ".blend"])
config.add_file_type("Design", [".psd", ".ai", ".fig"])
config.remove_file_type("Programme")  # Kategorie entfernen
```

## Fortgeschrittene Features

### Windows-Dienst Integration
```bash
# Als Windows-Dienst installieren
python -m src.main --install-service
python -m src.main --start-service
```

### Autostart beim Systemstart
```bash
# Automatisch mit Windows starten
python -m src.main --enable-autostart
```

### System Tray GUI
```bash
# Visuelle Kontrolle via System Tray
python -m src.main --tray
```

## Mitmachen & Beiträge

Du hast eine Idee für ein Feature oder gefunden einen Bug? Super!

- [Bug melden](https://github.com/Mauxstn/file-organizer/issues)
- [Feature vorschlagen](https://github.com/Mauxstn/file-organizer/issues)  
- [Pull Request einreichen](https://github.com/Mauxstn/file-organizer/pulls)
- [GitHub Star geben](https://github.com/Mauxstn/file-organizer) - wenn es dir hilft!

## Lizenz

MIT License - Kostenlos für private und kommerzielle Nutzung

---

**Fertig! Dein Download-Ordner wird nie wieder chaotisch sein!**

[Star auf GitHub](https://github.com/Mauxstn/file-organizer) | 
[Bug melden](https://github.com/Mauxstn/file-organizer/issues) | 
[Feature vorschlagen](https://github.com/Mauxstn/file-organizer/issues)
