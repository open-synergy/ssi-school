# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.5.21.0 -> 14.0.5.22.0
#
# Changes: the ``addendum_ok`` policy field is removed from
#          ``school_enrollment`` (and its related copies on the payment
#          term and detail models). Policy template lines that point to
#          that field -- the shipped
#          ``policy_template_school_enrollment_addendum`` record and any
#          line created on an instance -- would be left dangling, so
#          they are deleted before the field itself is dropped.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Delete every policy template line of ``addendum_ok``.

    Looks up the ``policy.template_detail`` records whose field is
    ``school_enrollment.addendum_ok`` -- including lines created on the
    instance, not only the shipped XML record -- and unlinks them, which
    also removes their external identifiers.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; deletes ``policy.template_detail`` records
    """
    details = env["policy.template_detail"].search(
        [
            ("field_id.model", "=", "school_enrollment"),
            ("field_id.name", "=", "addendum_ok"),
        ]
    )
    count = len(details)
    details.unlink()
    _logger.info(
        "Deleted %s policy.template_detail record(s) of addendum_ok.",
        count,
    )
