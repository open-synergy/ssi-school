# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionPaymentTermDuplicate(YamlTransactionCase):
    def test_admission_payment_term_duplicate(self):
        self.run_yaml_scenario("test_data_admission_payment_term_duplicate.yaml")

    def test_wizard_duplicate_default_get_prefill(self):
        # Plain Python (not YAML): default_get keys off context active_id,
        # which the YAML scenario's context: key cannot express reliably.
        term = self.env["school_admission_payment_term"].create(
            {
                "name": "Term Source PREFILL",
                "sequence": 15,
                "date_invoice": "2024-08-01",
                "date_due": "2024-08-15",
            }
        )
        wizard = (
            self.env["school_admission_payment_term.wizard_duplicate"]
            .with_context(active_id=term.id)
            .create({})
        )
        self.assertEqual(wizard.term_id, term)
        self.assertEqual(wizard.name, "%s (copy)" % term.name)
        self.assertEqual(wizard.sequence, term.sequence)
        self.assertEqual(wizard.date_invoice, term.date_invoice)
        self.assertEqual(wizard.date_due, term.date_due)
