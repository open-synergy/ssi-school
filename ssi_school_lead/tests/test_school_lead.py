# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree
from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestSchoolLead(YamlTransactionCase):
    """Cover the school/admission fields and flow on ``crm.lead``."""

    def test_school_lead(self):
        """Run the school lead CRUD, compute, and admission scenario."""
        self.run_yaml_scenario("test_data_school_lead.yaml")

    def _create_customer_invoice_type(self, suffix):
        """Create the customer invoice type required by a payment template.

        :param suffix: unique suffix used to build the record name/code
        :return: the created ``customer_invoice_type`` record
        """
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        account = self.env["account.account"].create(
            {
                "name": "Customer Invoice Receivable %s" % suffix,
                "code": "CIREC%s" % suffix,
                "user_type_id": self.env.ref("account.data_account_type_receivable").id,
                "reconcile": True,
            }
        )
        return self.env["customer_invoice_type"].create(
            {
                "name": "Customer Invoice Type %s" % suffix,
                "code": "CIT%s" % suffix,
                "journal_id": journal.id,
                "receivable_account_id": account.id,
            }
        )

    def test_onchange_payment_template_id_auto_populates(self):
        """payment_template_id auto-populates once school/grade/term match.

        Pure Python -- trigger P12 (L-20: ``odoo-yaml-test``'s
        ``action: form`` opens ``Form()`` without a ``view:`` key, so it
        cannot exercise the domain-restricted ``academic_term_id`` and
        ``payment_template_id`` fields the way this wizard's own form
        view declares them). ``payment_template_id`` is a plain stored
        field with no server-side default: it is only ever populated by
        the chained ``onchange_payment_template_id`` while the wizard
        form is live, so the assertion needs a real ``Form()`` walking
        the view-declared fields in sequence.
        """
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
                "customer_invoice_type_id": self._create_customer_invoice_type("OC").id,
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
        """payment_template_id clears once the school changes.

        Pure Python -- trigger P12 (L-20: ``odoo-yaml-test``'s
        ``action: form`` cannot bind to this wizard's own view, which
        is what declares the ``payment_template_id`` domain that the
        chained onchange relies on). Same wizard/``Form()`` reasoning
        as ``test_onchange_payment_template_id_auto_populates``.
        """
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
                "customer_invoice_type_id": self._create_customer_invoice_type(
                    "OC2"
                ).id,
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
        """Admission inherits the receivable journal/account from template.

        Pure Python -- trigger P12 (L-20: reaching ``payment_template_id``
        requires the same wizard-form onchange chain as the two tests
        above, which ``action: form`` cannot drive without a ``view:``
        key). ``action_confirm()`` is called directly on the ``Form()``-
        saved wizard afterwards to assert the propagation onto the
        created ``school_admission``.
        """
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
                "customer_invoice_type_id": self._create_customer_invoice_type(
                    "OC3"
                ).id,
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

        Ketiga nama group ini adalah kontrak publik yang sengaja diperluas modul
        lain (mis. `ssi_school_admission_lead`) lewat `xpath`, sehingga assertion
        di sini memeriksa **keberadaan** (`assertIn`) field wajib milik
        `ssi_school_lead`, bukan daftar tertutup — sesuai Skenario Uji #147
        ("arch form memuat ...").
        """
        result = self.env["crm.lead"].fields_view_get(view_type="form")
        arch = etree.fromstring(result["arch"])

        for group_name, expected_string, required_fields in (
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
            for required_field in required_fields:
                self.assertIn(
                    required_field,
                    child_field_names,
                    "Group %s should contain field %s" % (group_name, required_field),
                )

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
