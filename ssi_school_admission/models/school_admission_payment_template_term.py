# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolAdmissionPaymentTemplateTerm(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents a single payment term in a school admission payment
    template, grouping related fee detail lines into one installment.
    """

    _name = "school_admission_payment_template.term"
    _description = "School Admission Payment Template Term"
    _order = "template_id, sequence, id"

    template_id = fields.Many2one(
        string="Template",
        comodel_name="school_admission_payment_template",
        ondelete="cascade",
        required=True,
        help="The parent payment template this term belongs to.",
    )
    name = fields.Char(
        string="Term Name",
        required=True,
        help="The name or label for this payment installment term.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Determines the order of this term within the template.",
    )
    detail_ids = fields.One2many(
        string="Detail",
        comodel_name="school_admission_payment_template.term.detail",
        inverse_name="term_id",
        copy=True,
        help="The individual fee items included in this payment term.",
    )
