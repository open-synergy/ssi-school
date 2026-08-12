# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentPaymentTermDuplicate(YamlTransactionCase):
    """Cover the wizard duplicating an enrollment payment term.

    The scenario runs the duplication itself, while the Python test
    covers the wizard prefill reading the source term from the context.
    """

    def test_enrollment_payment_term_duplicate(self):
        """Run the payment term duplication scenario."""
        self.run_yaml_scenario("test_data_enrollment_payment_term_duplicate.yaml")

    def test_wizard_duplicate_default_get_prefill(self):
        """Prefill the duplicate wizard from the active payment term.

        Pure Python — trigger P1 (L-01: ``action: call`` throws a
        method's return value away; L-02: the actual side of a YAML
        assert is always a dotted read off a record in the registry).
        What is under test here is the value ``default_get()`` returns,
        which no YAML assertion can reach.

        Opening the wizard with ``active_id`` set copies the source term
        name suffixed with ``(copy)``, its sequence and both of its
        invoice and due dates.
        """
        term = self.env["school_enrollment_payment_term"].create(
            {
                "name": "Term Source PREFILL",
                "sequence": 15,
                "date_invoice": "2024-08-01",
                "date_due": "2024-08-15",
            }
        )
        wizard = (
            self.env["school_enrollment_payment_term.wizard_duplicate"]
            .with_context(active_id=term.id)
            .create({})
        )
        self.assertEqual(wizard.term_id, term)
        self.assertEqual(wizard.name, "%s (copy)" % term.name)
        self.assertEqual(wizard.sequence, term.sequence)
        self.assertEqual(wizard.date_invoice, term.date_invoice)
        self.assertEqual(wizard.date_due, term.date_due)
