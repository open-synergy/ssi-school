# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestSchoolIncident(YamlTransactionCase):
    def test_school_incident(self):
        self.run_yaml_scenario("test_data_school_incident.yaml")

    def _create_student_with_open_enrollment(self, code_suffix):
        grade_type = self.env["school_grade_type"].create(
            {
                "name": "Grade Type Incident OC %s" % code_suffix,
                "code": "GTINCOC%s" % code_suffix,
            }
        )
        school = self.env["school"].create(
            {
                "name": "School Incident OC %s" % code_suffix,
                "code": "SCHINCOC%s" % code_suffix,
                "grade_type_id": grade_type.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade Incident OC %s" % code_suffix,
                "code": "GINCOC%s" % code_suffix,
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Class Incident OC %s" % code_suffix,
                "code": "CLINCOC%s" % code_suffix,
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "AY Incident OC %s" % code_suffix,
                "code": "AYINCOC%s" % code_suffix,
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        academic_term = self.env["school_academic_term"].create(
            {
                "name": "Term Incident OC %s" % code_suffix,
                "code": "TMINCOC%s" % code_suffix,
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": academic_year.id,
                "enrollment_state": "open",
            }
        )
        contact = self.env["res.partner"].create(
            {"name": "Student Contact Incident OC %s" % code_suffix}
        )
        student = self.env["school_student"].create(
            {
                "name": "Student Incident OC %s" % code_suffix,
                "code": "STUINCOC%s" % code_suffix,
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

    def test_onchange_enrollment_id_from_student(self):
        """Selecting student_id fills enrollment_id from the student's
        open enrollment."""
        student, enrollment, _grade_class = self._create_student_with_open_enrollment(
            "1"
        )
        form = Form(self.env["school_incident"])
        form.student_id = student
        self.assertEqual(form.enrollment_id, enrollment)

    def test_onchange_grade_class_id_from_student(self):
        """Selecting student_id fills grade_class_id from the student's
        active enrollment homeroom class."""
        student, _enrollment, grade_class = self._create_student_with_open_enrollment(
            "2"
        )
        form = Form(self.env["school_incident"])
        form.student_id = student
        self.assertEqual(form.grade_class_id, grade_class)

    def _create_minimal_student(self, code_suffix, **student_extra_vals):
        grade_type = self.env["school_grade_type"].create(
            {
                "name": "Grade Type Incident OC %s" % code_suffix,
                "code": "GTINCOC%s" % code_suffix,
            }
        )
        school = self.env["school"].create(
            {
                "name": "School Incident OC %s" % code_suffix,
                "code": "SCHINCOC%s" % code_suffix,
                "grade_type_id": grade_type.id,
            }
        )
        contact = self.env["res.partner"].create(
            {"name": "Student Contact Incident OC %s" % code_suffix}
        )
        student_vals = {
            "name": "Student Incident OC %s" % code_suffix,
            "code": "STUINCOC%s" % code_suffix,
            "contact_id": contact.id,
            "school_id": school.id,
        }
        student_vals.update(student_extra_vals)
        return self.env["school_student"].create(student_vals)

    def test_onchange_parent_partner_id_from_student_father(self):
        """Selecting student_id fills parent_partner_id from the student's
        Father contact when set."""
        father = self.env["res.partner"].create({"name": "Father Incident OC"})
        student = self._create_minimal_student("3", father_id=father.id)
        form = Form(self.env["school_incident"])
        form.student_id = student
        self.assertEqual(form.parent_partner_id, father)

    def test_onchange_parent_partner_id_fallback_to_guardian(self):
        """When the student has no Father/Mother contact, parent_partner_id
        falls back to the Guardian contact."""
        guardian = self.env["res.partner"].create({"name": "Guardian Incident OC"})
        student = self._create_minimal_student("4", guardian_id=guardian.id)
        form = Form(self.env["school_incident"])
        form.student_id = student
        self.assertEqual(form.parent_partner_id, guardian)

    def test_onchange_handling_level_from_incident_type(self):
        """Selecting incident_type_id fills handling_level from the type's
        default_handling_level."""
        incident_type = self.env["school_incident_type"].create(
            {
                "name": "Injury Case OC",
                "code": "INCTYPE-OC-INJURY",
                "default_handling_level": "2",
            }
        )
        form = Form(self.env["school_incident"])
        form.incident_type_id = incident_type
        self.assertEqual(form.handling_level, "2")

    def test_resolution_status_requires_date_resolved(self):
        """Setting resolution_status to a Resolved value with date_resolved
        filled in must save without error; clearing date_resolved
        afterwards while still Resolved must raise a UserError."""
        student = self._create_minimal_student("5")
        incident_type = self.env["school_incident_type"].create(
            {
                "name": "Resolution Constraint Case",
                "code": "INCTYPE-OC-RESOLUTION",
            }
        )
        incident = self.env["school_incident"].create(
            {
                "date_incident": fields.Date.today(),
                "student_id": student.id,
                "incident_type_id": incident_type.id,
                "description": "Case used to verify the resolution constraint.",
            }
        )

        incident.write(
            {
                "resolution_status": "resolved_satisfied",
                "date_resolved": fields.Date.today(),
            }
        )
        self.assertEqual(incident.resolution_status, "resolved_satisfied")

        with self.assertRaises(UserError):
            incident.write({"date_resolved": False})

    def test_escalate_raises_when_no_criteria_selected(self):
        """Calling action_escalate with an empty escalation_criteria_ids
        recordset must raise a UserError (Guard 1: escalation is never
        automatic, at least one criterion must justify it)."""
        student = self._create_minimal_student("6")
        incident_type = self.env["school_incident_type"].create(
            {
                "name": "Escalation Guard Case - No Criteria",
                "code": "INCTYPE-OC-ESC-NOCRIT",
            }
        )
        incident = self.env["school_incident"].create(
            {
                "date_incident": fields.Date.today(),
                "student_id": student.id,
                "incident_type_id": incident_type.id,
                "description": "Case used to verify the no-criteria escalation guard.",
            }
        )
        empty_criteria = self.env["school_incident_escalation_criteria"]

        with self.assertRaises(UserError):
            incident.action_escalate(
                target_level="2",
                escalation_criteria_ids=empty_criteria,
                escalation_reason="Attempt without any criteria selected.",
            )

    def test_escalate_raises_when_criteria_target_level_mismatch(self):
        """Calling action_escalate with target_level='2' while the
        selected criteria are all target_level='level_3' must raise a
        UserError (Guard 2: criteria must justify the target tier)."""
        student = self._create_minimal_student("7")
        incident_type = self.env["school_incident_type"].create(
            {
                "name": "Escalation Guard Case - Mismatch",
                "code": "INCTYPE-OC-ESC-MISMATCH",
            }
        )
        incident = self.env["school_incident"].create(
            {
                "date_incident": fields.Date.today(),
                "student_id": student.id,
                "incident_type_id": incident_type.id,
                "description": "Case used to verify the mismatched-criteria escalation "
                "guard.",
            }
        )
        mismatched_criteria = self.env["school_incident_escalation_criteria"].create(
            {
                "name": "Physical Harm Involved (Guard Test)",
                "code": "ESC-GUARD-L3",
                "target_level": "level_3",
            }
        )

        with self.assertRaises(UserError):
            incident.action_escalate(
                target_level="2",
                escalation_criteria_ids=mismatched_criteria,
                escalation_reason="Attempt to escalate to tier 2 using a tier-3 "
                "criterion.",
            )
