# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestResPartnerNuptk(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the NUPTK, school partner and class expertise fields.

    The scenarios exercise the ``nuptk`` field of ``res.partner`` and its
    search, archive and multiple-record rejection, the related teacher
    field, the school partner, and the class expertise fields.
    """

    def test_res_partner_nuptk(self):
        """Run the NUPTK, school partner and expertise scenarios."""
        self.run_yaml_scenario("test_data_res_partner_nuptk.yaml")
