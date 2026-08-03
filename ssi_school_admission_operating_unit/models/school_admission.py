# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models

from .school_admission_operating_unit_mixin import (
    derive_operating_unit_from_school_vals,
)


class SchoolAdmission(models.Model):
    """
    Extends School Admission with single operating unit support
    for operating unit-based access and data segregation. Derives
    operating_unit_id from school_id on create/write instead of
    relying solely on the creating user's default operating unit.
    """

    _name = "school_admission"
    _inherit = [
        "school_admission",
        "mixin.single_operating_unit",
    ]

    @api.model
    def create(self, vals):
        """Derive ``operating_unit_id`` from ``school_id`` on create.

        Overridden so ``operating_unit_id`` always reflects the
        school's own operating unit rather than the creating user's
        default operating unit from ``mixin.single_operating_unit``,
        unless the caller explicitly passes ``operating_unit_id`` in
        the same ``vals``.

        :param vals: values for the new record
        :return: the created ``school_admission`` record
        """
        derive_operating_unit_from_school_vals(self.env, vals)
        return super().create(vals)

    def write(self, vals):
        """Re-derive ``operating_unit_id`` when ``school_id`` changes.

        Only triggers when ``school_id`` is part of ``vals``, so a
        write that only sets ``operating_unit_id`` (e.g. the
        ``ssi_school_admission_lead_operating_unit`` wizard patch,
        applied right after creation) passes through unchanged.

        :param vals: values to write
        :return: True
        """
        derive_operating_unit_from_school_vals(self.env, vals)
        return super().write(vals)

    @api.onchange("school_id")
    def onchange_operating_unit_id(self):
        """Set ``operating_unit_id`` from the selected school.

        Mirrors the ``create``/``write`` derivation so the form shows
        the correct operating unit before the record is saved. Only
        sets a value when the school has exactly one operating unit;
        otherwise the current value is left untouched.
        """
        if self.school_id and len(self.school_id.operating_unit_ids) == 1:
            self.operating_unit_id = self.school_id.operating_unit_ids
