# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestResPartnerNisn(YamlTransactionCase):  # pylint: disable=too-few-public-methods
    """Cover the ``nisn`` field of ``res.partner``.

    The scenarios exercise the compute, inverse and search helpers of
    ``partner_identification`` behind that field, including archiving on
    an empty value and the rejection of a write when several NISN ID
    numbers exist.
    """

    def test_res_partner_nisn(self):
        """Run the NISN compute, inverse and search scenarios."""
        self.run_yaml_scenario("test_data_res_partner_nisn.yaml")
