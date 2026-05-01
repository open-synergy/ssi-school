# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolEnrollmentPaymentTemplate(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    A payment billing template for school enrollments.
    Stores standard billing structures that can be automatically applied to an
    enrollment. Templates can be general or specific based on a combination of
    academic term, school, and grade level. The template structure consists of
    one or more payment terms (term_ids), each containing product/fee detail lines.
    """

    _name = "school_enrollment_payment_template"
    _inherit = ["mixin.master_data"]
    _description = "School Enrollment Payment Template"

    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        required=False,
        help=(
            "The academic term this template is based on. "
            "Leave empty if applicable to all terms."
        ),
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=False,
        help=(
            "The school using this template. "
            "Leave empty if applicable to all schools."
        ),
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        related="school_id.grade_type_id",
        store=True,
        help=(
            "The education level type, automatically populated "
            "from the selected school."
        ),
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        required=False,
        help=(
            "The specific grade level targeted by this template. "
            "Will be reset if the school is changed."
        ),
    )
    term_ids = fields.One2many(
        string="Payment Terms",
        comodel_name="school_enrollment_payment_template.term",
        inverse_name="template_id",
        copy=True,
        help=(
            "List of payment periods in this template that "
            "will be applied to the enrollment."
        ),
    )

    @api.onchange("school_id")
    def onchange_grade_id(self):
        self.grade_id = False
