# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionFeeAnalysis(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the ``school_admission_fee_analysis`` reporting view."""

    def test_admission_fee_analysis(self):
        """Run every admission fee analysis scenario against the YAML."""
        self.run_yaml_scenario("test_data_admission_fee_analysis.yaml")
