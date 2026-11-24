# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.5.21.0 -> 14.0.5.22.0
#
# Changes: the Close Addendum button is removed, so a payment term or
#          detail line that was left unlocked because its addendum was
#          never closed can no longer be locked by the user. They are
#          locked here for every enrollment that is open or done, so
#          later changes go through a Payment Term Amendment or Transfer
#          document only.
#
# Note: plain SQL on purpose. An ORM ``write`` would go through the
#       ``write()`` override and its lock guard.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Lock the unlocked terms and details of open or done enrollments.

    Sets ``locked`` to true on every ``school_enrollment_payment_term``
    and ``school_enrollment_payment_term_detail`` row that is still
    unlocked and belongs to an enrollment in state ``open`` or
    ``done``. Draft enrollments are left untouched.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates ``locked`` on terms and detail lines
    """
    terms = openupgrade.logged_query(
        env.cr,
        """
        UPDATE school_enrollment_payment_term term
        SET locked = true
        FROM school_enrollment enrollment
        WHERE term.enrollment_id = enrollment.id
            AND enrollment.state IN ('open', 'done')
            AND term.locked IS NOT TRUE
        """,
    )
    details = openupgrade.logged_query(
        env.cr,
        """
        UPDATE school_enrollment_payment_term_detail detail
        SET locked = true
        FROM school_enrollment_payment_term term
        JOIN school_enrollment enrollment
            ON term.enrollment_id = enrollment.id
        WHERE detail.term_id = term.id
            AND enrollment.state IN ('open', 'done')
            AND detail.locked IS NOT TRUE
        """,
    )
    _logger.info("Locked %s payment term(s) and %s detail line(s).", terms, details)
