# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentProductSummary(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the product summary computed from the payment terms.

    The scenarios check that adding a term detail creates its summary
    line, that two terms sharing the same product are aggregated into a
    single line, and that the summary disappears when either the detail
    or the whole term is unlinked.
    """

    def test_enrollment_product_summary(self):
        """Run the product summary aggregation and removal scenarios."""
        self.run_yaml_scenario("test_data_enrollment_product_summary.yaml")
