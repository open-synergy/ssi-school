# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree
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

    def test_create_admission_propagates_receivable(self):
        """Admission created from lead inherits receivable journal/account from template."""
        year = self.env["school_academic_year"].create(
            {
                "name": "Year OC3",
                "code": "AYOC3",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        term = self.env["school_academic_term"].create(
            {
                "name": "Term OC3",
                "code": "SMOC3",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
                "year_id": year.id,
                "is_open_admission": True,
            }
        )
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type OC3", "code": "GTOC3", "sequence": 10}
        )
        school = self.env["school"].create(
            {"name": "School OC3", "code": "SCHOC3", "grade_type_id": grade_type.id}
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade OC3",
                "code": "GOC3",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        account = self.env["account.account"].create(
            {
                "name": "Admission Receivable OC3",
                "code": "ADMRECOC3",
                "user_type_id": self.env.ref("account.data_account_type_receivable").id,
                "reconcile": True,
            }
        )
        template = self.env["school_admission_payment_template"].create(
            {
                "name": "PT OC3",
                "code": "PTOC3",
                "school_id": school.id,
                "grade_id": grade.id,
                "academic_term_id": term.id,
                "receivable_journal_id": journal.id,
                "receivable_account_id": account.id,
            }
        )
        student = self.env["res.partner"].create({"name": "Student OC3"})
        lead = (
            self.env["crm.lead"]
            .with_user(self.env.ref("base.user_admin"))
            .create({"name": "Lead OC3"})
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
        wizard = form.save()
        wizard.action_confirm()

        admission = lead.admission_id
        self.assertTrue(admission)
        self.assertEqual(admission.receivable_journal_id, journal)
        self.assertEqual(admission.receivable_account_id, account)

    def test_crm_lead_form_view_groups_school_fields(self):
        """Python murni — pemicu P1 (L-01): tata letak view (arch hasil
        `fields_view_get`) bukan permukaan yang bisa dibaca DSL `odoo-yaml-test`,
        dan `action: call` membuang nilai balik method.

        `student_id` harus berada di group `school_lead_prospective_student`,
        `school_id` di `school_lead_admission_target`, dan `admission_id` di
        `school_lead_admission_document` — bukan lagi anak langsung dari group
        bawaan CRM `lead_partner`/`opportunity_partner`, yang tetap memuat
        `partner_id` dan berjudul `Parent/Guardian`.
        """
        result = self.env["crm.lead"].fields_view_get(view_type="form")
        arch = etree.fromstring(result["arch"])

        for group_name, expected_string, expected_fields in (
            ("school_lead_prospective_student", "Prospective Student", ["student_id"]),
            ("school_lead_admission_target", "Admission Target", ["school_id"]),
            (
                "school_lead_admission_document",
                "Admission Document",
                ["admission_id", "create_admission_ok"],
            ),
        ):
            group = arch.find(".//group[@name='%s']" % group_name)
            self.assertIsNotNone(group, "Group %s not found in arch" % group_name)
            self.assertEqual(group.get("string"), expected_string)
            child_field_names = [
                field.get("name") for field in group.findall("./field")
            ]
            self.assertEqual(sorted(child_field_names), sorted(expected_fields))

        school_field_names = {
            "school_id",
            "student_id",
            "admission_id",
            "create_admission_ok",
        }
        for partner_group_name in ("lead_partner", "opportunity_partner"):
            group = arch.find(".//group[@name='%s']" % partner_group_name)
            self.assertIsNotNone(
                group, "Group %s not found in arch" % partner_group_name
            )
            self.assertEqual(group.get("string"), "Parent/Guardian")
            child_field_names = {
                field.get("name") for field in group.findall("./field")
            }
            self.assertIn("partner_id", child_field_names)
            self.assertFalse(
                child_field_names & school_field_names,
                "School fields leaked into group %s: %s"
                % (partner_group_name, child_field_names & school_field_names),
            )
