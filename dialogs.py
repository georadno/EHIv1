"""
Elektronikus Hirdetmény Iktató (EHI)

dialogs.py
"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QFormLayout
)

from PySide6.QtCore import QDate

from ui.widgets import (
    LabeledLineEdit,
    LabeledTextEdit,
    PartnerCombo,
    DateField,
    DaysField,
    PdfSelector
)


class UgyDialog(QDialog):

    def __init__(self, db, parent=None):

        super().__init__(parent)

        self.db = db

        self.setWindowTitle("Új ügy")

        self.resize(850,700)

        self.create_ui()

        self.load_partners()

    # -------------------------------------------------------

    def create_ui(self):

        layout = QVBoxLayout(self)

        form = QFormLayout()

        #
        # Partner
        #

        self.partner = PartnerCombo()

        form.addRow("Beküldő", self.partner)

        #
        # Hivatali iktatószám
        #

        self.iktatoszam = LabeledLineEdit(
            "",
            "pl.: IG/15149-2/2026"
        )

        form.addRow(
            "Hivatali iktatószám",
            self.iktatoszam
        )

        #
        # Beküldő ügyszáma
        #

        self.bekuldo_ugyszam = LabeledLineEdit(
            "",
            "Beküldő ügyszáma"
        )

        form.addRow(
            "Beküldő ügyszáma",
            self.bekuldo_ugyszam
        )

        #
        # Tárgy
        #

        self.targy = LabeledTextEdit("")

        form.addRow("Tárgy", self.targy)

        #
        # Ügyintéző
        #

        self.ugyintezo = LabeledLineEdit("")

        form.addRow(
            "Ügyintéző",
            self.ugyintezo
        )

        #
        # Kifüggesztés
        #

        self.kifuggesztes = DateField("")

        form.addRow(
            "Kifüggesztés",
            self.kifuggesztes
        )

        #
        # Napok
        #

        self.napok = DaysField()

        form.addRow(
            "Napok",
            self.napok
        )

        #
        # Levétel
        #

        self.leveletel = DateField("")

        self.leveletel.date.setDate(
            QDate.currentDate().addDays(
                self.napok.value()
            )
        )

        form.addRow(
            "Levétel",
            self.leveletel
        )

        #
        # PDF
        #

        self.pdf = PdfSelector()

        form.addRow(
            "Eredeti PDF",
            self.pdf
        )

        #
        # Megjegyzés
        #

        self.megjegyzes = LabeledTextEdit("")

        form.addRow(
            "Megjegyzés",
            self.megjegyzes
        )

        layout.addLayout(form)

        #
        # Gombok
        #

        buttons = QHBoxLayout()

        self.btn_save = QPushButton("Mentés")

        self.btn_cancel = QPushButton("Mégse")

        buttons.addStretch()

        buttons.addWidget(self.btn_save)

        buttons.addWidget(self.btn_cancel)

        layout.addLayout(buttons)

        #
        # Kapcsolatok
        #

        self.btn_cancel.clicked.connect(self.reject)

        self.btn_save.clicked.connect(self.save_record)
    # -------------------------------------------------------
    # Partnerek betöltése
    # -------------------------------------------------------

    def load_partners(self):

        self.partner.clear()

        sql = """
            SELECT
                id,
                nev
            FROM partnerek
            WHERE aktiv = 1
            ORDER BY nev
        """

        rows = self.db.query(sql)

        for row in rows:
            self.partner.addItem(
                row["nev"],
                row["id"]
            )

    # -------------------------------------------------------
    # Dátumkezelés bekötése
    # -------------------------------------------------------

    def connect_date_events(self):

        self.kifuggesztes.date.dateChanged.connect(
            self.calculate_removal_date
        )

        self.napok.spin.valueChanged.connect(
            self.calculate_removal_date
        )

        self.leveletel.date.dateChanged.connect(
            self.calculate_days
        )

    # -------------------------------------------------------
    # Levétel dátum számítása
    # -------------------------------------------------------

    def calculate_removal_date(self):

        start = self.kifuggesztes.date.date()

        days = self.napok.value()

        self.leveletel.date.blockSignals(True)

        self.leveletel.date.setDate(
            start.addDays(days)
        )

        self.leveletel.date.blockSignals(False)

    # -------------------------------------------------------
    # Napok újraszámítása
    # -------------------------------------------------------

    def calculate_days(self):

        start = self.kifuggesztes.date.date()

        end = self.leveletel.date.date()

        days = start.daysTo(end)

        if days < 1:
            days = 1

        self.napok.spin.blockSignals(True)

        self.napok.setValue(days)

        self.napok.spin.blockSignals(False)

    # -------------------------------------------------------
    # Kötelező mezők ellenőrzése
    # -------------------------------------------------------

    def validate(self):

        if self.partner.currentId() is None:

            QMessageBox.warning(
                self,
                "Hiányzó adat",
                "Nincs kiválasztva beküldő."
            )

            return False

        if self.iktatoszam.text().strip() == "":

            QMessageBox.warning(
                self,
                "Hiányzó adat",
                "A hivatali iktatószám kötelező."
            )

            return False

        if self.targy.text().strip() == "":

            QMessageBox.warning(
                self,
                "Hiányzó adat",
                "A tárgy megadása kötelező."
            )

            return False

        if self.ugyintezo.text().strip() == "":

            QMessageBox.warning(
                self,
                "Hiányzó adat",
                "Az ügyintéző megadása kötelező."
            )

            return False

        if self.leveletel.date.date() < self.kifuggesztes.date.date():

            QMessageBox.warning(
                self,
                "Hibás dátum",
                "A levétel dátuma nem lehet korábbi a kifüggesztés dátumánál."
            )

            return False

        return True
from datetime import datetime

    # -------------------------------------------------------
    # Mentés
    # -------------------------------------------------------

    def save_record(self):

        if not self.validate():
            return

        #
        # Duplikált iktatószám ellenőrzése
        #

        sql = """
            SELECT COUNT(*)
            FROM ugyek
            WHERE hivatali_iktatoszam = ?
              AND torolt = 0
        """

        result = self.db.query(
            sql,
            (self.iktatoszam.text().strip(),)
        )

        if result[0][0] > 0:

            QMessageBox.warning(
                self,
                "Duplikált iktatószám",
                "Ez a hivatali iktatószám már létezik."
            )

            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #
        # Mentés
        #

        sql = """
        INSERT INTO ugyek (

            hivatali_iktatoszam,
            bekuldo_ugyszam,
            partner_id,
            targy,
            ugyintezo,
            kifuggesztes_datum,
            napok,
            levetel_datum,
            eredeti_pdf,
            vegleges_pdf,
            megjegyzes,
            statusz,
            torolt,
            letrehozva,
            modositva

        )

        VALUES (

            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?

        )
        """

        self.db.execute(

            sql,

            (

                self.iktatoszam.text().strip(),

                self.bekuldo_ugyszam.text().strip(),

                self.partner.currentId(),

                self.targy.text(),

                self.ugyintezo.text().strip(),

                self.kifuggesztes.value(),

                self.napok.value(),

                self.levetel.value(),

                self.pdf.filename(),

                "",

                self.megjegyzes.text(),

                "Aktív",

                0,

                now,

                now

            )

        )

        QMessageBox.information(

            self,

            "Sikeres mentés",

            "Az ügy sikeresen mentésre került."

        )

        self.accept()