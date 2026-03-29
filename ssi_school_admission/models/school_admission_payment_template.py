# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolAdmissionPaymentTemplate(models.Model):
    _name = "school_admission_payment_template"
    _inherit = ["mixin.master_data"]
    _description = "School Admission Payment Template"

    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        required=False,
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=False,
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        related="school_id.grade_type_id",
        store=True,
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        required=False,
    )
    term_ids = fields.One2many(
        string="Payment Terms",
        comodel_name="school_admission_payment_template.term",
        inverse_name="template_id",
        copy=True,
    )

    @api.onchange("school_id")
    def onchange_grade_id(self):
        self.grade_id = False
