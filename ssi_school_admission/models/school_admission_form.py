# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolAdmissionForm(models.Model):
    """
    Represents a school admission registration form submitted
    by a student's parent to apply for admission into a specific
    school and grade, including fee computation and accounting
    entry generation.
    """

    _name = "school_admission_form"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.transaction_account_move_with_field",
        "mixin.account_move_single_line_with_field",
        "mixin.company_currency",
        "mixin.transaction_untaxed_with_field",
        "mixin.transaction_tax_with_field",
        "mixin.transaction_total_with_field",
    ]
    _description = "School Admission Form"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_open_policy_fields = False
    _automatically_insert_open_button = False
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
        "create_admission_ok",
        "create_admission_test_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
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

    # Accounting entry
    _normal_amount = "debit"
    _amount_currency_field_name = "amount_total"
    _partner_id_field_name = "parent_id"

    # Tax computation (for mixin.account_move)
    _tax_lines_field_name = "tax_ids"
    _tax_on_self = False
    _tax_source_recordset_field_name = "line_ids"
    _price_unit_field_name = "price_unit"
    _quantity_field_name = "uom_quantity"

    # Amount computation
    _detail_object_name = "line_ids"
    _detail_amount_field_name = "price_subtotal"
    # _tax_detail_object_name defaults to "tax_ids"
    # _tax_detail_amount_field_name defaults to "tax_amount"
    _amount_tax_field_name = "amount_tax"
    _amount_total_field_name = "amount_total"

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
        help="The date of this admission form.",
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
        help=("The academic year in which the student " "applies for admission."),
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
        help="The academic term associated with this admission form.",
    )
    student_id = fields.Many2one(
        string="Student Name",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The prospective student submitting this admission form.",
    )
    parent_id = fields.Many2one(
        string="Parent Name",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=("The parent or guardian of the student, " "used as the billing partner."),
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The pricelist applied to fee calculations in this form.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="pricelist_id.currency_id",
        store=True,
        compute_sudo=True,
        help="The currency derived from the selected pricelist.",
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
        help=("The school to which the student is " "applying for admission."),
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
        help="The grade level the student is applying to enter.",
    )
    fee_template_id = fields.Many2one(
        string="Fee Template",
        comodel_name="school_admission_fee_template",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=("The fee template used to automatically " "populate fee lines."),
    )
    line_ids = fields.One2many(
        string="Fee Details",
        comodel_name="school_admission_form.line",
        inverse_name="admission_form_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        copy=True,
        help="The individual fee line items for this admission form.",
    )
    tax_ids = fields.One2many(
        string="Taxes",
        comodel_name="school_admission_form.tax",
        inverse_name="admission_form_id",
        readonly=True,
        help="Tax lines computed from the fee items in this form.",
    )
    admission_ids = fields.One2many(
        string="Admissions",
        comodel_name="school_admission",
        inverse_name="admission_form_id",
        help="Admission records linked to this form.",
    )
    admission_test_ids = fields.One2many(
        string="Admission Tests",
        comodel_name="school_admission_test",
        inverse_name="admission_form_id",
        help="Admission test records linked to this form.",
    )
    create_admission_ok = fields.Boolean(
        string="Can Create Admission",
        compute="_compute_policy",
        compute_sudo=True,
        help=("Indicates whether a new admission can be " "created from this form."),
    )
    create_admission_test_ok = fields.Boolean(
        string="Can Create Admission Test",
        compute="_compute_policy",
        compute_sudo=True,
        help=("Indicates whether an admission test can be " "created from this form."),
    )
    admission_test_id = fields.Many2one(
        string="Admission Test",
        comodel_name="school_admission_test",
        compute="_compute_admission_test_id",
        inverse="_inverse_admission_test_id",
        store=False,
        help="The admission test associated with this form.",
    )

    @api.depends("admission_test_ids")
    def _compute_admission_test_id(self):
        for record in self:
            record.admission_test_id = record.admission_test_ids[:1]

    def _inverse_admission_test_id(self):
        for record in self:
            if record.admission_test_id:
                record.admission_test_id.admission_form_id = record

    def action_create_admission_test(self):
        self.ensure_one()
        if not self.admission_test_id:
            test = self.env["school_admission_test"].create(
                {
                    "date": self.date,
                    "academic_year_id": self.academic_year_id.id,
                    "academic_term_id": self.academic_term_id.id,
                    "school_id": self.school_id.id,
                    "grade_id": self.grade_id.id,
                    "admission_form_id": self.id,
                    "student_id": self.student_id.id,
                }
            )
        else:
            test = self.admission_test_id  # pylint: disable=no-member
        return {
            "type": "ir.actions.act_window",
            "name": "Admission Test",
            "res_model": "school_admission_test",
            "res_id": test.id,
            "view_mode": "form",
            "target": "current",
        }

    @api.onchange("academic_year_id")
    def _onchange_academic_term_id(self):
        self.academic_term_id = False

    @api.onchange("fee_template_id")
    def _onchange_fee_template_id(self):
        if self.fee_template_id:
            self.journal_id = (
                self.fee_template_id.journal_id
            )  # pylint: disable=attribute-defined-outside-init
            self.account_id = (
                self.fee_template_id.account_id
            )  # pylint: disable=attribute-defined-outside-init
        else:
            self.journal_id = False  # pylint: disable=attribute-defined-outside-init
            self.account_id = False  # pylint: disable=attribute-defined-outside-init

    def action_compute_fee(self):
        for record in self.sudo():
            record._compute_fee_from_template()  # pylint: disable=protected-access

    def action_compute_tax(self):
        for record in self:
            record._recompute_standard_tax()  # pylint: disable=protected-access

    @ssi_decorator.post_open_action()
    def _10_create_accounting_entry(
        self,
    ):  # pylint: disable=inconsistent-return-statements
        self.ensure_one()

        if self.move_id:
            return True

        self._create_standard_move()  # Mixin
        ml = (
            self._create_standard_ml()
        )  # Mixin  # pylint: disable=protected-access,invalid-name
        self.write(
            {
                "move_line_id": ml.id,
            }
        )

        for line in self.line_ids:
            line_ml = (
                line._create_standard_ml()
            )  # Mixin  # pylint: disable=protected-access
            line.write(
                {
                    "move_line_id": line_ml.id,
                }
            )

        for tax in self.tax_ids:
            tax._create_standard_ml()  # Mixin

        self._post_standard_move()  # Mixin

    @ssi_decorator.post_cancel_action()
    def _delete_accounting_entry(self):
        self.ensure_one()
        self._delete_standard_move()  # Mixin

    def _compute_fee_from_template(self):
        self.ensure_one()
        template = self.fee_template_id
        if not template:
            return
        self.line_ids.unlink()
        Line = self.env["school_admission_form.line"]  # pylint: disable=invalid-name
        for tline in template.line_ids.sorted("sequence"):
            Line.create(
                {
                    "admission_form_id": self.id,
                    "sequence": tline.sequence,
                    "product_id": tline.product_id.id,
                    "name": tline.name,
                    "account_id": tline.account_id.id if tline.account_id else False,
                    "analytic_account_id": tline.analytic_account_id.id
                    if tline.analytic_account_id
                    else False,
                    "usage_id": tline.usage_id.id if tline.usage_id else False,
                    "price_unit": tline.price_unit,
                    "uom_quantity": tline.uom_quantity,
                    "uom_id": tline.uom_id.id if tline.uom_id else False,
                    "tax_ids": [(6, 0, tline.tax_ids.ids)],
                }
            )

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "done_ok",
            "cancel_ok",
            "open_ok",
            "restart_ok",
            "manual_number_ok",
            "restart_approval_ok",
            "create_admission_ok",
            "create_admission_test_ok",
        ]
        res += policy_field
        return res
