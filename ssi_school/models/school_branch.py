# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class SchoolBranch(models.Model):  # pylint: disable=too-few-public-methods
    """
    Represents a branch within the school organization hierarchy.
    A branch is overseen by a center (res.company) and, in turn, oversees
    one or more school units. This hierarchy is intentionally separate
    from the Operating Unit concept.
    """

    _name = "school_branch"
    _inherit = ["mixin.master_data"]
    _description = "School Branch"

    company_id = fields.Many2one(
        string="Center",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company,
        help="Center (head office) that oversees this branch.",
    )
    school_ids = fields.One2many(
        string="School Units",
        comodel_name="school",
        inverse_name="branch_id",
        help="School units directly overseen by this branch.",
    )
    school_count = fields.Integer(
        string="Number of School Units",
        compute="_compute_school_count",
        compute_sudo=True,
        help="Number of school units overseen by this branch.",
    )

    @api.depends("school_ids")
    def _compute_school_count(self):
        for record in self:
            record.school_count = len(record.school_ids)
