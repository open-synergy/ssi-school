# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionWorkflow(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    def test_admission_workflow(self):
        self.run_yaml_scenario("test_data_admission.yaml")

    def _prepare_payment_template(self):
        """Create a payment template carrying receivable journal/account defaults."""
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        account_type = self.env.ref("account.data_account_type_receivable")
        account = self.env["account.account"].create(
            {
                "name": "Admission Receivable Onchange",
                "code": "ADMREC01",
                "user_type_id": account_type.id,
                "reconcile": True,
            }
        )
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type Onchange", "code": "GTONC1", "sequence": 10}
        )
        school = self.env["school"].create(
            {
                "name": "School Onchange",
                "code": "SCHONC1",
                "grade_type_id": grade_type.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade Onchange",
                "code": "GONC1",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        customer_invoice_type = self.env["customer_invoice_type"].create(
            {
                "name": "Customer Invoice Type Onchange",
                "code": "ADMCITONC1",
                "journal_id": journal.id,
                "receivable_account_id": account.id,
            }
        )
        template = self.env["school_admission_payment_template"].create(
            {
                "name": "Admission Payment Template Onchange",
                "code": "ADMPMTONC1",
                "school_id": school.id,
                "grade_id": grade.id,
                "receivable_journal_id": journal.id,
                "receivable_account_id": account.id,
                "customer_invoice_type_id": customer_invoice_type.id,
            }
        )
        return template, journal, account

    def test_onchange_payment_template_sets_receivable(self):
        """Selecting a payment template copies its receivable journal/account."""
        template, journal, account = self._prepare_payment_template()
        form = Form(self.env["school_admission"])
        form.payment_template_id = template
        self.assertEqual(form.receivable_journal_id, journal)
        self.assertEqual(form.receivable_account_id, account)

    def test_onchange_payment_template_clears_receivable(self):
        """Clearing the payment template clears the receivable journal/account."""
        template, _journal, _account = self._prepare_payment_template()
        form = Form(self.env["school_admission"])
        form.payment_template_id = template
        form.payment_template_id = self.env["school_admission_payment_template"]
        self.assertFalse(form.receivable_journal_id)
        self.assertFalse(form.receivable_account_id)
