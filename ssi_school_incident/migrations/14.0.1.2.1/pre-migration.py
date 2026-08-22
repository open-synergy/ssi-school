# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.2.0 -> 14.0.1.2.1
#
# Changes: the escalation wizard was renamed from
#          school_incident.wizard_escalate to escalate_incident
#          (model, view, action, and ACL) without a migration script.
#          Databases upgraded from any version <= 14.0.1.2.0 keep the
#          orphaned ir.model, ir.actions.act_window (still bound to
#          school_incident's "More" menu via binding_model_id),
#          ir.ui.view, ir.model.access, and ir.model.data rows of the
#          old model name, which raises
#          "KeyError: 'school_incident.wizard_escalate'" when School
#          Incident is updated or opened. This purges every trace of
#          the old TransientModel before ir.model.data._process_end()
#          loads this module's data files; its data is disposable
#          (wizard input, never held state worth keeping).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

OLD_MODEL = "school_incident.wizard_escalate"


@openupgrade.migrate()
def migrate(env, version):
    """Purge every leftover record and table of the renamed wizard.

    Removes, in dependency order, the ir.model.access,
    ir.model.fields.selection, ir.translation, ir.ui.view,
    ir.actions.act_window (with its ir.actions parent row --
    ``ir.actions.actions.unlink()`` does not cascade to subtype
    tables, so both must be deleted explicitly), ir.model.fields,
    ir.model, and ir.model.data rows that still reference the old
    model name ``school_incident.wizard_escalate``, then drops its
    table and many2many relation table.

    Idempotent: every ``DELETE`` is scoped by a condition on the old
    model name and every ``DROP TABLE`` uses ``IF EXISTS``, so this is
    a no-op on databases that never installed a pre-rename version.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; purges leftover
        ``school_incident.wizard_escalate`` artifacts
    """
    cr = env.cr

    # ir.model.access rows for the old model.
    openupgrade.logged_query(
        cr,
        """
        DELETE FROM ir_model_access
        WHERE model_id IN (
            SELECT id FROM ir_model WHERE model = '%s'
        )
        """
        % OLD_MODEL,
    )
    _logger.info("Deleted %s ir.model.access row(s).", cr.rowcount)

    # ir.model.fields.selection rows for fields of the old model
    # (target_level's selection values).
    openupgrade.logged_query(
        cr,
        """
        DELETE FROM ir_model_fields_selection
        WHERE field_id IN (
            SELECT id FROM ir_model_fields WHERE model = '%s'
        )
        """
        % OLD_MODEL,
    )
    _logger.info("Deleted %s ir.model.fields.selection row(s).", cr.rowcount)

    # ir.translation rows keyed to the old model name
    # (name = 'school_incident.wizard_escalate,<field>').
    openupgrade.logged_query(
        cr,
        """
        DELETE FROM ir_translation
        WHERE name LIKE '%s,%%'
        """
        % OLD_MODEL,
    )
    _logger.info("Deleted %s ir.translation row(s).", cr.rowcount)

    # ir.ui.view rows for the old model.
    openupgrade.logged_query(
        cr,
        """
        DELETE FROM ir_ui_view
        WHERE model = '%s'
        """
        % OLD_MODEL,
    )
    _logger.info("Deleted %s ir.ui.view row(s).", cr.rowcount)

    # ir.actions.act_window rows for the old model, then their
    # ir.actions parent rows. ir.actions.actions.unlink() does NOT
    # cascade to subtype tables (see the NOTE in that method's
    # docstring in Odoo core: "ondelete cascade will not work on
    # ir.actions.actions"), so both tables need an explicit DELETE.
    # Capture the ids first: both rows of a given action share the
    # same id (both tables draw from the 'ir_actions_id_seq'
    # sequence), so the captured act_window ids double as the
    # ir_actions ids to purge.
    cr.execute("SELECT id FROM ir_act_window WHERE res_model = %s", (OLD_MODEL,))
    act_window_ids = [row[0] for row in cr.fetchall()]

    openupgrade.logged_query(
        cr,
        """
        DELETE FROM ir_act_window
        WHERE res_model = '%s'
        """
        % OLD_MODEL,
    )
    _logger.info("Deleted %s ir.actions.act_window row(s).", cr.rowcount)

    if act_window_ids:
        ids_sql = ",".join(str(i) for i in act_window_ids)
        openupgrade.logged_query(
            cr,
            "DELETE FROM ir_actions WHERE id IN (%s)" % ids_sql,
        )
        _logger.info("Deleted %s orphaned ir.actions row(s).", cr.rowcount)

    # ir.model.fields rows for the old model.
    openupgrade.logged_query(
        cr,
        """
        DELETE FROM ir_model_fields
        WHERE model = '%s'
        """
        % OLD_MODEL,
    )
    _logger.info("Deleted %s ir.model.fields row(s).", cr.rowcount)

    # ir.model row for the old model.
    openupgrade.logged_query(
        cr,
        """
        DELETE FROM ir_model
        WHERE model = '%s'
        """
        % OLD_MODEL,
    )
    _logger.info("Deleted %s ir.model row(s).", cr.rowcount)

    # ir.model.data rows for the old model's XML IDs (module
    # ssi_school_incident only; no other module ever referenced it).
    openupgrade.logged_query(
        cr,
        """
        DELETE FROM ir_model_data
        WHERE module = 'ssi_school_incident'
          AND (
              name = 'model_school_incident_wizard_escalate'
              OR name LIKE 'school_incident_wizard_escalate\\_%'
              OR name LIKE 'field_school_incident_wizard_escalate\\_\\_%'
              OR name LIKE 'selection\\_\\_school_incident_wizard_escalate\\_\\_%'
          )
        """,
    )
    _logger.info("Deleted %s ir.model.data row(s).", cr.rowcount)

    # Drop the transient model's own table and its many2many relation
    # table (school_incident_escalation_criteria selection). Order is
    # binding: the relation table's wizard_id column carries a foreign
    # key onto school_incident_wizard_escalate, so the relation table
    # MUST be dropped first -- dropping the referenced table first
    # raises psycopg2.errors.DependentObjectsStillExist and rolls back
    # the whole migration.
    openupgrade.logged_query(
        cr,
        "DROP TABLE IF EXISTS " "rel_school_incident_wizard_escalate_2_criteria",
    )
    openupgrade.logged_query(cr, "DROP TABLE IF EXISTS school_incident_wizard_escalate")
