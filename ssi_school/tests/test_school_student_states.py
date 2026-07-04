# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import ValidationError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolStudentStates(YamlTransactionCase):
    def test_student_states(self):
        self.run_yaml_scenario("test_data_student_states.yaml")

    def _create_student(self, code, state=None):
        grade_type = self.env["school_grade_type"].create(
            {
                "name": f"Grade Type Transition {code}",
                "code": f"GTT{code}",
                "sequence": 10,
            }
        )
        school = self.env["school"].create(
            {
                "name": f"School Transition {code}",
                "code": f"SCHT{code}",
                "grade_type_id": grade_type.id,
            }
        )
        contact = self.env["res.partner"].create({"name": f"Transition Contact {code}"})
        student = self.env["school_student"].create(
            {
                "name": f"Transition Student {code}",
                "code": f"STUT{code}",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        if state:
            student.write({"state": state})
        return student

    def test_transition_deceased_to_enrol_raises(self):
        """A deceased student can never transition back into any other state."""
        student = self._create_student("DCS", state="deceased")
        with self.assertRaises(ValidationError):
            student.write({"state": "enrol"})

    def test_transition_graduate_to_enrol_raises(self):
        """A graduated student cannot jump straight back to enrolled; it must
        first be reset to draft before being enrolled again."""
        student = self._create_student("GRD", state="graduate")
        with self.assertRaises(ValidationError):
            student.write({"state": "enrol"})

    def test_transition_dropped_to_draft_to_enrol_allowed(self):
        """Reactivating a dropped student is a legal two-step transition:
        dropped -> draft -> enrol."""
        student = self._create_student("DRP", state="dropped")
        student.write({"state": "draft"})
        student.write({"state": "enrol"})
        self.assertEqual(student.state, "enrol")
