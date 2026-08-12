# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Rescue ``school_student.father_id``/``mother_id``/``guardian_id`` data
before this version turns the three fields into ``related`` fields on
``contact_id`` (``res.partner``).

Once the fields become ``related=..., store=True``, Odoo recomputes every
row from ``res.partner`` on module update. Since ``res.partner`` almost
never has these three columns populated yet (the feature is new on that
model, see ``ssi_partner`` commit ``b3f8b28``), an unmigrated update would
overwrite -- effectively erase -- all existing student family data.

This script copies ``school_student.<field>`` into ``res_partner.<field>``
of the linked ``contact_id``, but **only** where the ``res_partner`` column
is still ``NULL``. If ``res.partner`` already holds a different value, that
value wins (it was entered after the family feature shipped on
``res.partner``, so it is considered the more recent, authoritative one);
the conflict is logged at INFO level rather than silently discarded.

See open-synergy/ssi-school#168.
"""

import logging

_logger = logging.getLogger(__name__)


def _column_exists(cr, table, column):
    """Report whether a column is still present in the database.

    Used as the guard of ``migrate``: the rescue only makes sense while the
    old ``school_student`` columns have not been dropped yet.

    :param cr: database cursor
    :param table: physical table name
    :param column: physical column name
    :return: True when the column exists, False otherwise
    """
    cr.execute(
        "SELECT 1 FROM information_schema.columns "
        "WHERE table_name = %s AND column_name = %s",
        (table, column),
    )
    return bool(cr.fetchone())


def _migrate_father_id(cr):
    """Copy ``school_student.father_id`` onto the linked contact.

    Only rows whose ``res_partner.father_id`` is still NULL are written, so
    a value already entered on ``res.partner`` always wins. Every conflict
    that is therefore discarded is logged at INFO level.

    :param cr: database cursor
    """
    cr.execute(
        "UPDATE res_partner rp "
        "SET father_id = ss.father_id "
        "FROM school_student ss "
        "WHERE rp.id = ss.contact_id "
        "AND ss.father_id IS NOT NULL "
        "AND rp.father_id IS NULL"
    )
    cr.execute(
        "SELECT ss.id, ss.contact_id, ss.father_id, rp.father_id "
        "FROM school_student ss "
        "JOIN res_partner rp ON rp.id = ss.contact_id "
        "WHERE ss.father_id IS NOT NULL "
        "AND rp.father_id IS NOT NULL "
        "AND rp.father_id != ss.father_id"
    )
    for student_id, contact_id, student_value, partner_value in cr.fetchall():
        _logger.info(
            "school_student id=%s (contact_id=%s): res_partner.father_id "
            "is already set to partner id=%s, discarding conflicting "
            "school_student.father_id=%s",
            student_id,
            contact_id,
            partner_value,
            student_value,
        )


def _migrate_mother_id(cr):
    """Copy ``school_student.mother_id`` onto the linked contact.

    Only rows whose ``res_partner.mother_id`` is still NULL are written, so
    a value already entered on ``res.partner`` always wins. Every conflict
    that is therefore discarded is logged at INFO level.

    :param cr: database cursor
    """
    cr.execute(
        "UPDATE res_partner rp "
        "SET mother_id = ss.mother_id "
        "FROM school_student ss "
        "WHERE rp.id = ss.contact_id "
        "AND ss.mother_id IS NOT NULL "
        "AND rp.mother_id IS NULL"
    )
    cr.execute(
        "SELECT ss.id, ss.contact_id, ss.mother_id, rp.mother_id "
        "FROM school_student ss "
        "JOIN res_partner rp ON rp.id = ss.contact_id "
        "WHERE ss.mother_id IS NOT NULL "
        "AND rp.mother_id IS NOT NULL "
        "AND rp.mother_id != ss.mother_id"
    )
    for student_id, contact_id, student_value, partner_value in cr.fetchall():
        _logger.info(
            "school_student id=%s (contact_id=%s): res_partner.mother_id "
            "is already set to partner id=%s, discarding conflicting "
            "school_student.mother_id=%s",
            student_id,
            contact_id,
            partner_value,
            student_value,
        )


def _migrate_guardian_id(cr):
    """Copy ``school_student.guardian_id`` onto the linked contact.

    Only rows whose ``res_partner.guardian_id`` is still NULL are written,
    so a value already entered on ``res.partner`` always wins. Every
    conflict that is therefore discarded is logged at INFO level.

    :param cr: database cursor
    """
    cr.execute(
        "UPDATE res_partner rp "
        "SET guardian_id = ss.guardian_id "
        "FROM school_student ss "
        "WHERE rp.id = ss.contact_id "
        "AND ss.guardian_id IS NOT NULL "
        "AND rp.guardian_id IS NULL"
    )
    cr.execute(
        "SELECT ss.id, ss.contact_id, ss.guardian_id, rp.guardian_id "
        "FROM school_student ss "
        "JOIN res_partner rp ON rp.id = ss.contact_id "
        "WHERE ss.guardian_id IS NOT NULL "
        "AND rp.guardian_id IS NOT NULL "
        "AND rp.guardian_id != ss.guardian_id"
    )
    for student_id, contact_id, student_value, partner_value in cr.fetchall():
        _logger.info(
            "school_student id=%s (contact_id=%s): res_partner.guardian_id "
            "is already set to partner id=%s, discarding conflicting "
            "school_student.guardian_id=%s",
            student_id,
            contact_id,
            partner_value,
            student_value,
        )


def migrate(cr, version):
    """Rescue the student family data before the fields become related.

    Entry point called by Odoo before this version is loaded. Does nothing
    on a fresh install (``version`` is falsy) or when the old
    ``school_student.father_id`` column is already gone; otherwise the three
    family columns are copied onto the linked ``res.partner`` rows.

    :param cr: database cursor
    :param version: version the module is upgraded from, or a falsy value
        on a fresh install
    """
    if not version:
        # Fresh install, nothing to rescue.
        return
    if not _column_exists(cr, "school_student", "father_id"):
        # Column never existed (unexpected) or was already migrated.
        return
    _migrate_father_id(cr)
    _migrate_mother_id(cr)
    _migrate_guardian_id(cr)
