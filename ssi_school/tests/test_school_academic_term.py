# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestSchoolAcademicTerm(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "2024/2025 Term Test",
                "code": "AY2425T",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        cls.term_1 = cls.env["school_academic_term"].create(
            {
                "name": "Semester 1",
                "code": "SM1T",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": cls.academic_year.id,
            }
        )
        cls.term_2 = cls.env["school_academic_term"].create(
            {
                "name": "Semester 2",
                "code": "SM2T",
                "date_start": "2025-01-01",
                "date_end": "2025-06-30",
                "year_id": cls.academic_year.id,
            }
        )

    # --- CREATE ---

    def test_create(self):
        year = self.env["school_academic_year"].create(
            {
                "name": "2026/2027",
                "code": "AY2627",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        record = self.env["school_academic_term"].create(
            {
                "name": "Semester 1 2026",
                "code": "SM1-2026",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": year.id,
            }
        )
        self.assertTrue(record.id)
        self.assertEqual(record.name, "Semester 1 2026")
        self.assertEqual(record.year_id, year)
        self.assertEqual(record.state, "draft")

    # --- EDIT ---

    def test_edit_name(self):
        self.term_1.write({"name": "Semester 1 Updated"})
        self.assertEqual(self.term_1.name, "Semester 1 Updated")

    def test_edit_dates(self):
        self.term_1.write(
            {
                "date_start": "2024-08-01",
                "date_end": "2024-12-31",
            }
        )
        self.assertEqual(str(self.term_1.date_start), "2024-08-01")

    # --- DELETE ---

    def test_delete(self):
        year = self.env["school_academic_year"].create(
            {
                "name": "Year For Delete Term",
                "code": "AYDT",
                "date_start": "2030-07-01",
                "date_end": "2031-06-30",
            }
        )
        record = self.env["school_academic_term"].create(
            {
                "name": "Term To Delete",
                "code": "TTD",
                "date_start": "2030-07-01",
                "date_end": "2030-12-31",
                "year_id": year.id,
            }
        )
        record_id = record.id
        record.unlink()
        self.assertFalse(self.env["school_academic_term"].browse(record_id).exists())

    # --- COMPUTE: first_term / last_term ---

    def test_compute_first_term(self):
        """term_1 harus menjadi first_term karena merupakan term pertama di year."""
        self.term_1.invalidate_cache()
        self.assertTrue(self.term_1.first_term)
        self.assertFalse(self.term_2.first_term)

    def test_compute_last_term(self):
        """term_2 harus menjadi last_term karena merupakan term terakhir di year."""
        self.term_2.invalidate_cache()
        self.assertFalse(self.term_1.last_term)
        self.assertTrue(self.term_2.last_term)
