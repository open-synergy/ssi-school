# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.2.26.0 -> 14.0.2.27.0
#
# Changes: ``school_admission_payment_term.state`` gains a stored
#          ``paid`` value driven by ``customer_invoice_id.state``. Odoo
#          never recomputes an existing stored compute field on module
#          update, so a term whose invoice is already ``done`` would
#          stay stuck at ``invoiced`` until an unrelated write happens
#          to touch it.
#
# Note: the first version of this script called ``_compute_state()``
#       directly. Outside of ``env.protecting``, ``Field.__set__``
#       drops a real id into its ``other_ids`` branch and calls
#       ``records.write(...)``, going through the model's ``write()``
#       override -- which runs ``_check_addendum_lock`` and raised
#       ``UserError`` on every already-locked term. It reproducibly
#       failed the 2026-09-04 production deploy of the twin module
#       (``ssi_school``, issue #387). The fix replays the compute
#       through the same ``env.add_to_compute`` + ``flush`` idiom the
#       ORM itself uses for a normal recompute, which writes at the
#       field level under ``env.protecting`` and never calls
#       ``write()``.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Recompute ``state`` on every existing payment term.

    Marks ``state`` to be recomputed on the whole
    ``school_admission_payment_term`` table via
    ``env.add_to_compute`` and forces it with ``flush``, so a term
    whose linked customer invoice is already ``done`` moves to the
    new ``paid`` value right away, instead of waiting for an
    unrelated write to trigger the recompute. This idiom writes at
    the field level under ``env.protecting`` (see
    ``Field.compute_value``), so it never calls the model's
    ``write()`` and therefore never trips ``_check_addendum_lock`` on
    a term that is already ``locked`` -- unlike calling
    ``_compute_state()`` directly, which does.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates ``state`` on every
        ``school_admission_payment_term`` row
    """
    term_model = env["school_admission_payment_term"]
    terms = term_model.search([])
    env.add_to_compute(terms._fields["state"], terms)
    terms.flush(["state"])
    _logger.info(
        "Recomputed state on %s school_admission_payment_term " "record(s).",
        len(terms),
    )
