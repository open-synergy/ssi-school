# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolIncident(YamlTransactionCase):  # pylint: disable=too-few-public-methods
    """Scenario tests for ``school_incident``.

    Covers the Draft -> Confirm -> Approve -> Open -> Done approval
    workflow, cancellation, the SLA driven deadline and overdue
    computations, the ``student_id`` and ``incident_type_id`` onchanges,
    the Resolution Date constraint, and both guards of
    ``action_escalate``.
    """

    def test_school_incident(self):
        """Run every ``school_incident`` scenario from YAML.

        Includes the workflow, compute, onchange and negative-path
        scenarios declared in ``test_data_school_incident.yaml``.
        """
        self.run_yaml_scenario("test_data_school_incident.yaml")
