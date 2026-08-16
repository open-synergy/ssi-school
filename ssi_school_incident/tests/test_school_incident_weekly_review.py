# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolIncidentWeeklyReview(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Scenario tests for ``school_incident_weekly_review``.

    Covers the simplified Draft -> Confirm -> Done approval workflow,
    cancellation and restart, the scoping applied by
    ``action_collect_incidents`` (date range, and School when set), and
    the overdue / escalated / unresolved-over-7-days counters computed
    from the collected incidents.
    """

    def test_school_incident_weekly_review(self):
        """Run every ``school_incident_weekly_review`` scenario from YAML.

        Includes the workflow, collect-scoping and counter scenarios
        declared in ``test_data_school_incident_weekly_review.yaml``.
        """
        self.run_yaml_scenario("test_data_school_incident_weekly_review.yaml")
