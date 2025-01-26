# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models


class SchoolTeacher(models.Model):
    _name = "school_teacher"
    _inherit = ["mixin.master_data"]
    _description = "Teacher"

    contact_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
        required=True,
        ondelete="restrict",
    )
