# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentWorkflow(YamlTransactionCase):
    def test_enrollment_workflow(self):
        self.run_yaml_scenario("test_data_enrollment.yaml")

    def test_onchange_receivable_journal_id_from_template(self):
        """Selecting payment_template_id fills receivable_journal_id from the template."""
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        template = self.env["school_enrollment_payment_template"].create(
            {
                "name": "Template Receivable Journal OC",
                "code": "PMTRJOC",
                "journal_id": journal.id,
            }
        )
        form = Form(self.env["school_enrollment"])
        form.payment_template_id = template
        self.assertEqual(form.receivable_journal_id, journal)

    def test_onchange_receivable_account_id_from_template(self):
        """Selecting payment_template_id fills receivable_account_id from the template."""
        account_type_income = self.env.ref("account.data_account_type_revenue")
        account = self.env["account.account"].create(
            {
                "name": "Test Receivable Account OC",
                "code": "TESTRAOC",
                "user_type_id": account_type_income.id,
            }
        )
        template = self.env["school_enrollment_payment_template"].create(
            {
                "name": "Template Receivable Account OC",
                "code": "PMTRAOC",
                "receivable_account_id": account.id,
            }
        )
        form = Form(self.env["school_enrollment"])
        form.payment_template_id = template
        self.assertEqual(form.receivable_account_id, account)

    def test_onchange_receivable_fields_reset_when_template_cleared(self):
        """Clearing payment_template_id resets both receivable fields."""
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        account_type_income = self.env.ref("account.data_account_type_revenue")
        account = self.env["account.account"].create(
            {
                "name": "Test Receivable Account Reset OC",
                "code": "TESTRARST",
                "user_type_id": account_type_income.id,
            }
        )
        template = self.env["school_enrollment_payment_template"].create(
            {
                "name": "Template Receivable Reset OC",
                "code": "PMTRRST",
                "journal_id": journal.id,
                "receivable_account_id": account.id,
            }
        )
        form = Form(self.env["school_enrollment"])
        form.payment_template_id = template
        form.payment_template_id = self.env["school_enrollment_payment_template"]
        self.assertFalse(form.receivable_journal_id)
        self.assertFalse(form.receivable_account_id)
