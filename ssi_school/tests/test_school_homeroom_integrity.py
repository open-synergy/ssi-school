# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests import SavepointCase, tagged

# These scenarios assert that invalid data is REJECTED (ValidationError), which
# the odoo-yaml-test YAML DSL cannot express (any exception raised by a step
# simply fails the scenario). They are written as plain Python tests instead,
# following the same precedent as test_school_enrollment_integrity.py.


@tagged("post_install", "-at_install")
class TestSchoolHomeroomIntegrity(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.grade_type = cls.env["school_grade_type"].create(
            {"name": "Grade Type Homeroom Integrity", "code": "GTHRI", "sequence": 10}
        )
        cls.school = cls.env["school"].create(
            {
                "name": "School Homeroom Integrity",
                "code": "SCHHRI",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.other_school = cls.env["school"].create(
            {
                "name": "Other School Homeroom Integrity",
                "code": "SCHHRI2",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "Grade Homeroom Integrity",
                "code": "GHRI",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )
        cls.other_school_grade = cls.env["school_grade"].create(
            {
                "name": "Grade Other School Homeroom Integrity",
                "code": "GHRI2",
                "sequence": 20,
                "type_id": cls.grade_type.id,
            }
        )
        cls.grade_class = cls.env["school_grade_class"].create(
            {
                "name": "Class Homeroom Integrity",
                "code": "CLHRI",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
                "capacity": 30,
            }
        )
        cls.other_grade_class = cls.env["school_grade_class"].create(
            {
                "name": "Class Other School Homeroom Integrity",
                "code": "CLHRI2",
                "school_id": cls.other_school.id,
                "grade_id": cls.other_school_grade.id,
                "capacity": 30,
            }
        )
        cls.year = cls.env["school_academic_year"].create(
            {
                "name": "Year Homeroom Integrity",
                "code": "AYHRI",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        cls.other_year = cls.env["school_academic_year"].create(
            {
                "name": "Other Year Homeroom Integrity",
                "code": "AYHRI2",
                "date_start": "2025-07-01",
                "date_end": "2026-06-30",
            }
        )
        cls.term = cls.env["school_academic_term"].create(
            {
                "name": "Term Homeroom Integrity",
                "code": "TMHRI",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": cls.year.id,
                "enrollment_state": "open",
            }
        )

    def _base_homeroom_vals(self, **overrides):
        vals = {
            "date": "2024-07-01",
            "academic_year_id": self.year.id,
            "academic_term_id": self.term.id,
            "school_id": self.school.id,
            "grade_id": self.grade.id,
            "grade_class_id": self.grade_class.id,
            "capacity": 30,
        }
        vals.update(overrides)
        return vals

    def test_valid_homeroom_data_is_accepted(self):
        """Sanity check: a fully consistent Homeroom must NOT raise."""
        homeroom = self.env["school_homeroom"].create(self._base_homeroom_vals())
        self.assertEqual(homeroom.state, "draft")

    def test_term_year_mismatch_raises(self):
        with self.assertRaises(ValidationError):
            self.env["school_homeroom"].create(
                self._base_homeroom_vals(academic_year_id=self.other_year.id)
            )

    def test_grade_class_school_mismatch_raises(self):
        with self.assertRaises(ValidationError):
            self.env["school_homeroom"].create(
                self._base_homeroom_vals(grade_class_id=self.other_grade_class.id)
            )
