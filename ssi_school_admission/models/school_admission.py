# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolAdmission(models.Model):
    """
    Represents the final school admission record for a student,
    tracking the admission decision, payment setup, and the creation
    of the student's enrollment profile after approval.
    """

    _name = "school_admission"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
    ]
    _description = "School Admission"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_open_policy_fields = False
    _automatically_insert_open_button = False

    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_done",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    date = fields.Date(
        string="Date",
        default=lambda r: datetime_date.today(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The date of this admission.",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=("The academic year for which the student " "is being admitted."),
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The academic term associated with this admission.",
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The school the student is being admitted to.",
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        related="school_id.grade_type_id",
        required=False,
        readonly=True,
        help="The grade type derived from the selected school.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The grade level the student is being admitted to.",
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The student being admitted to the school.",
    )
    admission_form_id = fields.Many2one(
        string="Admission Form",
        comodel_name="school_admission_form",
        readonly=True,
        help="The admission form that initiated this admission, if any.",
    )
    admission_test_id = fields.Many2one(
        string="Admission Test",
        comodel_name="school_admission_test",
        readonly=True,
        help=("The admission test associated with this admission, " "if any."),
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        default=lambda self: self.env.company.currency_id,
        help=("The currency used for payment calculations " "in this admission."),
    )
    allowed_pricelist_ids = fields.Many2many(
        string="Allowed Pricelists",
        comodel_name="product.pricelist",
        compute="_compute_allowed_pricelist_ids",
        store=False,
        help="Pricelists available based on the selected currency.",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=("The pricelist applied for price calculations " "in this admission."),
    )
    payment_template_id = fields.Many2one(
        string="Payment Template",
        comodel_name="school_admission_payment_template",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The payment template used to generate payment " "terms for this admission."
        ),
    )
    payment_term_ids = fields.One2many(
        string="Payment Terms",
        comodel_name="school_admission_payment_term",
        inverse_name="admission_id",
        help="The payment installment terms defined for this admission.",
    )
    receivable_journal_id = fields.Many2one(
        string="Receivable Journal",
        comodel_name="account.journal",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=("The journal used to post receivable entries " "for admission payments."),
    )
    receivable_account_id = fields.Many2one(
        string="Receivable Account",
        comodel_name="account.account",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=("The account used to record receivables " "for admission payments."),
    )
    school_student_id = fields.Many2one(
        string="School Student",
        comodel_name="school_student",
        readonly=True,
        help=("The student profile created after this " "admission is completed."),
    )

    def _compute_policy(self):  # pylint: disable=missing-return
        _super = super()
        _super._compute_policy()  # pylint: disable=protected-access

    @api.depends(
        "currency_id",
    )
    def _compute_allowed_pricelist_ids(self):
        Pricelist = self.env["product.pricelist"]  # pylint: disable=invalid-name
        for record in self:
            result = []
            if record.currency_id:
                criteria = [("currency_id", "=", record.currency_id.id)]
                result = Pricelist.search(criteria).ids
            record.allowed_pricelist_ids = result

    @api.onchange(
        "currency_id",
    )
    def onchange_pricelist_id(self):
        self.pricelist_id = False

    @api.onchange(
        "academic_year_id",
    )
    def onchange_academic_term_id(self):
        self.academic_term_id = False

    @api.onchange(
        "grade_type_id",
    )
    def onchange_grade_id(self):
        self.grade_id = False

    def action_compute_payment(self):
        for record in self.sudo():
            record._compute_payment_from_template()  # pylint: disable=protected-access

    def _compute_payment_from_template(self):
        self.ensure_one()
        template = self.payment_template_id
        if not template:
            return
        self.payment_term_ids.unlink()
        Term = self.env["school_admission_payment_term"]  # pylint: disable=invalid-name
        Detail = self.env[
            "school_admission_payment_term_detail"
        ]  # pylint: disable=invalid-name
        for tterm in template.term_ids.sorted("sequence"):
            term = Term.create(
                {
                    "admission_id": self.id,
                    "name": tterm.name,
                    "sequence": tterm.sequence,
                }
            )
            for tdetail in tterm.detail_ids.sorted("sequence"):
                Detail.create(
                    {
                        "term_id": term.id,
                        "product_id": tdetail.product_id.id,
                        "name": tdetail.name,
                        "account_id": tdetail.account_id.id,
                        "uom_quantity": tdetail.uom_quantity,
                        "uom_id": tdetail.uom_id.id if tdetail.uom_id else False,
                        "price_unit": tdetail.price_unit,
                        "tax_ids": [(6, 0, tdetail.tax_ids.ids)],
                    }
                )

    @ssi_decorator.post_done_action()
    def _10_create_school_student(self):
        self.ensure_one()
        if self.school_student_id:
            return
        initial_grade = (
            self.grade_id.previous_grade_id or False
        )  # pylint: disable=no-member
        student = self.env["school_student"].create(
            {
                "code": "/",
                "contact_id": self.student_id.id,
                "name": self.student_id.name,
                "school_id": self.school_id.id,
                "initial_grade_id": initial_grade.id if initial_grade else False,
            }
        )
        self.write({"school_student_id": student.id})

    @api.model
    def _get_policy_field(self):
        res = super(
            SchoolAdmission, self
        )._get_policy_field()  # pylint: disable=super-with-arguments
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
