# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolGradeRecompute(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover ``school_grade._recompute_next_previous`` as a repair pass.

    The migration shipped with version ``14.0.5.13.1`` replays that
    method on databases whose chain was built before
    open-synergy/ssi-school#79, when it spanned every grade type at once.
    The scenarios check the three properties the repair relies on:
    a cross-type link is cut, a chain that is already correct survives
    being recomputed twice, and a grade type holding a single grade never
    borrows a neighbour from another type.
    """

    def test_grade_recompute(self):
        """Run the previous/next grade chain repair scenarios."""
        self.run_yaml_scenario("test_data_grade_recompute.yaml")
