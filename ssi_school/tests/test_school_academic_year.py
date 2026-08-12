# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAcademicYear(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the ``school_academic_year`` model.

    The scenarios exercise CRUD on an academic year, editing its date
    range, and the computed first and last term links both when the year
    has no term yet and when terms are attached to it.
    """

    def test_academic_year(self):
        """Run the academic year CRUD and first/last term scenarios."""
        self.run_yaml_scenario("test_data_academic_year.yaml")
