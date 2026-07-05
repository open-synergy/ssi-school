# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolHomeroom(models.Model):
    """
    Represents a Homeroom transaction: a bulk enrollment container for one
    academic year, term, grade, and grade class (physical classroom). A
    Homeroom groups many school_enrollment records (via enrollment_ids) so
    that mass re-enrollment for a whole class can be tracked and audited as
    a single document, instead of managing hundreds of individual enrollment
    records with no shared audit trail. The approval workflow uses
    multi-approval mixins: Draft → Confirm → Approve → Open → Done / Cancel.
    """

    _name = "school_homeroom"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
    ]
    _description = "School Homeroom"

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
        help="The date the Homeroom document was created.",
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
        help="The academic year this Homeroom batch is based on.",
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
            "The academic term for this Homeroom batch. "
            "Must belong to the selected Academic Year."
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
        help="The school this Homeroom batch belongs to.",
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        related="school_id.grade_type_id",
        store=True,
        compute_sudo=True,
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
        help="The class level for this Homeroom batch.",
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
        help=(
            "The physical homeroom classroom this batch is enrolled into. "
            "Must belong to the selected Grade and School."
        ),
    )
    teacher_id = fields.Many2one(
        string="Teacher",
        comodel_name="school_teacher",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The homeroom teacher responsible for this batch, if assigned.",
    )
    capacity = fields.Integer(
        string="Capacity",
        default=0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Target seat capacity for this Homeroom batch. Automatically "
            "filled from the selected Grade Class capacity, but can be "
            "adjusted."
        ),
    )
    enrollment_ids = fields.One2many(
        string="Enrollments",
        comodel_name="school_enrollment",
        inverse_name="homeroom_id",
        readonly=True,
        help="Enrollments generated or linked under this Homeroom batch.",
    )
    enrolled_count = fields.Integer(
        string="Enrolled Count",
        compute="_compute_enrolled_count",
        store=True,
        compute_sudo=True,
        help="Number of enrollments currently linked to this Homeroom batch.",
    )
    seat_available = fields.Integer(
        string="Seat Available",
        compute="_compute_enrolled_count",
        store=True,
        compute_sudo=True,
        help="Remaining seats, computed as Capacity minus Enrolled Count.",
    )

    @api.depends(
        "capacity",
        "enrollment_ids",
    )
    def _compute_enrolled_count(self):
        for record in self:
            enrolled_count = len(record.enrollment_ids)
            record.enrolled_count = enrolled_count
            record.seat_available = record.capacity - enrolled_count

    @api.onchange(
        "academic_year_id",
    )
    def onchange_academic_term_id(self):
        self.academic_term_id = False

    @api.onchange(
        "school_id",
    )
    def onchange_grade_id(self):
        self.grade_id = False

    @api.onchange(
        "school_id",
        "grade_id",
    )
    def onchange_grade_class_id(self):
        self.grade_class_id = False

    @api.onchange(
        "grade_class_id",
    )
    def onchange_capacity(self):
        self.capacity = 0
        if self.grade_class_id:
            self.capacity = self.grade_class_id.capacity

    @api.constrains("academic_term_id", "academic_year_id")
    def _check_term_year_match(self):
        for record in self.sudo():
            if not record._check_term_year_match_condition():
                error_message = (
                    _(
                        """
Context: Set Homeroom academic term
Database ID: %s
Problem: Academic Term '%s' does not belong to Academic Year '%s'
Solution: Select an Academic Term that belongs to the selected Academic Year
"""
                    )
                    % (
                        record.id,
                        record.academic_term_id.name,
                        record.academic_year_id.name,
                    )
                )
                raise ValidationError(error_message)

    def _check_term_year_match_condition(self):
        self.ensure_one()
        if not self.academic_term_id or not self.academic_year_id:
            return True
        return self.academic_term_id.year_id == self.academic_year_id

    @api.constrains("grade_class_id", "grade_id", "school_id")
    def _check_grade_class_match(self):
        for record in self.sudo():
            if not record._check_grade_class_match_condition():
                error_message = (
                    _(
                        """
Context: Set Homeroom grade class
Database ID: %s
Problem: Grade Class '%s' does not match the selected Grade/School
Solution: Select a Grade Class that belongs to the selected Grade and School
"""
                    )
                    % (record.id, record.grade_class_id.name)
                )
                raise ValidationError(error_message)

    def _check_grade_class_match_condition(self):
        self.ensure_one()
        if not self.grade_class_id:
            return True
        return (
            self.grade_class_id.grade_id == self.grade_id
            and self.grade_class_id.school_id == self.school_id
        )

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
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
