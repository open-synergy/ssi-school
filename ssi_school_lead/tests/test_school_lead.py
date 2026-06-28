# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestSchoolLead(YamlTransactionCase):
    def test_school_lead(self):
        self.run_yaml_scenario("test_data_school_lead.yaml")

    def test_onchange_payment_template_id_auto_populates(self):
        """payment_template_id should auto-populate when school, grade, and term match."""
        year = self.env["school_academic_year"].create(
            {
                "name": "Year OC",
                "code": "AYOC",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        term = self.env["school_academic_term"].create(
            {
                "name": "Term OC",
                "code": "SMOC",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
                "year_id": year.id,
                "is_open_admission": True,
            }
        )
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type OC", "code": "GTOC", "sequence": 10}
        )
        school = self.env["school"].create(
            {"name": "School OC", "code": "SCHOC", "grade_type_id": grade_type.id}
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade OC",
                "code": "GOC",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        template = self.env["school_admission_payment_template"].create(
            {
                "name": "PT OC",
                "code": "PTOC",
                "school_id": school.id,
                "grade_id": grade.id,
                "academic_term_id": term.id,
            }
        )
        student = self.env["res.partner"].create({"name": "Student OC"})
        lead = (
            self.env["crm.lead"]
            .with_user(self.env.ref("base.user_admin"))
            .create({"name": "Lead OC"})
        )

        form = Form(
            self.env["crm.lead.create_admission"].with_context(
                default_lead_id=lead.id,
                default_student_id=student.id,
            )
        )
        form.academic_year_id = year
        form.school_id = school
        form.grade_id = grade
        form.academic_term_id = term

        self.assertEqual(form.payment_template_id.id, template.id)

    def test_onchange_payment_template_id_clears_on_school_change(self):
        """payment_template_id should clear when school changes."""
        year = self.env["school_academic_year"].create(
            {
                "name": "Year OC2",
                "code": "AYOC2",
                "date_start": "2025-07-01",
                "date_end": "2026-06-30",
            }
        )
        term = self.env["school_academic_term"].create(
            {
                "name": "Term OC2",
                "code": "SMOC2",
                "date_start": "2025-07-01",
                "date_end": "2026-06-30",
                "year_id": year.id,
                "is_open_admission": True,
            }
        )
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type OC2", "code": "GTOC2", "sequence": 10}
        )
        school_a = self.env["school"].create(
            {"name": "School OC2A", "code": "SCHOC2A", "grade_type_id": grade_type.id}
        )
        school_b = self.env["school"].create(
            {"name": "School OC2B", "code": "SCHOC2B", "grade_type_id": grade_type.id}
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade OC2",
                "code": "GOC2",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        self.env["school_admission_payment_template"].create(
            {
                "name": "PT OC2",
                "code": "PTOC2",
                "school_id": school_a.id,
                "grade_id": grade.id,
                "academic_term_id": term.id,
            }
        )
        student = self.env["res.partner"].create({"name": "Student OC2"})
        lead = (
            self.env["crm.lead"]
            .with_user(self.env.ref("base.user_admin"))
            .create({"name": "Lead OC2"})
        )

        form = Form(
            self.env["crm.lead.create_admission"].with_context(
                default_lead_id=lead.id,
                default_student_id=student.id,
            )
        )
        form.academic_year_id = year
        form.school_id = school_a
        form.grade_id = grade
        form.academic_term_id = term
        self.assertTrue(form.payment_template_id.id)

        form.school_id = school_b
        self.assertFalse(form.payment_template_id.id)
