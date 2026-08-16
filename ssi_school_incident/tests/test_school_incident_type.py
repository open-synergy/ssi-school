# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolIncidentType(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Scenario tests for the ``school_incident_type`` master data.

    Covers creating, editing and deleting an Incident Type, including
    its default handling tier and the First Contact / Resolution SLA
    hours that drive the incident deadline computations.
    """

    def test_school_incident_type(self):
        """Run every ``school_incident_type`` scenario from YAML.

        Scenarios are declared in
        ``test_data_school_incident_type.yaml``.
        """
        self.run_yaml_scenario("test_data_school_incident_type.yaml")
