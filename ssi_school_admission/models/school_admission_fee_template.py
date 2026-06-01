# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolAdmissionFeeTemplate(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Master data template defining standard admission fee structures
    for a specific school and grade, used to prepopulate fee lines
    on school admission forms.
    """

    _name = "school_admission_fee_template"
    _inherit = ["mixin.master_data"]
    _description = "School Admission Fee Template"

    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=False,
        help="The school this fee template applies to.",
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
        help="The grade level for which this fee template applies.",
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=False,
        help="The accounting journal used to post admission fees.",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=False,
        help="The revenue account for recording admission fee income.",
    )
    line_ids = fields.One2many(
        string="Fee Lines",
        comodel_name="school_admission_fee_template.line",
        inverse_name="template_id",
        copy=True,
        help="The individual fee items included in this template.",
    )

    @api.onchange("school_id")
    def onchange_grade_id(self):
        self.grade_id = False
