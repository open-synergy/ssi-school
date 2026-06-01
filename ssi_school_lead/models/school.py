# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class School(models.Model):  # pylint: disable=too-few-public-methods
    """
    Extends the School model to associate a default sales team
    for CRM lead routing and assignment automation.
    """

    _name = "school"
    _inherit = "school"

    default_sales_team_id = fields.Many2one(
        string="Default Sales Team",
        comodel_name="crm.team",
        required=False,
        ondelete="restrict",
        help=(
            "The default sales team assigned to this school "
            "for automatic CRM lead routing."
        ),
    )
