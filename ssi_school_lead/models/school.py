# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class School(models.Model):
    _name = "school"
    _inherit = "school"

    default_sales_team_id = fields.Many2one(
        string="Default Sales Team",
        comodel_name="crm.team",
        required=False,
        ondelete="restrict",
    )
