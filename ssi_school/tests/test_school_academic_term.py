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

    # --- ACTION METHODS: state ---

    def test_action_open(self):
        """Tombol Open: draft → open."""
        record = self.env["school_academic_term"].create(
            {
                "name": "Term Action Open",
                "code": "TAO",
                "date_start": "2027-07-01",
                "date_end": "2027-12-31",
                "year_id": self.academic_year.id,
            }
        )
        self.assertEqual(record.state, "draft")
        record.action_open()
        self.assertEqual(record.state, "open")

    def test_action_done(self):
        """Tombol Done: open → done."""
        record = self.env["school_academic_term"].create(
            {
                "name": "Term Action Done",
                "code": "TAD",
                "date_start": "2027-07-01",
                "date_end": "2027-12-31",
                "year_id": self.academic_year.id,
            }
        )
        record.action_open()
        self.assertEqual(record.state, "open")
        record.action_done()
        self.assertEqual(record.state, "done")

    def test_action_restart(self):
        """Tombol Restart: done → draft."""
        record = self.env["school_academic_term"].create(
            {
                "name": "Term Action Restart",
                "code": "TAR",
                "date_start": "2027-07-01",
                "date_end": "2027-12-31",
                "year_id": self.academic_year.id,
            }
        )
        record.action_open()
        record.action_done()
        self.assertEqual(record.state, "done")
        record.action_restart()
        self.assertEqual(record.state, "draft")

    # --- ACTION METHODS: enrollment_state ---

    def test_action_open_enrollment(self):
        """Tombol Open Enrollment: close → open."""
        record = self.env["school_academic_term"].create(
            {
                "name": "Term Enroll Open",
                "code": "TEO",
                "date_start": "2027-07-01",
                "date_end": "2027-12-31",
                "year_id": self.academic_year.id,
            }
        )
        self.assertEqual(record.enrollment_state, "close")
        record.action_open_enrollment()
        self.assertEqual(record.enrollment_state, "open")

    def test_action_close_enrollment(self):
        """Tombol Close Enrollment: open → close."""
        record = self.env["school_academic_term"].create(
            {
                "name": "Term Enroll Close",
                "code": "TEC",
                "date_start": "2027-07-01",
                "date_end": "2027-12-31",
                "year_id": self.academic_year.id,
            }
        )
        record.action_open_enrollment()
        self.assertEqual(record.enrollment_state, "open")
        record.action_close_enrollment()
        self.assertEqual(record.enrollment_state, "close")
