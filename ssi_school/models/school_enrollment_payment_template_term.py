# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolEnrollmentPaymentTemplateTerm(models.Model):
    """
    Represents a payment period (term) within an enrollment payment template.
    Each term is a billing group that will generate one invoice when applied
    to an enrollment. Examples: 'Registration Fee' (term 1),
    'Tuition Semester 1' (term 2), etc.
    """

    _name = "school_enrollment_payment_template.term"
    _description = "School Enrollment Payment Template Term"
    _order = "template_id, sequence, id"

    template_id = fields.Many2one(
        string="Template",
        comodel_name="school_enrollment_payment_template",
        ondelete="cascade",
        required=True,
        help="The parent template that owns this payment period.",
    )
    name = fields.Char(
        string="Term Name",
        required=True,
        help="Name of the payment period, e.g. 'Registration Fee' or 'Tuition Semester 1'.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Order of the payment period within the template. Lower values appear first.",
    )
    detail_ids = fields.One2many(
        string="Detail",
        comodel_name="school_enrollment_payment_template.term.detail",
        inverse_name="term_id",
        copy=True,
        help="Product/fee detail lines included in this payment period.",
    )
