# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentOperatingUnit(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover deriving ``operating_unit_id`` from ``school_id``.

    Covers ``school_enrollment`` create/write/onchange derivation,
    including the chain to the customer invoice created by the
    Create Due Invoice wizard.
    """

    def test_school_enrollment_operating_unit(self):
        """Run every enrollment operating unit derivation scenario."""
        self.run_yaml_scenario("test_data_school_enrollment_operating_unit.yaml")
