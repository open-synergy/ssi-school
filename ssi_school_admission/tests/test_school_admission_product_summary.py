# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionProductSummary(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the aggregated product summary of ``school_admission``."""

    def test_admission_product_summary(self):
        """Run the admission product summary scenario."""
        self.run_yaml_scenario("test_data_admission_product_summary.yaml")
