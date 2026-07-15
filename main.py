"""
Elektronikus Hirdetmény Iktató (EHI)

main.py
Program belépési pont
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from config import APP_NAME, VERSION
from database import Database
from ui.main_window import MainWindow


def initialize():
    """
    Program indulásakor végrehajtandó inicializálás.
    """

    db = Database()
    db.initialize()

    return db


def create_application():

    app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(VERSION)

    icon = Path("resources/icon.ico")

    if icon.exists():
        app.setWindowIcon(QIcon(str(icon)))

    return app


def main():

    db = initialize()

    app = create_application()

    window = MainWindow(db)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()