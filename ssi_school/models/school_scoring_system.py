# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class SchoolScoringSystem(models.Model):
    _name = "school_scoring_system"
    _inherit = ["mixin.master_data"]
    _description = "School Scoring System"

    usable = fields.Boolean(
        string="Usable",
        compute="_compute_usable",
        store=True,
        compute_sudo=True,
    )
    detail_ids = fields.One2many(
        string="Scoring System Details",
        comodel_name="school_scoring_system.detail",
        inverse_name="scoring_system_id",
    )

    @api.depends(
        "detail_ids",
        "detail_ids.percentage",
    )
    def _compute_usable(self):
        for record in self:
            result = False
            percentage = 0.0
            for detail in record.detail_ids:
                percentage += detail.percentage
            if percentage == 100.00:
                result = True
            record.usable = result
