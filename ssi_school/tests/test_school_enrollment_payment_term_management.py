# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentPaymentTermManagement(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the maintenance actions of an enrollment payment term.

    The scenarios exercise deleting the customer invoice generated from
    the term, disconnecting that invoice without deleting it, and
    unmarking a term that had been flagged as manual.
    """

    def test_enrollment_payment_term_management(self):
        """Run the delete, disconnect and unmark manual scenarios."""
        self.run_yaml_scenario("test_data_enrollment_payment_term_management.yaml")
