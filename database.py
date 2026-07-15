"""
Elektronikus Hirdetmény Iktató (EHI)

database.py
Adatbázis kezelés
"""

import sqlite3
from pathlib import Path
from config import DATABASE_FILE

DB_VERSION = 1


class Database:

    def __init__(self):
        self.db_file = DATABASE_FILE
        self.connection = None

    # ---------------------------------------------------------
    # Kapcsolódás
    # ---------------------------------------------------------

    def connect(self):

        if self.connection is None:

            self.connection = sqlite3.connect(self.db_file)

            self.connection.row_factory = sqlite3.Row

            self.connection.execute("PRAGMA foreign_keys = ON")

        return self.connection

    # ---------------------------------------------------------
    # Inicializálás
    # ---------------------------------------------------------

    def initialize(self):

        conn = self.connect()

        cur = conn.cursor()

        #
        # Partnerek
        #

        cur.execute("""

        CREATE TABLE IF NOT EXISTS partnerek (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nev TEXT NOT NULL,

            tipus TEXT NOT NULL,

            kod TEXT,

            aktiv INTEGER NOT NULL DEFAULT 1

        )

        """)

        #
        # Beállítások
        #

        cur.execute("""

        CREATE TABLE IF NOT EXISTS beallitasok (

            kulcs TEXT PRIMARY KEY,

            ertek TEXT

        )

        """)

        #
        # Ügyek
        #

        cur.execute("""

        CREATE TABLE IF NOT EXISTS ugyek (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            hivatali_iktatoszam TEXT NOT NULL,

            bekuldo_ugyszam TEXT,

            partner_id INTEGER,

            targy TEXT,

            ugyintezo TEXT,

            kifuggesztes_datum TEXT,

            napok INTEGER,

            levetel_datum TEXT,

            eredeti_pdf TEXT,

            vegleges_pdf TEXT,

            megjegyzes TEXT,

            statusz TEXT DEFAULT 'Aktív',

            torolt INTEGER DEFAULT 0,

            letrehozva TEXT,

            modositva TEXT,

            FOREIGN KEY(partner_id)
                REFERENCES partnerek(id)

        )

        """)

        #
        # Verzió
        #

        cur.execute("""

        CREATE TABLE IF NOT EXISTS rendszer (

            verzio INTEGER

        )

        """)

        #
        # Verzió ellenőrzése
        #

        cur.execute("SELECT COUNT(*) FROM rendszer")

        if cur.fetchone()[0] == 0:

            cur.execute(

                "INSERT INTO rendszer(verzio) VALUES(?)",

                (DB_VERSION,)

            )

        #
        # Alap beállítások
        #

        defaults = {

            "alap_elotag": "MT_IG",

            "dokumentum_veg": "RGY",

            "alap_napok": "15"

        }

        for key, value in defaults.items():

            cur.execute("""

                INSERT OR IGNORE INTO beallitasok
                (kulcs, ertek)

                VALUES (?,?)

            """, (key, value))

        conn.commit()

    # ---------------------------------------------------------
    # Lekérdezés
    # ---------------------------------------------------------

    def execute(self, sql, params=()):

        conn = self.connect()

        cur = conn.cursor()

        cur.execute(sql, params)

        conn.commit()

        return cur

    # ---------------------------------------------------------
    # Lekérdezés eredménnyel
    # ---------------------------------------------------------

    def query(self, sql, params=()):

        conn = self.connect()

        cur = conn.cursor()

        cur.execute(sql, params)

        return cur.fetchall()

    # ---------------------------------------------------------
    # Bezárás
    # ---------------------------------------------------------

    def close(self):

        if self.connection:

            self.connection.close()

            self.connection = None