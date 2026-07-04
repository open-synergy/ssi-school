# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests import SavepointCase, tagged

# These scenarios assert that invalid data is REJECTED (ValidationError), which
# the odoo-yaml-test YAML DSL cannot express (any exception raised by a step
# simply fails the scenario). They are written as plain Python tests instead,
# following the same precedent as the onchange tests in this test suite.


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentIntegrity(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.grade_type = cls.env["school_grade_type"].create(
            {"name": "Grade Type Integrity", "code": "GTINT", "sequence": 10}
        )
        cls.school = cls.env["school"].create(
            {
                "name": "School Integrity",
                "code": "SCHINT",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.other_school = cls.env["school"].create(
            {
                "name": "Other School Integrity",
                "code": "SCHINT2",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "Grade Integrity",
                "code": "GINT",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )
        cls.other_school_grade = cls.env["school_grade"].create(
            {
                "name": "Grade Other School Integrity",
                "code": "GINT2",
                "sequence": 20,
                "type_id": cls.grade_type.id,
            }
        )
        cls.grade_class = cls.env["school_grade_class"].create(
            {
                "name": "Class Integrity",
                "code": "CLINT",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
            }
        )
        cls.other_grade_class = cls.env["school_grade_class"].create(
            {
                "name": "Class Other School Integrity",
                "code": "CLINT2",
                "school_id": cls.other_school.id,
                "grade_id": cls.other_school_grade.id,
            }
        )
        cls.year = cls.env["school_academic_year"].create(
            {
                "name": "Year Integrity",
                "code": "AYINT",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        cls.other_year = cls.env["school_academic_year"].create(
            {
                "name": "Other Year Integrity",
                "code": "AYINT2",
                "date_start": "2025-07-01",
                "date_end": "2026-06-30",
            }
        )
        cls.term = cls.env["school_academic_term"].create(
            {
                "name": "Term Integrity",
                "code": "TMINT",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": cls.year.id,
                "enrollment_state": "open",
            }
        )
        cls.closed_term = cls.env["school_academic_term"].create(
            {
                "name": "Closed Term Integrity",
                "code": "TMINTCL",
                "date_start": "2025-01-01",
                "date_end": "2025-06-30",
                "year_id": cls.year.id,
                "enrollment_state": "close",
            }
        )
        cls.contact = cls.env["res.partner"].create({"name": "Contact Integrity"})
        cls.student = cls.env["school_student"].create(
            {
                "name": "Student Integrity",
                "code": "STUINT",
                "contact_id": cls.contact.id,
                "school_id": cls.school.id,
            }
        )
        cls.other_contact = cls.env["res.partner"].create(
            {"name": "Other Contact Integrity"}
        )
        cls.other_student = cls.env["school_student"].create(
            {
                "name": "Other Student Integrity",
                "code": "STUINT2",
                "contact_id": cls.other_contact.id,
                "school_id": cls.school.id,
            }
        )
        cls.capped_grade_class = cls.env["school_grade_class"].create(
            {
                "name": "Class Capacity Integrity",
                "code": "CLCAP",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
                "capacity": 1,
            }
        )

    def _base_enrollment_vals(self, **overrides):
        vals = {
            "date": "2024-07-01",
            "academic_year_id": self.year.id,
            "academic_term_id": self.term.id,
            "school_id": self.school.id,
            "grade_id": self.grade.id,
            "grade_class_id": self.grade_class.id,
            "student_id": self.student.id,
            "currency_id": self.env.company.currency_id.id,
        }
        vals.update(overrides)
        return vals

    def test_valid_enrollment_data_is_accepted(self):
        """Sanity check: a fully consistent enrollment must NOT raise."""
        enrollment = self.env["school_enrollment"].create(self._base_enrollment_vals())
        enrollment.write({"state": "open"})
        self.assertEqual(enrollment.state, "open")

    def test_term_year_mismatch_raises(self):
        with self.assertRaises(ValidationError):
            self.env["school_enrollment"].create(
                self._base_enrollment_vals(academic_year_id=self.other_year.id)
            )

    def test_grade_class_school_mismatch_raises(self):
        with self.assertRaises(ValidationError):
            self.env["school_enrollment"].create(
                self._base_enrollment_vals(grade_class_id=self.other_grade_class.id)
            )

    def test_open_enrollment_outside_window_raises(self):
        enrollment = self.env["school_enrollment"].create(
            self._base_enrollment_vals(academic_term_id=self.closed_term.id)
        )
        with self.assertRaises(ValidationError):
            enrollment.write({"state": "open"})

    def test_duplicate_active_enrollment_raises(self):
        first = self.env["school_enrollment"].create(self._base_enrollment_vals())
        first.write({"state": "open"})
        second = self.env["school_enrollment"].create(self._base_enrollment_vals())
        with self.assertRaises(ValidationError):
            second.write({"state": "open"})

    def test_grade_class_capacity_reflects_open_enrollments(self):
        enrollment = self.env["school_enrollment"].create(
            self._base_enrollment_vals(
                grade_class_id=self.capped_grade_class.id,
                student_id=self.student.id,
            )
        )
        enrollment.write({"state": "open"})
        self.capped_grade_class.invalidate_cache()
        self.assertEqual(self.capped_grade_class.student_count, 1)
        self.assertEqual(self.capped_grade_class.available_seat, 0)

    def test_grade_class_over_capacity_raises(self):
        first = self.env["school_enrollment"].create(
            self._base_enrollment_vals(
                grade_class_id=self.capped_grade_class.id,
                student_id=self.student.id,
            )
        )
        first.write({"state": "open"})
        second = self.env["school_enrollment"].create(
            self._base_enrollment_vals(
                grade_class_id=self.capped_grade_class.id,
                student_id=self.other_student.id,
            )
        )
        with self.assertRaises(ValidationError):
            second.write({"state": "open"})
