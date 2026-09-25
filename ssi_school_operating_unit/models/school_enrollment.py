# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models

from .school_enrollment_operating_unit_mixin import (
    derive_operating_unit_from_school_vals,
)


class SchoolEnrollment(models.Model):
    """Extend School Enrollment with single operating unit support.

    Restricts each enrollment record to one operating unit, and
    derives ``operating_unit_id`` from ``school_id`` on create/write
    instead of relying solely on the creating user's default
    operating unit.
    """

    _name = "school_enrollment"
    _inherit = [
        "school_enrollment",
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
        :return: the created ``school_enrollment`` record
        """
        derive_operating_unit_from_school_vals(self.env, vals)
        return super().create(vals)

    def write(self, vals):
        """Re-derive ``operating_unit_id`` when ``school_id`` changes.

        Only triggers when ``school_id`` is part of ``vals``, so a
        write that only sets ``operating_unit_id`` passes through
        unchanged.

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

    def _prepare_standard_move(self):
        """Add this enrollment's own operating unit to the move values.

        Extension point (``mixin.account_move``): the Revenue
        Recognition move must always carry this enrollment's own
        ``operating_unit_id`` -- never the acting user's default
        operating unit -- so it stays reconciled with the customer
        invoice already tied to the same operating unit. Copied
        unconditionally, including when this enrollment itself has no
        operating unit set.

        :return: dict of ``account.move`` create values
        """
        result = super()._prepare_standard_move()
        result["operating_unit_id"] = self.operating_unit_id.id
        return result
