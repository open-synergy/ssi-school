# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolIncidentOperatingUnit(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """
    Test the operating unit coverage added by
    ``ssi_school_incident_operating_unit`` to the school incident family.
    """

    def test_school_incident_operating_unit(self):
        """Run the operating unit scenarios of this module.

        Covers the operating unit default of ``school_incident`` and
        ``school_incident_weekly_review``, the operating unit stored on
        ``school_academic_alert``, and the propagation of that operating
        unit to the ``school_incident`` generated from the alert.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_incident_operating_unit.yaml")
