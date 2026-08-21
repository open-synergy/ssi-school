# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date, datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator

#: Resolution statuses that represent a closed/resolved case (Lampiran 4 of
#: the YPII Incident & Parent Complaint Handling Guideline v2.0). Used by
#: the "date_resolved required" constraint and by the resolution-overdue
#: computation below.
RESOLVED_RESOLUTION_STATUSES = (
    "resolved_satisfied",
    "resolved_unsatisfied",
)


class SchoolIncident(models.Model):
    """
    Represents the Master Log entry required by the YPII Incident & Parent
    Complaint Handling Guideline (v2.0): one record per incident or parent
    complaint case, capturing the five mandatory elements WHO
    (student_id, parent_partner_id), WHAT (incident_type_id, description),
    WHEN (date_incident, date_first_contact), ACTION (action_taken), and
    STATUS (the workflow state below). Each case is worked through the
    3-tier handling framework (handling_level): Homeroom Teacher,
    Counselor/Vice Principal, or Principal, defaulted from the selected
    incident_type_id but always adjustable per case. The approval workflow
    uses multi-approval mixins: Draft → Confirm → Approve → Open →
    Done / Cancel.
    """

    _name = "school_incident"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
    ]
    _description = "School Incident"

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

    date_incident = fields.Date(
        string="Incident Date",
        default=lambda r: datetime_date.today(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The date the incident or parent complaint case occurred "
            "(Master Log column A)."
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
        help=(
            "The student involved in this incident case "
            "(Master Log column B/C, the WHO element)."
        ),
    )
    enrollment_id = fields.Many2one(
        string="Enrollment",
        comodel_name="school_enrollment",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The student's active (open) enrollment, automatically "
            "populated when the Student is selected."
        ),
    )
    grade_class_id = fields.Many2one(
        string="Grade Class",
        comodel_name="school_grade_class",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The student's homeroom class at the time of the incident, "
            "automatically derived from the student's active enrollment."
        ),
    )
    parent_partner_id = fields.Many2one(
        string="Parent/Guardian Contact",
        comodel_name="res.partner",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The parent or guardian contact to be notified about this "
            "case. Automatically defaulted from the student's Father, "
            "Mother, or Guardian contact (in that order of preference) "
            "when the Student is selected, but can still be changed "
            "manually."
        ),
    )
    incident_type_id = fields.Many2one(
        string="Incident Type",
        comodel_name="school_incident_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The category/type of incident or parent complaint being "
            "logged (Master Log column D)."
        ),
    )
    handling_level = fields.Selection(
        string="Handling Level",
        selection=[
            ("1", "Tier 1 - Homeroom Teacher"),
            ("2", "Tier 2 - Counselor/Vice Principal"),
            ("3", "Tier 3 - Principal"),
        ],
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The handling tier currently assigned to this case "
            "(Master Log column F). Automatically defaulted from the "
            "selected Incident Type, but can still be adjusted per case."
        ),
    )
    description = fields.Text(
        string="Description",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "One-sentence description of what happened "
            "(Master Log column E, the WHAT element)."
        ),
    )
    handled_by_id = fields.Many2one(
        string="Handled By",
        comodel_name="res.users",
        default=lambda self: self.env.user,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The staff member responsible for handling this case "
            "(Master Log column J). Defaults to the user who logged "
            "the case."
        ),
    )
    contact_method = fields.Selection(
        string="Contact Method",
        selection=[
            ("whatsapp", "WhatsApp"),
            ("phone", "Phone"),
            ("face_to_face", "Face to Face"),
            ("letter", "Letter"),
        ],
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The channel used to make first contact with the parties "
            "involved in this case (Master Log column I)."
        ),
    )
    date_first_contact = fields.Datetime(
        string="First Contact Date",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "Date and time the assigned handler first contacted the "
            "parties involved in this case (Master Log column H). "
            "Automatically kept in sync with the earliest entry in the "
            "Parent Contacts log below whenever that log is not empty; "
            "manually editable as a fallback while no log entries have "
            "been recorded yet."
        ),
    )
    parent_contact_ids = fields.One2many(
        string="Parent Contacts",
        comodel_name="school_incident_parent_contact",
        inverse_name="incident_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
            "confirm": [
                ("readonly", False),
            ],
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "History of every contact made with the parent/guardian for "
            "this case (WhatsApp, phone call, face-to-face meeting, "
            "etc.), following the Empathy -> Facts -> Solution "
            "communication framework. The earliest entry here "
            "automatically updates the First Contact Date field above."
        ),
    )
    parent_contact_count = fields.Integer(
        string="Parent Contact Count",
        compute="_compute_parent_contact_count",
        compute_sudo=True,
        help="Number of parent contact log entries recorded for this case.",
    )
    action_taken = fields.Text(
        string="Action Taken",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "Description of the concrete action(s) taken to handle "
            "this case (the ACTION element of the Master Log)."
        ),
    )
    resolution_status = fields.Selection(
        string="Resolution Status",
        selection=[
            ("resolved_satisfied", "Resolved - Satisfied"),
            ("resolved_unsatisfied", "Resolved - Unsatisfied"),
            ("in_progress", "In Progress"),
            ("not_resolved", "Not Resolved"),
            ("escalated", "Escalated"),
        ],
        default="in_progress",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
            "confirm": [
                ("readonly", False),
            ],
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Outcome of this case from the parent/guardian's side, as "
            "distinct from the document workflow state above (Lampiran 4 "
            "of the YPII Guideline). Resolved - Satisfied/Unsatisfied = "
            "the case is closed and the parent's satisfaction has been "
            "recorded, In Progress = still being handled, Not Resolved = "
            "handling concluded without resolving the case, Escalated = "
            "moved to a higher handling tier (the escalation transition "
            "itself is implemented separately)."
        ),
    )
    date_resolved = fields.Date(
        string="Resolution Date",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
            "confirm": [
                ("readonly", False),
            ],
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Date this case was resolved (Master Log column L). Required "
            "once Resolution Status is set to one of the Resolved values."
        ),
    )
    first_contact_deadline = fields.Datetime(
        string="First Contact Deadline",
        compute="_compute_first_contact_deadline",
        store=True,
        help=(
            "Latest date/time by which the assigned handler must make "
            "first contact with the parties involved, computed from the "
            "Incident Date plus the applicable First Contact SLA (taken "
            "from the Incident Type, or from the per-tier default when "
            "the Incident Type does not define one)."
        ),
    )
    resolution_deadline = fields.Datetime(
        string="Resolution Deadline",
        compute="_compute_resolution_deadline",
        store=True,
        help=(
            "Latest date/time by which this case must be resolved, "
            "computed from the Incident Date plus the applicable "
            "Resolution SLA for the assigned handling tier."
        ),
    )
    is_first_contact_overdue = fields.Boolean(
        string="First Contact Overdue",
        compute="_compute_is_first_contact_overdue",
        help=(
            "True when no First Contact Date has been recorded yet and "
            "the current date/time is past the First Contact Deadline."
        ),
    )
    is_resolution_overdue = fields.Boolean(
        string="Resolution Overdue",
        compute="_compute_is_resolution_overdue",
        help=(
            "True when the case has not reached a Resolved outcome yet "
            "and the current date/time is past the Resolution Deadline."
        ),
    )
    is_overdue = fields.Boolean(
        string="Overdue",
        compute="_compute_is_overdue",
        store=True,
        help=(
            "True when this case is overdue on either its First Contact "
            "or its Resolution SLA. Stored so it can be used in list view "
            "decorations and in search filters/group-by."
        ),
    )
    escalation_criteria_ids = fields.Many2many(
        string="Escalation Criteria",
        comodel_name="school_incident_escalation_criteria",
        relation="rel_school_incident_2_escalation_criteria",
        column1="incident_id",
        column2="criteria_id",
        help=(
            "Explicit criteria (Bab 8.7 of the YPII Guideline) selected as "
            "the justification for the most recent escalation of this "
            "case to a higher handling tier. Escalation is never "
            "automatic: at least one matching criterion must be selected "
            "here before the case can move up a tier."
        ),
    )
    escalation_reason = fields.Text(
        string="Escalation Reason",
        help=(
            "Narrative/chronology explaining why this case was escalated "
            "(Bab 8.8 of the YPII Guideline: what must be reported when "
            "a case moves to a higher handling tier)."
        ),
    )
    escalated_to_level = fields.Selection(
        string="Escalated To Level",
        selection=[
            ("2", "Level 2 - Counselor/Vice Principal"),
            ("3", "Level 3 - Principal"),
        ],
        readonly=True,
        help="Handling tier this case was moved to by its most recent escalation.",
    )
    escalated_by_id = fields.Many2one(
        string="Escalated By",
        comodel_name="res.users",
        readonly=True,
        help="User who performed the most recent escalation of this case.",
    )
    escalation_date = fields.Datetime(
        string="Escalation Date",
        readonly=True,
        help="Date and time of the most recent escalation of this case.",
    )
    escalate_ok = fields.Boolean(
        string="Can Escalate",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help=(
            "Policy that determines whether this case can be escalated "
            "to a higher handling tier (via the Escalate wizard), taking "
            "into account the current document state and the user's "
            "group, as configured in the Policy Template."
        ),
    )

    @api.model
    def _get_first_contact_sla_hour(self, handling_level):
        """Per-tier fallback for the First Contact SLA (in hours), used
        only when the selected Incident Type does not define its own
        ``first_contact_sla_hour``. Override this method in a downstream
        module to customize per-tier SLA policy without touching the
        base computation.
        """
        default_sla_hour_per_level = {
            "1": 24.0,
            "2": 2.0,
            "3": 2.0,
        }
        return default_sla_hour_per_level.get(handling_level, 24.0)

    @api.model
    def _get_resolution_sla_hour(self, handling_level):
        """Per-tier Resolution SLA (in hours). Override this method in a
        downstream module to customize per-tier SLA policy without
        touching the base computation.
        """
        default_sla_hour_per_level = {
            "1": 24.0,
            "2": 168.0,
            "3": 168.0,
        }
        return default_sla_hour_per_level.get(handling_level, 168.0)

    @api.depends(
        "date_incident",
        "handling_level",
        "incident_type_id",
        "incident_type_id.first_contact_sla_hour",
    )
    def _compute_first_contact_deadline(self):
        """Compute the First Contact Deadline for every record in self.

        Deadline = Incident Date at midnight plus the applicable First
        Contact SLA (hours), taken from ``incident_type_id.
        first_contact_sla_hour`` when set, otherwise from the per-tier
        fallback ``_get_first_contact_sla_hour``. Empty when Incident
        Date is not set.
        """
        for record in self:
            deadline = False
            if record.date_incident:
                sla_hour = record.incident_type_id.first_contact_sla_hour or 0.0
                if not sla_hour:
                    sla_hour = record._get_first_contact_sla_hour(record.handling_level)
                date_start = datetime.combine(record.date_incident, datetime.min.time())
                deadline = date_start + timedelta(hours=sla_hour)
            record.first_contact_deadline = deadline

    @api.depends(
        "date_incident",
        "handling_level",
    )
    def _compute_resolution_deadline(self):
        """Compute the Resolution Deadline for every record in self.

        Deadline = Incident Date at midnight plus the applicable
        Resolution SLA (hours) for the assigned handling tier, taken
        from ``_get_resolution_sla_hour``. Empty when Incident Date is
        not set.
        """
        for record in self:
            deadline = False
            if record.date_incident:
                sla_hour = record._get_resolution_sla_hour(record.handling_level)
                date_start = datetime.combine(record.date_incident, datetime.min.time())
                deadline = date_start + timedelta(hours=sla_hour)
            record.resolution_deadline = deadline

    @api.depends(
        "date_first_contact",
        "first_contact_deadline",
    )
    def _compute_is_first_contact_overdue(self):
        """Set True when First Contact is still missing past its deadline.

        ``is_first_contact_overdue`` is True only when
        ``date_first_contact`` is empty, ``first_contact_deadline`` is
        set, and the current date/time is already past that deadline.
        """
        now = fields.Datetime.now()
        for record in self:
            record.is_first_contact_overdue = bool(
                not record.date_first_contact
                and record.first_contact_deadline
                and now > record.first_contact_deadline
            )

    @api.depends(
        "resolution_status",
        "resolution_deadline",
    )
    def _compute_is_resolution_overdue(self):
        """Set True when the case is still unresolved past its deadline.

        ``is_resolution_overdue`` is True only when
        ``resolution_status`` is not one of
        ``RESOLVED_RESOLUTION_STATUSES``, ``resolution_deadline`` is
        set, and the current date/time is already past that deadline.
        """
        now = fields.Datetime.now()
        for record in self:
            record.is_resolution_overdue = bool(
                record.resolution_status not in RESOLVED_RESOLUTION_STATUSES
                and record.resolution_deadline
                and now > record.resolution_deadline
            )

    @api.depends(
        "is_first_contact_overdue",
        "is_resolution_overdue",
    )
    def _compute_is_overdue(self):
        """Set True when either the First Contact or Resolution SLA is
        breached.

        ``is_overdue`` is the OR of ``is_first_contact_overdue`` and
        ``is_resolution_overdue``, stored for use in list view
        decorations and search filters/group-by.
        """
        for record in self:
            record.is_overdue = bool(
                record.is_first_contact_overdue or record.is_resolution_overdue
            )

    @api.depends(
        "parent_contact_ids",
    )
    def _compute_parent_contact_count(self):
        """Count the Parent Contacts log entries of every record in self."""
        for record in self:
            record.parent_contact_count = len(record.parent_contact_ids)

    def _sync_date_first_contact_from_parent_contact(self):
        """Push ``date_first_contact`` from the earliest entry in
        ``parent_contact_ids`` (the parent contact log) whenever that log
        is not empty. Called by ``school_incident_parent_contact``'s
        ``create``/``write``/``unlink`` overrides whenever a contact log
        entry is added, changed, or removed. When the log is empty
        ``date_first_contact`` is left untouched so it keeps behaving as
        a plain manually-editable fallback field (as it did before this
        log was introduced).
        """
        for record in self:
            if record.parent_contact_ids:
                record.date_first_contact = min(
                    record.parent_contact_ids.mapped("contact_datetime")
                )

    @api.constrains(
        "resolution_status",
        "date_resolved",
    )
    def _check_date_resolved(self):
        """Require Resolution Date once Resolution Status is Resolved.

        :raises UserError: when ``resolution_status`` is one of
            ``RESOLVED_RESOLUTION_STATUSES`` while ``date_resolved`` is
            still empty
        """
        for record in self:
            if (
                record.resolution_status in RESOLVED_RESOLUTION_STATUSES
                and not record.date_resolved
            ):
                error_message = _(
                    """
Context: Set Resolution Status to a Resolved value
Database ID: %s
Problem: Resolution Date is empty while Resolution Status is Resolved
Solution: Fill in the Resolution Date field before saving
"""
                    % (record.id,)
                )
                raise UserError(error_message)

    @api.onchange(
        "student_id",
    )
    def onchange_enrollment_id(self):
        self.enrollment_id = False
        if self.student_id:
            self.enrollment_id = self.student_id.active_enrollment_id

    @api.onchange(
        "student_id",
    )
    def onchange_grade_class_id(self):
        self.grade_class_id = False
        if self.student_id:
            self.grade_class_id = self.student_id.grade_class_id

    @api.onchange(
        "student_id",
    )
    def onchange_parent_partner_id(self):
        self.parent_partner_id = False
        if self.student_id:
            self.parent_partner_id = (
                self.student_id.father_id
                or self.student_id.mother_id
                or self.student_id.guardian_id
            )

    @api.onchange(
        "incident_type_id",
    )
    def onchange_handling_level(self):
        self.handling_level = False
        if self.incident_type_id:
            self.handling_level = self.incident_type_id.default_handling_level

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
            "escalate_ok",
        ]
        res += policy_field
        return res

    def action_escalate(self, target_level, escalation_criteria_ids, escalation_reason):
        """Escalate every record in self to a higher handling tier.

        Called by the ``escalate_incident`` wizard. Runs as ``sudo()``
        so a user who only passed the ``escalate_ok`` policy check
        (evaluated by the caller) does not also need write access.

        :param target_level: target ``handling_level`` selection value
        :param escalation_criteria_ids: ``school_incident_escalation_
            criteria`` recordset justifying the escalation
        :param escalation_reason: narrative/chronology text
        """
        for record in self.sudo():
            record._escalate(target_level, escalation_criteria_ids, escalation_reason)

    def _escalate(self, target_level, escalation_criteria_ids, escalation_reason):
        """Validate and apply an escalation to a higher handling tier.

        :param target_level: target ``handling_level`` selection value
        :param escalation_criteria_ids: ``school_incident_escalation_
            criteria`` recordset justifying the escalation; must not be
            empty and every entry's ``target_level`` must match
        :param escalation_reason: narrative/chronology text
        :raises UserError: when no criteria is selected, or a selected
            criterion's Target Level does not match ``target_level``
        """
        self.ensure_one()
        if not escalation_criteria_ids:
            error_message = _(
                """
Context: Escalate incident to a higher handling tier
Database ID: %s
Problem: No escalation criteria selected
Solution: Select at least one escalation criterion that justifies moving
this case to the target handling tier
"""
                % (self.id,)
            )
            raise UserError(error_message)

        expected_target_level = {
            "2": "level_2",
            "3": "level_3",
        }.get(target_level)
        mismatched = escalation_criteria_ids.filtered(
            lambda criteria: criteria.target_level != expected_target_level
        )
        if mismatched:
            error_message = _(
                """
Context: Escalate incident to handling tier %s
Database ID: %s
Problem: The following escalation criteria do not target this tier:
%s
Solution: Deselect the listed criteria, or select only criteria whose
Target Level matches the tier being escalated to
"""
                % (
                    target_level,
                    self.id,
                    "\n".join("- %s" % criteria.name for criteria in mismatched),
                )
            )
            raise UserError(error_message)

        self.write(
            {
                "handling_level": target_level,
                "resolution_status": "escalated",
                "escalated_to_level": target_level,
                "escalated_by_id": self.env.user.id,
                "escalation_date": fields.Datetime.now(),
                "escalation_criteria_ids": [(6, 0, escalation_criteria_ids.ids)],
                "escalation_reason": escalation_reason,
            }
        )
        body = _(
            "Case escalated to handling tier %s.<br/>Criteria: %s<br/>Reason: %s"
        ) % (
            target_level,
            ", ".join(escalation_criteria_ids.mapped("name")),
            escalation_reason or "-",
        )
        self.message_post(body=body)

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
