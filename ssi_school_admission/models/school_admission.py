# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolAdmission(models.Model):
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
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        related="school_id.grade_type_id",
        required=False,
        readonly=True,
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
    )
    admission_form_id = fields.Many2one(
        string="Admission Form",
        comodel_name="school_admission_form",
        readonly=True,
    )
    admission_test_id = fields.Many2one(
        string="Admission Test",
        comodel_name="school_admission_test",
        readonly=True,
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
    )
    allowed_pricelist_ids = fields.Many2many(
        string="Allowed Pricelists",
        comodel_name="product.pricelist",
        compute="_compute_allowed_pricelist_ids",
        store=False,
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
    )
    payment_term_ids = fields.One2many(
        string="Payment Terms",
        comodel_name="school_admission_payment_term",
        inverse_name="admission_id",
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
    )
    school_student_id = fields.Many2one(
        string="School Student",
        comodel_name="school_student",
        readonly=True,
    )

    def _compute_policy(self):
        _super = super()
        _super._compute_policy()

    @api.depends(
        "currency_id",
    )
    def _compute_allowed_pricelist_ids(self):
        Pricelist = self.env["product.pricelist"]
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
            record._compute_payment_from_template()

    def _compute_payment_from_template(self):
        self.ensure_one()
        template = self.payment_template_id
        if not template:
            return
        self.payment_term_ids.unlink()
        Term = self.env["school_admission_payment_term"]
        Detail = self.env["school_admission_payment_term_detail"]
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
        initial_grade = self.grade_id.previous_grade_id or False
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
        res = super(SchoolAdmission, self)._get_policy_field()
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
