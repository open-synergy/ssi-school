# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestEscalateIncidentMigration(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Post-rename invariants for the ``escalate_incident`` wizard.

    ``school_incident.wizard_escalate`` was renamed to
    ``escalate_incident`` in 14.0.1.2.0. The rename itself cannot be
    exercised here (the migration script runs outside a transaction,
    and CI always installs on a fresh database where the old model
    never existed), so these scenarios assert the invariants the
    migration script (``migrations/14.0.1.2.1/pre-migration.py``) is
    responsible for keeping true: the new model/action/ACL are
    registered, and no trace of the old model name is left behind.
    """

    def test_escalate_incident_migration(self):
        """Run every post-rename invariant scenario from YAML.

        Scenarios are declared in
        ``test_data_escalate_incident_migration.yaml``.
        """
        self.run_yaml_scenario("test_data_escalate_incident_migration.yaml")
