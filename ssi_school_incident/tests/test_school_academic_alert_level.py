# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAcademicAlertLevel(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Scenario tests for the ``school_academic_alert_level`` master data.

    Covers creating, editing and deleting an Academic Alert Level,
    including its warning color and the Python Code that decides whether
    the level triggers.
    """

    def test_school_academic_alert_level(self):
        """Run every ``school_academic_alert_level`` scenario from YAML.

        Scenarios are declared in
        ``test_data_school_academic_alert_level.yaml``.
        """
        self.run_yaml_scenario("test_data_school_academic_alert_level.yaml")
