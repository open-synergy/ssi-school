# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Backfill the ``school_grade`` previous/next chain on existing databases.

``school_grade.previous_grade_id`` and ``school_grade.next_grade_id`` are
plain stored fields maintained by code, not computes, so Odoo never
rebuilds them on module update. ``_recompute_next_previous`` is only
reached from ``create``, ``write`` and ``unlink`` of ``school_grade``.

Before open-synergy/ssi-school#79 that method walked every grade of the
database as a single ordered list, so the last grade of one ``type_id``
was linked to the first grade of the next one. The fix scoped the chain
per ``type_id``, but it only repairs a database once somebody happens to
edit a grade: an instance that already stored a cross-type chain keeps it
forever, and it propagates into
``school_enrollment._set_result_to_passed`` (``promote_to_grade_id``) and
``school_student._compute_next_grade_id`` -- students get "promoted" into
another education level instead of graduating.

This script replays ``_recompute_next_previous`` once, so every instance
upgraded to this version ends up with a chain scoped per ``type_id``
without any manual intervention.

See open-synergy/ssi-school#79 and open-synergy/ssi-school#184.
"""

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Relink every grade chain so that it stays inside its grade type.

    Entry point called by Odoo after this version is loaded. Does nothing
    on a fresh install (``version`` is falsy), since there is no legacy
    chain to repair there. Otherwise the per-``type_id`` algorithm
    introduced by open-synergy/ssi-school#79 is replayed over the whole
    ``school_grade`` table, which is why this runs as ``post-`` and calls
    the ORM instead of SQL: that algorithm stays the single source of
    truth.

    :param cr: database cursor
    :param version: version the module is upgraded from, or a falsy value
        on a fresh install
    :return: nothing; rewrites ``previous_grade_id`` and
        ``next_grade_id`` on every ``school_grade`` row
    """
    if not version:
        # Fresh install: no legacy chain to repair.
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    grade_model = env["school_grade"]
    grade_model._recompute_next_previous()
    _logger.info(
        "Rebuilt the previous/next chain of %s school_grade record(s), "
        "scoped per type_id.",
        grade_model.search_count([]),
    )
