# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestCrmLeadPreviousSchool(YamlTransactionCase):
    """Covers the Previous School M2O Configurator on ``crm.lead``."""

    def test_crm_lead_previous_school(self):
        """Run the previous school configurator scenario."""
        self.run_yaml_scenario("test_data_previous_school_configurator.yaml")
