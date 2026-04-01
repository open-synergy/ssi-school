# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolAdmissionFeeTemplateLine(models.Model):
    """
    Represents a single fee line item in a school admission fee template,
    defining the product, account, and amount for one admission fee item.
    """

    _name = "school_admission_fee_template.line"
    _inherit = ["mixin.product_line_account"]
    _description = "School Admission Fee Template - Line"
    _order = "template_id, sequence, id"

    template_id = fields.Many2one(
        string="Template",
        comodel_name="school_admission_fee_template",
        required=True,
        ondelete="cascade",
        help="The admission fee template this line belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help=("Determines the display order of this line " "within the template."),
    )
    product_id = fields.Many2one(
        required=True,
    )
