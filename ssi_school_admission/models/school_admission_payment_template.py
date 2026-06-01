# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolAdmissionPaymentTemplate(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Master data template defining the payment schedule structure for
    school admission, used to populate payment terms on admission
    records for a specific school and grade.
    """

    _name = "school_admission_payment_template"
    _inherit = ["mixin.master_data"]
    _description = "School Admission Payment Template"

    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        required=False,
        help="The academic term this payment template applies to.",
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=False,
        help="The school this payment template applies to.",
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        related="school_id.grade_type_id",
        store=True,
        help="The grade type derived from the selected school.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        required=False,
        help="The grade level for which this payment template applies.",
    )
    term_ids = fields.One2many(
        string="Payment Terms",
        comodel_name="school_admission_payment_template.term",
        inverse_name="template_id",
        copy=True,
        help=("The payment term items defining the schedule " "in this template."),
    )

    @api.onchange("school_id")
    def onchange_grade_id(self):
        self.grade_id = False
