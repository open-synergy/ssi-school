# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models


class SchoolScoringSystemDetail(models.Model):
    _name = "school_scoring_system.detail"
    _order = "scoring_system_id, sequence"

    scoring_system_id = fields.Many2one(
        string="Scoring System",
        comodel_name="school_scoring_system",
        required=True,
        ondelete="restrict",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    score_type_id = fields.Many2one(
        string="Score Type",
        comodel_name="school_score_type",
        required=True,
        ondelete="restrict",
    )
    percentage = fields.Float(
        string="Percentage",
        required=True,
        default=0.0,
    )
