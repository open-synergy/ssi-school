# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentCustomerInvoice(YamlTransactionCase):
    """Customer invoice generated from enrollment payment terms."""

    def test_enrollment_customer_invoice(self):
        """Create, auto confirm, disconnect and delete the customer invoice."""
        self.run_yaml_scenario("test_data_enrollment_customer_invoice.yaml")
