# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentCreateDueInvoice(YamlTransactionCase):
    """Cover the wizard invoicing the due payment terms in bulk.

    The scenarios exercise how the date range narrows down which terms
    get invoiced, the idempotency of a repeated run, and the guards
    rejecting a non-open enrollment or an inverted date range.
    """

    def test_enrollment_create_due_invoice(self):
        """Run the due invoice date range and guard scenarios."""
        self.run_yaml_scenario("test_data_enrollment_create_due_invoice.yaml")
