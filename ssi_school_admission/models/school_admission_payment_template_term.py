# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolAdmissionPaymentTemplateTerm(models.Model):
    _name = "school_admission_payment_template.term"
    _description = "School Admission Payment Template Term"
    _order = "template_id, sequence, id"

    template_id = fields.Many2one(
        string="Template",
        comodel_name="school_admission_payment_template",
        ondelete="cascade",
        required=True,
    )
    name = fields.Char(
        string="Term Name",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    detail_ids = fields.One2many(
        string="Detail",
        comodel_name="school_admission_payment_template.term.detail",
        inverse_name="term_id",
        copy=True,
    )
