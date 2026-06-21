# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolEnrollment(models.Model):
    """
    Represents the enrollment process of a student into a school for a specific
    academic term and grade. Enrollment is the primary transaction document
    recording a student's participation in one academic term. The approval
    workflow uses multi-approval mixins:
    Draft → Confirm → Approve → Open → Done / Cancel.
    After enrollment is completed (Done), the system records the academic result
    (academic_year_result) and the next promotion grade (promote_to_grade_id),
    which are used by SchoolStudent to update current_grade_id and next_grade_id.
    Enrollment also manages payment billing through payment_term_ids, and a
    payment template (payment_template_id) can be used to auto-populate billing.
    """

    _name = "school_enrollment"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
    ]
    _description = "School Enrollment"

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
        help="The date the enrollment document was created.",
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
        help="The academic year this enrollment is based on.",
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
        help=(
            "The academic term in which the student is enrolled. "
            "Must belong to the selected academic year."
        ),
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
        help="The destination school for this enrollment.",
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        related="school_id.grade_type_id",
        required=False,
        readonly=True,
        help=(
            "The education level type, automatically populated "
            "from the selected school."
        ),
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
        help="The class level the student will attend in this enrollment.",
    )
    grade_class_id = fields.Many2one(
        string="Grade Class",
        comodel_name="school_grade_class",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The specific homeroom class the student is placed in.",
    )
    last_term = fields.Boolean(
        string="Last Term of Academic Year?",
        related="academic_term_id.last_term",
        store=True,
        compute_sudo=True,
        readonly=True,
        help=(
            "Indicates whether this is the last term of the academic year, "
            "derived from the term data."
        ),
    )
    allowed_student_ids = fields.Many2many(
        string="Allowed Students",
        comodel_name="school_student",
        compute="_compute_allowed_student_ids",
        store=False,
        compute_sudo=True,
        help=(
            "List of students eligible for selection in this enrollment, "
            "computed based on the selected grade and term."
        ),
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="school_student",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The student being enrolled.",
    )

    academic_year_result = fields.Selection(
        string="Academic Year Result",
        selection=[
            ("passed", "Passed"),
            ("failed", "Failed"),
            ("drop_out", "Drop Out"),
            ("graduate", "Graduate"),
        ],
        help=(
            "The student's academic result at the end of the enrollment period: "
            "Passed, Failed, Drop Out, or Graduate."
        ),
    )
    promote_to_grade_id = fields.Many2one(
        string="Promote To Grade",
        comodel_name="school_grade",
        help=(
            "The target grade for promotion if the student passes "
            "at the end of the academic year."
        ),
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
        help="The currency used for the enrollment payment billing.",
    )
    allowed_pricelist_ids = fields.Many2many(
        string="Allowed Pricelists",
        comodel_name="product.pricelist",
        compute="_compute_allowed_pricelist_ids",
        store=False,
        help="Available pricelists based on the selected currency.",
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
        help="The pricelist used to calculate enrollment billing amounts.",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        related="student_id.contact_id",
        store=True,
        help=(
            "The student's contact partner, automatically "
            "populated from the student record."
        ),
    )
    payment_template_id = fields.Many2one(
        string="Payment Template",
        comodel_name="school_enrollment_payment_template",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "A payment template that can be applied to "
            "auto-populate the billing terms."
        ),
    )
    payment_term_ids = fields.One2many(
        string="Payment Terms",
        comodel_name="school_enrollment_payment_term",
        inverse_name="enrollment_id",
        help=(
            "The payment billing terms that must be settled "
            "by the student for this enrollment."
        ),
    )
    product_summary_ids = fields.One2many(
        string="Payment Summary",
        comodel_name="school_enrollment.product_summary",
        inverse_name="enrollment_id",
        help=(
            "Automatically maintained summary of all payment term details "
            "grouped by product. Recomputed on every change to payment terms "
            "or their detail lines."
        ),
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
        help=(
            "The accounting journal used to record receivables "
            "for this enrollment payment."
        ),
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
        help="The receivable account used to record enrollment billing.",
    )
    pass_ok = fields.Boolean(
        string="Pass",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help="Policy that determines whether the Pass action button is visible.",
    )
    fail_ok = fields.Boolean(
        string="Fail",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help="Policy that determines whether the Fail action button is visible.",
    )
    drop_out_ok = fields.Boolean(
        string="Drop Out",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help="Policy that determines whether the Drop Out action button is visible.",
    )
    graduate_ok = fields.Boolean(
        string="Graduate",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help="Policy that determines whether the Graduate action button is visible.",
    )

    def _recompute_product_summaries(self):
        for record in self.sudo():
            summary_data = {}
            for term in record.payment_term_ids:
                for detail in term.detail_ids:
                    pid = detail.product_id.id
                    if not pid:
                        continue
                    if pid not in summary_data:
                        summary_data[pid] = {
                            "enrollment_id": record.id,
                            "product_id": pid,
                            "uom_quantity": 0.0,
                            "amount_untaxed": 0.0,
                            "amount_tax": 0.0,
                            "amount_total": 0.0,
                        }
                    summary_data[pid]["uom_quantity"] += detail.uom_quantity
                    summary_data[pid]["amount_untaxed"] += detail.price_subtotal
                    summary_data[pid]["amount_tax"] += detail.price_tax
                    summary_data[pid]["amount_total"] += detail.price_total
            record.product_summary_ids.unlink()
            Summary = self.env[
                "school_enrollment.product_summary"
            ]  # pylint: disable=invalid-name
            for data in summary_data.values():
                Summary.create(data)

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

    @api.depends("academic_term_id", "grade_id", "school_id")
    def _compute_allowed_student_ids(self):
        for record in self:
            result = False
            if record.academic_term_id and record.grade_id and record.school_id:
                criteria = [
                    ("state", "=", "draft"),
                    ("school_id", "=", record.school_id.id),
                ]
                if record.academic_term_id.first_term:
                    criteria += [("next_grade_id", "=", record.grade_id.id)]
                else:
                    criteria += [("current_grade_id", "=", record.grade_id.id)]
                result = self.env["school_student"].search(criteria).ids
            record.allowed_student_ids = result

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

    @api.onchange(
        "academic_term_id",
        "school_id",
        "grade_id",
    )
    def onchange_student_id(self):
        self.student_id = False

    @api.onchange(
        "grade_id",
        "school_id",
    )
    def onchange_grade_class_id(self):
        self.grade_class_id = False

    def action_set_result_to_passed(self):
        for record in self.sudo():
            record._set_result_to_passed()  # pylint: disable=protected-access

    def action_compute_payment(self):
        for record in self.sudo():
            record._compute_payment_from_template()  # pylint: disable=protected-access

    def _compute_payment_from_template(self):
        self.ensure_one()
        template = self.payment_template_id
        if not template:
            return
        self.payment_term_ids.unlink()
        Term = self.env[  # pylint: disable=invalid-name
            "school_enrollment_payment_term"
        ]
        Detail = self.env[  # pylint: disable=invalid-name
            "school_enrollment_payment_term_detail"
        ]
        for tterm in template.term_ids.sorted("sequence"):
            term = Term.create(
                {
                    "enrollment_id": self.id,
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

    def action_set_result_to_failed(self):
        for record in self.sudo():
            record._set_result_to_failed()  # pylint: disable=protected-access

    def action_set_result_to_drop_out(self):
        self.ensure_one()
        for record in self.sudo():
            record._set_result_to_drop_out()  # pylint: disable=protected-access

    def action_set_result_to_graduate(self):
        self.ensure_one()
        for record in self.sudo():
            record._set_result_to_graduate()  # pylint: disable=protected-access

    def _set_result_to_graduate(self):
        self.ensure_one()
        self.with_context(bypass_policy_check=True).action_done()
        self.write(
            {
                "academic_year_result": "graduate",
            }
        )
        self.student_id.action_set_to_graduate()  # pylint: disable=no-member

    def _set_result_to_drop_out(self):
        self.ensure_one()
        self.with_context(bypass_policy_check=True).action_done()
        self.write(
            {
                "academic_year_result": "drop_out",
            }
        )
        self.student_id.action_set_to_dropped()  # pylint: disable=no-member

    def _set_result_to_failed(self):
        self.ensure_one()
        self.with_context(bypass_policy_check=True).action_done()
        self.write(
            {
                "academic_year_result": "failed",
            }
        )
        self.student_id.action_set_to_draft()  # pylint: disable=no-member

    def _set_result_to_passed(self):
        self.ensure_one()
        self.with_context(bypass_policy_check=True).action_done()
        next_grade_id = self.grade_id.next_grade_id.id  # pylint: disable=no-member
        self.write(
            {
                "academic_year_result": "passed",
                "promote_to_grade_id": next_grade_id,
            }
        )
        self.student_id.action_set_to_draft()  # pylint: disable=no-member

    @ssi_decorator.post_open_action()
    def _10_enroll_student(self):
        self.ensure_one()
        self.student_id.action_set_to_enroll()  # pylint: disable=no-member

    @ssi_decorator.post_done_action()
    def _30_unenroll_or_graduate_student(self):
        self.ensure_one()
        self.student_id.action_set_to_draft()  # pylint: disable=no-member

    @ssi_decorator.post_cancel_action()
    def _10_unenroll_student(self):
        self.ensure_one()
        self.student_id.action_set_to_draft()  # pylint: disable=no-member

    @api.model
    def _get_policy_field(self):
        res = super(  # pylint: disable=super-with-arguments
            SchoolEnrollment, self
        )._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
            "pass_ok",
            "fail_ok",
            "drop_out_ok",
            "graduate_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
