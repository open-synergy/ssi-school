# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests import SavepointCase, tagged

# This scenario asserts that invalid data is REJECTED (ValidationError), which
# the odoo-yaml-test YAML DSL cannot express (any exception raised by a step
# simply fails the scenario). It is written as a plain Python test instead,
# following the same precedent as test_school_enrollment_integrity.py.


@tagged("post_install", "-at_install")
class TestSchoolIntegrity(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.grade_type = cls.env["school_grade_type"].create(
            {"name": "Grade Type Integrity", "code": "GTSCHINT", "sequence": 10}
        )
        cls.other_company = cls.env["res.company"].create(
            {"name": "Other Center Integrity"}
        )
        cls.branch = cls.env["school_branch"].create(
            {
                "name": "Branch Integrity",
                "code": "BRSCHINT",
                "company_id": cls.env.company.id,
            }
        )
        cls.other_branch = cls.env["school_branch"].create(
            {
                "name": "Other Center Branch Integrity",
                "code": "BRSCHINT2",
                "company_id": cls.other_company.id,
            }
        )

    def _base_school_vals(self, **overrides):
        vals = {
            "name": "School Integrity",
            "code": "SCHBRINT",
            "grade_type_id": self.grade_type.id,
        }
        vals.update(overrides)
        return vals

    def test_school_with_matching_branch_company_is_accepted(self):
        """Sanity check: a branch belonging to the school's own center must
        NOT raise."""
        school = self.env["school"].create(
            self._base_school_vals(branch_id=self.branch.id)
        )
        self.assertEqual(school.branch_id, self.branch)

    def test_school_branch_company_mismatch_raises(self):
        with self.assertRaises(ValidationError):
            self.env["school"].create(
                self._base_school_vals(branch_id=self.other_branch.id)
            )

    def test_school_branch_company_mismatch_on_write_raises(self):
        school = self.env["school"].create(self._base_school_vals())
        with self.assertRaises(ValidationError):
            school.write({"branch_id": self.other_branch.id})
