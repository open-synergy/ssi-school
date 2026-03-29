# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestSchoolAcademicYear(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "2024/2025",
                "code": "AY2425",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )

    # --- CREATE ---

    def test_create(self):
        record = self.env["school_academic_year"].create(
            {
                "name": "2025/2026",
                "code": "AY2526",
                "date_start": "2025-07-01",
                "date_end": "2026-06-30",
            }
        )
        self.assertTrue(record.id)
        self.assertEqual(record.name, "2025/2026")

    # --- EDIT ---

    def test_edit_name(self):
        self.academic_year.write({"name": "2024/2025 Revised"})
        self.assertEqual(self.academic_year.name, "2024/2025 Revised")

    def test_edit_dates(self):
        self.academic_year.write(
            {
                "date_start": "2024-08-01",
                "date_end": "2025-07-31",
            }
        )
        self.assertEqual(str(self.academic_year.date_start), "2024-08-01")
        self.assertEqual(str(self.academic_year.date_end), "2025-07-31")

    # --- DELETE ---

    def test_delete(self):
        record = self.env["school_academic_year"].create(
            {
                "name": "Year To Delete",
                "code": "AYDEL",
                "date_start": "2030-07-01",
                "date_end": "2031-06-30",
            }
        )
        record_id = record.id
        record.unlink()
        self.assertFalse(self.env["school_academic_year"].browse(record_id).exists())

    # --- COMPUTE: first_term_id / last_term_id ---

    def test_compute_first_last_term_empty(self):
        """Jika belum ada term, first_term_id dan last_term_id harus False."""
        self.assertFalse(self.academic_year.first_term_id)
        self.assertFalse(self.academic_year.last_term_id)

    def test_compute_first_last_term_with_terms(self):
        """first_term_id dan last_term_id harus terisi setelah term dibuat."""
        year = self.env["school_academic_year"].create(
            {
                "name": "Year With Terms",
                "code": "AYT",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        term_1 = self.env["school_academic_term"].create(
            {
                "name": "Semester 1",
                "code": "SM1",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": year.id,
            }
        )
        term_2 = self.env["school_academic_term"].create(
            {
                "name": "Semester 2",
                "code": "SM2",
                "date_start": "2025-01-01",
                "date_end": "2025-06-30",
                "year_id": year.id,
            }
        )
        year.invalidate_cache()
        self.assertEqual(year.first_term_id, term_1)
        self.assertEqual(year.last_term_id, term_2)
