# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class School(models.Model):  # pylint: disable=too-few-public-methods
    """
    Represents a school entity.
    A school is associated with one grade type that defines the class level
    structure used within it. It is overseen either by a branch or, when no
    branch is set, directly by its center (res.company). Inherits from
    mixin.master_data.
    """

    _name = "school"
    _inherit = ["mixin.master_data"]
    _description = "School"

    grade_type_id = fields.Many2one(
        "school_grade_type",
        string="Grade Type",
        required=True,
        help=(
            "The education level type used by this school, "
            "e.g. Elementary, Junior High, or Senior High School."
        ),
    )
    company_id = fields.Many2one(
        string="Center",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company,
        help="Center (head office) that oversees this school unit.",
    )
    branch_id = fields.Many2one(
        string="Branch",
        comodel_name="school_branch",
        required=False,
        domain="[('company_id', '=', company_id)]",
        help=(
            "Branch that oversees this school unit. "
            "Leave empty when the unit is directly overseen by the center."
        ),
    )

    @api.onchange(
        "company_id",
    )
    def onchange_branch_id(self):
        if self.branch_id and self.branch_id.company_id != self.company_id:
            self.branch_id = False

    @api.constrains("company_id", "branch_id")
    def _check_branch_company(self):
        """Enforce that the branch belongs to the school's center.

        Runs on every create or write touching ``company_id`` or
        ``branch_id``: each record delegates the test to
        ``_check_branch_company_condition``, so a school can never be
        attached to a branch owned by another ``res.company``.

        :raises ValidationError: the branch's center differs from the
            center of the school.
        """
        for record in self.sudo():
            if not record._check_branch_company_condition():
                error_message = (
                    _(
                        """
Context: Set school branch
Database ID: %s
Problem: Branch '%s' does not belong to Center '%s'
Solution: Select a Branch whose Center matches the school's Center
"""
                    )
                    % (
                        record.id,
                        record.branch_id.name,
                        record.company_id.name,
                    )
                )
                raise ValidationError(error_message)

    def _check_branch_company_condition(self):
        """Return whether the branch matches the school's center.

        Extension point of the ``_check_branch_company`` constraint:
        override it to widen or narrow the accepted combinations. A
        school without ``branch_id`` is always valid, since it is then
        overseen directly by the center; otherwise
        ``branch_id.company_id`` must equal ``company_id``.

        :return: ``True`` when the combination is valid.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        if not self.branch_id:
            return True
        return self.branch_id.company_id == self.company_id
