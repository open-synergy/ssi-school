# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models


class SchoolPassCriteria(models.Model):
    _name = "school_pass_criteria"
    _inherit = ["mixin.master_data"]
    _description = "School Pass Criteria"

    python_code = fields.Text(
        string="Python Code",
        default="result = True",
    )
