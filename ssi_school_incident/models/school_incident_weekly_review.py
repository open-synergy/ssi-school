# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date, timedelta

from odoo import _, api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator

#: Resolution statuses treated as "still open / unresolved" for the
#: Agenda 3 checklist item of the Weekly Case Review (Bab 8 + Lampiran 3 of
#: the YPII Incident & Parent Complaint Handling Guideline v2.0): cases
#: that have neither been resolved nor already escalated to a higher
#: handling tier. "Escalated" is intentionally excluded here because an
#: escalated case has already received the elevated attention this
#: checklist item is meant to trigger; it is instead surfaced separately
#: via ``count_escalated`` / Agenda 5.
UNRESOLVED_RESOLUTION_STATUSES = (
    "in_progress",
    "not_resolved",
)


class SchoolIncidentWeeklyReview(models.Model):
    """
    Represents one run of the mandatory Weekly Case Review (Bab 8 +
    Lampiran 3 of the YPII Incident & Parent Complaint Handling Guideline
    v2.0): a max-30-minute Friday meeting that goes through a fixed
    checklist against the ``school_incident`` Master Log entries logged
    for a date range (optionally scoped to one School/unit). Incidents are
    never linked automatically nor edited from here: they are pulled in
    on demand via the Collect button (``action_collect_incidents``), which
    delegates to the overridable ``_get_incident_criteria`` domain so
    downstream modules (e.g. an Operating Unit glue module) can extend the
    scoping without touching this model directly.

    The workflow is intentionally the simplified 3-state pattern already
    used by ``school_student_mutation`` in the base ``ssi_school`` module
    (Draft -> Confirm -> Done, no separate Open state): a review is a
    lightweight, single-sitting audit document, not a multi-stage case
    that needs an in-progress "Open" state of its own. Approval moves the
    document directly from Confirm to Done (``_after_approved_method =
    "action_done"``).
    """

    _name = "school_incident_weekly_review"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
    ]
    _description = "School Incident Weekly Review"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
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
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "School/unit this Weekly Case Review is scoped to. Used by the "
            "Collect button to only pull in School Incidents whose "
            "Student belongs to this School. Leave empty to review all "
            "Schools/units together."
        ),
    )
    date_start = fields.Date(
        string="Date Start",
        default=lambda r: datetime_date.today() - timedelta(days=7),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "Start of the week (or other period) this review covers. "
            "School Incidents with an Incident Date on or after this date "
            "are eligible to be pulled in by the Collect button."
        ),
    )
    date_end = fields.Date(
        string="Date End",
        default=lambda r: datetime_date.today(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "End of the week (or other period) this review covers, "
            "normally the Friday the review meeting is held on. School "
            "Incidents with an Incident Date on or before this date are "
            "eligible to be pulled in by the Collect button. Also used as "
            "the reference 'as of' date for the Not Resolved > 7 days "
            "computation below, since a review can be filed in "
            "retrospect and should not depend on the date it happens to "
            "be opened/saved."
        ),
    )
    incident_ids = fields.Many2many(
        string="Incidents",
        comodel_name="school_incident",
        relation="rel_school_incident_weekly_review_2_incident",
        column1="review_id",
        column2="incident_id",
        readonly=True,
        copy=False,
        help=(
            "School Incident records included in this review. Never "
            "editable directly: populated only by the Collect button "
            "(action_collect_incidents), which re-runs the Date Start/"
            "Date End/School criteria and replaces the whole list. This "
            "keeps the review from being coupled to incident management "
            "itself -- it only ever reads/references incidents, never "
            "creates, edits, or cancels them."
        ),
    )
    count_total = fields.Integer(
        string="Total Incidents",
        compute="_compute_count_total",
        store=True,
        compute_sudo=True,
        help="Total number of School Incidents currently collected into this review.",
    )
    count_overdue = fields.Integer(
        string="Overdue Incidents",
        compute="_compute_count_overdue",
        store=True,
        compute_sudo=True,
        help=(
            "Number of collected School Incidents whose Overdue flag "
            "(is_overdue, either on First Contact or on Resolution SLA) "
            "is currently set. Backs the 'SLA-breaching cases identified' "
            "checklist item."
        ),
    )
    count_unresolved_over_7d = fields.Integer(
        string="Not Resolved > 7 Days",
        compute="_compute_count_unresolved_over_7d",
        store=True,
        compute_sudo=True,
        help=(
            "Number of collected School Incidents that are still 'In "
            "Progress' or 'Not Resolved' (i.e. not yet Resolved and not "
            "yet Escalated) whose Incident Date is more than 7 days "
            "before Date End. Date End (not today's real date) is used "
            "as the 'as of' reference so a review filed in retrospect "
            "computes the same result it would have on the day it was "
            "held. Backs the 'cases Not Resolved for more than 7 days "
            "flagged' checklist item."
        ),
    )
    count_escalated = fields.Integer(
        string="Escalated Incidents",
        compute="_compute_count_escalated",
        store=True,
        compute_sudo=True,
        help=(
            "Number of collected School Incidents whose Resolution "
            "Status is 'Escalated'. Used as supporting evidence for the "
            "Agenda 5 escalation-criteria compliance audit checklist item."
        ),
    )
    chk_master_log_updated = fields.Boolean(
        string="Master Log Updated",
        help=(
            "Confirms that the school_incident Master Log has been kept "
            "up to date for the period under review (Agenda 1 of the "
            "Weekly Case Review): every case that occurred in the period "
            "has a corresponding School Incident record."
        ),
    )
    chk_unresolved_over_7d_flagged = fields.Boolean(
        string="Not Resolved > 7 Days Flagged",
        help=(
            "Confirms that every case counted in 'Not Resolved > 7 Days' "
            "above (Agenda 2) has actually been flagged/escalated to the "
            "handler and/or their supervisor for follow-up, not merely "
            "observed in this review."
        ),
    )
    chk_sla_breach_identified = fields.Boolean(
        string="SLA Breach Identified",
        help=(
            "Confirms that every case counted in 'Overdue Incidents' "
            "above (Agenda 3, First Contact or Resolution SLA breach) "
            "has been identified and communicated to the relevant "
            "handling tier."
        ),
    )
    chk_escalation_criteria_audited = fields.Boolean(
        string="Escalation Criteria Audited",
        help=(
            "Agenda 5 (v2.0): manual confirmation that the officer has "
            "audited every Escalated case in the Incidents list below and "
            "verified it complies with Bab 8.7 -- i.e. each one has at "
            "least one Escalation Criteria entry recorded as its "
            "justification. 'Compliance' here means no case was moved to "
            "a higher handling tier without at least one matching, "
            "recorded criterion; this checkbox does not enforce that by "
            "itself, it only records that the manual audit was performed."
        ),
    )
    chk_health_summary_available = fields.Boolean(
        string="Health Case Summary Available",
        help=(
            "Agenda 6 (v2.0): confirms that a summary of this period's "
            "health-related cases (School Incidents whose Incident Type "
            "is flagged is_health) has been prepared and reviewed, so "
            "health trends are not lost inside the general incident log."
        ),
    )
    note = fields.Text(
        string="Note",
        help=(
            "Free-text minutes or follow-up notes from this Weekly Case "
            "Review meeting."
        ),
    )
    collect_ok = fields.Boolean(
        string="Can Collect",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help=(
            "Policy that determines whether the Incidents list can be "
            "(re)collected via the Collect button, taking into account "
            "the current document state and the user's group, as "
            "configured in the Policy Template."
        ),
    )

    @api.depends(
        "incident_ids",
    )
    def _compute_count_total(self):
        """Count the collected School Incidents for each record in self."""
        for record in self:
            record.count_total = len(record.incident_ids)

    @api.depends(
        "incident_ids.is_overdue",
    )
    def _compute_count_overdue(self):
        """Count the collected incidents whose ``is_overdue`` is set."""
        for record in self:
            record.count_overdue = len(record._get_overdue_incidents())

    def _get_overdue_incidents(self):
        """Return the collected incidents whose ``is_overdue`` is set.

        :return: ``school_incident`` recordset
        """
        self.ensure_one()
        return self.incident_ids.filtered("is_overdue")

    @api.depends(
        "incident_ids.resolution_status",
    )
    def _compute_count_escalated(self):
        """Count the collected incidents whose Resolution Status is
        Escalated.
        """
        for record in self:
            record.count_escalated = len(record._get_escalated_incidents())

    def _get_escalated_incidents(self):
        """Return the collected incidents whose Resolution Status is
        Escalated.

        :return: ``school_incident`` recordset
        """
        self.ensure_one()
        return self.incident_ids.filtered(
            lambda incident: incident.resolution_status == "escalated"
        )

    @api.depends(
        "incident_ids.resolution_status",
        "incident_ids.date_incident",
        "date_end",
    )
    def _compute_count_unresolved_over_7d(self):
        """Count collected incidents unresolved for more than 7 days.

        Delegates to ``_get_unresolved_over_7d_incidents`` for the
        actual selection rule.
        """
        for record in self:
            record.count_unresolved_over_7d = len(
                record._get_unresolved_over_7d_incidents()
            )

    def _get_unresolved_over_7d_incidents(self):
        """Overridable so downstream modules can adjust which resolution
        statuses count as "still unresolved" or the 7-day threshold
        itself without touching the base computation.
        """
        self.ensure_one()
        if not self.date_end:
            return self.env["school_incident"]
        threshold_date = self.date_end - timedelta(days=7)
        return self.incident_ids.filtered(
            lambda incident: incident.resolution_status
            in UNRESOLVED_RESOLUTION_STATUSES
            and incident.date_incident
            and incident.date_incident <= threshold_date
        )

    def _get_incident_criteria(self):
        """Domain used by the Collect button to search for eligible
        ``school_incident`` records. Kept as a plain overridable method
        (not a decorated hook) so downstream modules -- e.g. a future
        Operating Unit glue module -- can extend the scoping (for
        instance, restrict it further by the user's allowed operating
        units) by calling ``super()._get_incident_criteria()`` and adding
        to the returned list.
        """
        self.ensure_one()
        criteria = [
            ("date_incident", ">=", self.date_start),
            ("date_incident", "<=", self.date_end),
        ]
        if self.school_id:
            criteria.append(("student_id.school_id", "=", self.school_id.id))
        return criteria

    def action_collect_incidents(self):
        """(Re)collect incidents into every record in self.

        Runs as ``sudo()`` so a user who only passed the
        ``collect_ok`` policy check does not also need read access to
        every matched ``school_incident``.
        """
        for record in self.sudo():
            record._collect_incidents()

    def _collect_incidents(self):
        """Re-run ``_get_incident_criteria`` and replace ``incident_ids``.

        Fully replaces the current list with the fresh search result
        (never merges), so a Collect after Date Start/Date End/School
        changes always reflects only the current criteria.
        """
        self.ensure_one()
        incidents = self.env["school_incident"].search(self._get_incident_criteria())
        self.write({"incident_ids": [(6, 0, incidents.ids)]})

    def action_view_total_incidents(self):
        """Open the collected incidents in a list/form action.

        Runs as ``sudo()`` so a user who only passed a read-oriented
        policy check does not also need read access to
        ``school_incident``.

        :return: an ``ir.actions.act_window`` dict
        """
        result = None
        for record in self.sudo():
            result = record._view_total_incidents()
        return result

    def _view_total_incidents(self):
        """Build the stat action for every collected incident.

        :return: an ``ir.actions.act_window`` dict
        """
        self.ensure_one()
        return self._prepare_incident_stat_action(self.incident_ids)

    def action_view_overdue_incidents(self):
        """Open the collected overdue incidents in a list/form action.

        Runs as ``sudo()``, same rationale as
        ``action_view_total_incidents``.

        :return: an ``ir.actions.act_window`` dict
        """
        result = None
        for record in self.sudo():
            result = record._view_overdue_incidents()
        return result

    def _view_overdue_incidents(self):
        """Build the stat action for the collected overdue incidents.

        :return: an ``ir.actions.act_window`` dict
        """
        self.ensure_one()
        return self._prepare_incident_stat_action(self._get_overdue_incidents())

    def action_view_unresolved_over_7d_incidents(self):
        """Open the collected Not Resolved > 7 Days incidents.

        Runs as ``sudo()``, same rationale as
        ``action_view_total_incidents``.

        :return: an ``ir.actions.act_window`` dict
        """
        result = None
        for record in self.sudo():
            result = record._view_unresolved_over_7d_incidents()
        return result

    def _view_unresolved_over_7d_incidents(self):
        """Build the stat action for the Not Resolved > 7 Days incidents.

        :return: an ``ir.actions.act_window`` dict
        """
        self.ensure_one()
        return self._prepare_incident_stat_action(
            self._get_unresolved_over_7d_incidents()
        )

    def action_view_escalated_incidents(self):
        """Open the collected escalated incidents in a list/form action.

        Runs as ``sudo()``, same rationale as
        ``action_view_total_incidents``.

        :return: an ``ir.actions.act_window`` dict
        """
        result = None
        for record in self.sudo():
            result = record._view_escalated_incidents()
        return result

    def _view_escalated_incidents(self):
        """Build the stat action for the collected escalated incidents.

        :return: an ``ir.actions.act_window`` dict
        """
        self.ensure_one()
        return self._prepare_incident_stat_action(self._get_escalated_incidents())

    def _prepare_incident_stat_action(self, incidents):
        """Build a tree/form action showing exactly ``incidents``.

        Reuses ``school_incident_action`` as a base, then overrides
        its domain/name/views so it opens scoped to the given
        recordset instead of the full Incidents list.

        :param incidents: ``school_incident`` recordset to show
        :return: an ``ir.actions.act_window`` dict
        """
        self.ensure_one()
        waction = self.env.ref("ssi_school_incident.school_incident_action").read()[0]
        waction.update(
            {
                "name": _("Incidents"),
                "view_mode": "tree,form",
                "views": [
                    (False, "tree"),
                    (False, "form"),
                ],
                "domain": [("id", "in", incidents.ids)],
                "context": {},
            }
        )
        return waction

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "done_ok",
            "cancel_ok",
            "manual_number_ok",
            "collect_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
