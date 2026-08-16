# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolIncidentEscalationCriteria(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Scenario tests for ``school_incident_escalation_criteria``.

    Covers creating, editing and deleting an Escalation Criteria,
    including the Target Level that ``action_escalate`` matches the
    requested handling tier against.
    """

    def test_school_incident_escalation_criteria(self):
        """Run every ``school_incident_escalation_criteria`` scenario.

        Scenarios are declared in
        ``test_data_school_incident_escalation_criteria.yaml``.
        """
        self.run_yaml_scenario("test_data_school_incident_escalation_criteria.yaml")
