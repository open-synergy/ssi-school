# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestCrmLeadFamilyCardNumber(YamlTransactionCase):
    """Covers the ``family_card_number`` capture field on ``crm.lead``."""

    def test_crm_lead_family_card_number(self):
        """Run the family card number format scenario."""
        self.run_yaml_scenario("test_data_crm_lead_family_card_number.yaml")
