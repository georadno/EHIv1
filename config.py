"""
Elektronikus Hirdetmény Iktató (EHI)

config.py
Globális beállítások
"""

from pathlib import Path

# ---------------------------------------------------------------------
# Projekt könyvtár
# ---------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------------------
# Könyvtárak
# ---------------------------------------------------------------------

DATABASE_DIR = BASE_DIR / "database"
PDF_DIR = BASE_DIR / "pdf"

PDF_ORIGINAL_DIR = PDF_DIR / "eredeti"
PDF_FINAL_DIR = PDF_DIR / "vegleges"

EXPORT_DIR = BASE_DIR / "export"
BACKUP_DIR = BASE_DIR / "backup"
LOG_DIR = BASE_DIR / "logs"
TEMPLATE_DIR = BASE_DIR / "templates"

# ---------------------------------------------------------------------
# Adatbázis
# ---------------------------------------------------------------------

DATABASE_FILE = DATABASE_DIR / "ehi.db"

# ---------------------------------------------------------------------
# Alapbeállítások
# ---------------------------------------------------------------------

APP_NAME = "Elektronikus Hirdetmény Iktató"

VERSION = "0.1.0"

DEFAULT_DAYS = 15

DATE_FORMAT = "%Y-%m-%d"

# ---------------------------------------------------------------------
# Könyvtárak automatikus létrehozása
# ---------------------------------------------------------------------

for folder in [
    DATABASE_DIR,
    PDF_DIR,
    PDF_ORIGINAL_DIR,
    PDF_FINAL_DIR,
    EXPORT_DIR,
    BACKUP_DIR,
    LOG_DIR,
    TEMPLATE_DIR,
]:
    folder.mkdir(parents=True, exist_ok=True)