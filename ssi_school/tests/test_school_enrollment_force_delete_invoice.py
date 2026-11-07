# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentForceDeleteInvoice(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover Force Delete Invoice on an enrollment payment term.

    The scenarios exercise the happy paths for a draft, an open, a
    partially reconciled and a fully paid invoice (the last one on a
    done enrollment), the chatter note, the policy rejection and the
    rejection of an invoice already recognized.
    """

    def test_enrollment_force_delete_invoice(self):
        """Run the force delete invoice scenarios."""
        self.run_yaml_scenario("test_data_enrollment_force_delete_invoice.yaml")
