# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionOperatingUnit(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover operating unit handling on the three admission models.

    Includes propagation from ``school_admission_form`` to its
    generated ``school_admission_test``, and the derivation of
    ``operating_unit_id`` from ``school_id`` on create/write/onchange.
    """

    def test_school_admission_operating_unit(self):
        """Run every operating unit scenario for the admission models."""
        self.run_yaml_scenario("test_data_school_admission_operating_unit.yaml")
