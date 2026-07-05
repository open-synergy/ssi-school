# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import random
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
    allowed_student_ids = fields.Many2many(
        string="Allowed Students",
        comodel_name="school_student",
        compute="_compute_allowed_student_ids",
        store=False,
        compute_sudo=True,
        help=(
            "List of students eligible to be added as candidates for this "
            "Homeroom, computed from the selected school, grade, and term."
        ),
    )
    candidate_student_ids = fields.Many2many(
        string="Candidate Students",
        comodel_name="school_student",
        relation="rel_homeroom_candidate_student",
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
            "Students selected to have a draft enrollment generated under "
            "this Homeroom. Fill manually or via the Fill Random action."
        ),
    )
    candidate_count = fields.Integer(
        string="Candidate Count",
        compute="_compute_candidate_count",
        help="Number of students currently selected as candidates.",
    )
    fill_random_ok = fields.Boolean(
        string="Can Fill Random",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help="Policy that determines whether the Fill Random button is visible.",
    )
    generate_enrollments_ok = fields.Boolean(
        string="Can Generate Enrollments",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help=(
            "Policy that determines whether the Generate Enrollments "
            "button is visible."
        ),
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

    @api.depends("candidate_student_ids")
    def _compute_candidate_count(self):
        for record in self:
            record.candidate_count = len(record.candidate_student_ids)

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

    def action_fill_random(self):
        for record in self.sudo():
            record._fill_random_candidate()

    def _fill_random_candidate(self):
        self.ensure_one()
        slot = max(
            self.capacity - (len(self.candidate_student_ids) + self.enrolled_count),
            0,
        )
        if not slot:
            return
        pool = (
            self.allowed_student_ids
            - self.candidate_student_ids
            - self.enrollment_ids.student_id
        )
        if not pool:
            return
        picked_ids = random.sample(pool.ids, min(slot, len(pool)))
        self.candidate_student_ids = [(4, sid) for sid in picked_ids]

    def action_generate_enrollments(self):
        for record in self.sudo():
            record._reconcile_enrollments()

    def _reconcile_enrollments(self):
        self.ensure_one()
        existing_enrollments = self._get_existing_enrollments()
        self._check_stale_non_draft_enrollments(existing_enrollments)
        self._remove_stale_draft_enrollments(existing_enrollments)
        self._enqueue_generate(existing_enrollments.exists())

    def _get_existing_enrollments(self):
        self.ensure_one()
        return self.env["school_enrollment"].search([("homeroom_id", "=", self.id)])

    def _check_stale_non_draft_enrollments(self, existing_enrollments):
        self.ensure_one()
        stale = existing_enrollments.filtered(
            lambda e: e.state != "draft"
            and e.student_id not in self.candidate_student_ids
        )
        if stale:
            error_message = (
                _(
                    """
Context: Generate Homeroom enrollments
Database ID: %s
Problem: Enrollment(s) %s are no longer in draft state, but their
student is not in Candidate Students
Solution: Add the student(s) back to Candidate Students, or
cancel/adjust the enrollment(s) manually before generating
"""
                )
                % (self.id, ", ".join(stale.mapped("name")))
            )
            raise ValidationError(error_message)

    def _remove_stale_draft_enrollments(self, existing_enrollments):
        self.ensure_one()
        stale = existing_enrollments.filtered(
            lambda e: e.state == "draft"
            and e.student_id not in self.candidate_student_ids
        )
        if stale:
            stale.unlink()

    def _enqueue_generate(self, existing_enrollments):
        self.ensure_one()
        students = self.candidate_student_ids - existing_enrollments.student_id
        for student in students:
            self.with_delay(
                description="Generate enrollment %s" % student.display_name
            )._generate_single_enrollment(student.id)

    def _generate_single_enrollment(self, student_id):
        self.ensure_one()
        existing = self.env["school_enrollment"].search(
            [
                ("homeroom_id", "=", self.id),
                ("student_id", "=", student_id),
            ]
        )
        if existing:
            return existing
        enrollment = self.env["school_enrollment"].create(
            self._prepare_enrollment_vals(student_id)
        )
        if enrollment.payment_template_id:
            enrollment.action_compute_payment()
        return enrollment

    def _get_default_payment_template(self):
        self.ensure_one()
        domain = [
            ("academic_term_id", "in", [self.academic_term_id.id, False]),
            ("school_id", "in", [self.school_id.id, False]),
            ("grade_id", "in", [self.grade_id.id, False]),
            ("is_default", "=", True),
        ]
        return self.env["school_enrollment_payment_template"].search(domain, limit=1)

    def _prepare_enrollment_vals(self, student_id):
        self.ensure_one()
        return {
            "date": self.date,
            "academic_year_id": self.academic_year_id.id,
            "academic_term_id": self.academic_term_id.id,
            "school_id": self.school_id.id,
            "grade_id": self.grade_id.id,
            "grade_class_id": self.grade_class_id.id,
            "student_id": student_id,
            "homeroom_id": self.id,
            "payment_template_id": self._get_default_payment_template().id,
        }

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
            "fill_random_ok",
            "generate_enrollments_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
