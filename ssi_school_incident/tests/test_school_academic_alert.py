# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAcademicAlert(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Scenario tests for ``school_academic_alert``.

    Covers the Draft -> Confirm -> Approve -> Open -> Done approval
    workflow, the Three-Color evaluation against
    ``school_academic_alert_level``, the ``student_id`` onchange that
    derives the homeroom class, and the guards protecting
    ``action_evaluate`` and ``action_create_incident``.
    """

    def test_school_academic_alert(self):
        """Run every ``school_academic_alert`` scenario from YAML.

        Includes the workflow, evaluation, onchange and negative-path
        scenarios declared in
        ``test_data_school_academic_alert.yaml``.
        """
        self.run_yaml_scenario("test_data_school_academic_alert.yaml")
