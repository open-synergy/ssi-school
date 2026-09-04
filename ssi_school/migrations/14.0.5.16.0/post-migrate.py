# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.5.15.0 -> 14.0.5.16.0
#
# Changes: ``school_enrollment_payment_term.state`` gains a stored
#          ``paid`` value driven by ``customer_invoice_id.state``. Odoo
#          never recomputes an existing stored compute field on module
#          update, so a term whose invoice is already ``done`` would
#          stay stuck at ``invoiced`` until an unrelated write happens
#          to touch it.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Recompute ``state`` on every existing payment term.

    Replays ``_compute_state`` over the whole
    ``school_enrollment_payment_term`` table so a term whose linked
    customer invoice is already ``done`` moves to the new ``paid``
    value right away, instead of waiting for an unrelated write to
    trigger the recompute.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates ``state`` on every
        ``school_enrollment_payment_term`` row
    """
    term_model = env["school_enrollment_payment_term"]
    terms = term_model.search([])
    terms._compute_state()  # pylint: disable=protected-access
    _logger.info(
        "Recomputed state on %s school_enrollment_payment_term " "record(s).",
        len(terms),
    )
