# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionForceDeleteInvoice(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover Force Delete Invoice on an admission payment term.

    The scenarios exercise the happy paths for a draft, an open, a
    partially reconciled and a fully paid invoice (the last one on a
    done admission), the chatter note, the policy rejection and the
    rejection of a term that holds no invoice.
    """

    def test_admission_force_delete_invoice(self):
        """Run the force delete invoice scenarios."""
        self.run_yaml_scenario("test_data_admission_force_delete_invoice.yaml")
