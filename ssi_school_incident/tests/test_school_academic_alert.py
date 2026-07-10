# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestSchoolAcademicAlert(YamlTransactionCase):
    def test_school_academic_alert(self):
        self.run_yaml_scenario("test_data_school_academic_alert.yaml")

    def _create_student_with_open_enrollment(self, code_suffix):
        grade_type = self.env["school_grade_type"].create(
            {
                "name": "Grade Type Alert OC %s" % code_suffix,
                "code": "GTALEROC%s" % code_suffix,
            }
        )
        school = self.env["school"].create(
            {
                "name": "School Alert OC %s" % code_suffix,
                "code": "SCHALEROC%s" % code_suffix,
                "grade_type_id": grade_type.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade Alert OC %s" % code_suffix,
                "code": "GALEROC%s" % code_suffix,
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Class Alert OC %s" % code_suffix,
                "code": "CLALEROC%s" % code_suffix,
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "AY Alert OC %s" % code_suffix,
                "code": "AYALEROC%s" % code_suffix,
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        academic_term = self.env["school_academic_term"].create(
            {
                "name": "Term Alert OC %s" % code_suffix,
                "code": "TMALEROC%s" % code_suffix,
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": academic_year.id,
                "enrollment_state": "open",
            }
        )
        contact = self.env["res.partner"].create(
            {"name": "Student Contact Alert OC %s" % code_suffix}
        )
        student = self.env["school_student"].create(
            {
                "name": "Student Alert OC %s" % code_suffix,
                "code": "STUALEROC%s" % code_suffix,
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        enrollment = self.env["school_enrollment"].create(
            {
                "date": "2024-07-01",
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "grade_class_id": grade_class.id,
                "student_id": student.id,
            }
        )
        enrollment.sudo().write({"state": "open"})
        student.invalidate_cache()
        return student, enrollment, grade_class

    def _create_minimal_student(self, code_suffix):
        grade_type = self.env["school_grade_type"].create(
            {
                "name": "Grade Type Alert OC %s" % code_suffix,
                "code": "GTALEROC%s" % code_suffix,
            }
        )
        school = self.env["school"].create(
            {
                "name": "School Alert OC %s" % code_suffix,
                "code": "SCHALEROC%s" % code_suffix,
                "grade_type_id": grade_type.id,
            }
        )
        contact = self.env["res.partner"].create(
            {"name": "Student Contact Alert OC %s" % code_suffix}
        )
        return self.env["school_student"].create(
            {
                "name": "Student Alert OC %s" % code_suffix,
                "code": "STUALEROC%s" % code_suffix,
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )

    def _create_three_levels(self, code_suffix):
        levels = self.env["school_academic_alert_level"]
        levels |= levels.create(
            {
                "name": "Yellow Level PY %s" % code_suffix,
                "code": "ALERT-YELLOW-PY%s" % code_suffix,
                "color": "yellow",
                "sequence": 10,
                "python_code": "result = trigger_count >= 2",
            }
        )
        levels |= levels.create(
            {
                "name": "Orange Level PY %s" % code_suffix,
                "code": "ALERT-ORANGE-PY%s" % code_suffix,
                "color": "orange",
                "sequence": 20,
                "python_code": "result = trigger_count >= 3",
            }
        )
        levels |= levels.create(
            {
                "name": "Red Level PY %s" % code_suffix,
                "code": "ALERT-RED-PY%s" % code_suffix,
                "color": "red",
                "sequence": 30,
                "python_code": "result = trigger_count >= 4",
            }
        )
        return levels

    def test_onchange_grade_class_id_from_student(self):
        """Selecting student_id fills grade_class_id from the student's
        active enrollment homeroom class."""
        student, _enrollment, grade_class = self._create_student_with_open_enrollment(
            "1"
        )
        form = Form(self.env["school_academic_alert"])
        form.student_id = student
        self.assertEqual(form.grade_class_id, grade_class)

    def test_create_incident_raises_for_yellow_level(self):
        """action_create_incident must raise a UserError when the last
        evaluation only triggered a Yellow level (only Orange/Red are
        allowed to create a School Incident)."""
        self._create_three_levels("2")
        student = self._create_minimal_student("2")
        alert = self.env["school_academic_alert"].create(
            {
                "date_alert": fields.Date.today(),
                "student_id": student.id,
                "evaluation_context": "trigger_count = 2",
            }
        )
        alert.action_evaluate()
        self.assertEqual(alert.color, "yellow")

        with self.assertRaises(UserError):
            alert.action_create_incident()

    def test_create_incident_raises_when_never_evaluated(self):
        """action_create_incident must raise a UserError when no
        evaluation has ever been run (alert_level_id is empty)."""
        student = self._create_minimal_student("3")
        alert = self.env["school_academic_alert"].create(
            {
                "date_alert": fields.Date.today(),
                "student_id": student.id,
            }
        )
        self.assertFalse(alert.alert_level_id)

        with self.assertRaises(UserError):
            alert.action_create_incident()

    def test_evaluate_alert_level_raises_on_invalid_evaluation_context(self):
        """action_evaluate must raise a UserError when evaluation_context
        is not valid Python source, instead of failing with a raw
        Python exception."""
        self._create_three_levels("4")
        student = self._create_minimal_student("4")
        alert = self.env["school_academic_alert"].create(
            {
                "date_alert": fields.Date.today(),
                "student_id": student.id,
                "evaluation_context": "trigger_count ===",
            }
        )

        with self.assertRaises(UserError):
            alert.action_evaluate()
