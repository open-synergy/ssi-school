# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval

from odoo.addons.ssi_decorator import ssi_decorator

#: Alert level colors that are serious enough to justify creating a School
#: Incident from a School Academic Alert (Bab 8.3 of the YPII Guideline:
#: Orange = serious warning, Red = critical warning).
INCIDENT_ALLOWED_COLORS = ("orange", "red")


class SchoolAcademicAlert(models.Model):
    """
    Represents one run of the Three-Color Academic Warning System (Bab 8.3
    of the YPII Incident & Parent Complaint Handling Guideline v2.0): a
    check of a student's academic standing against the configurable
    ``school_academic_alert_level`` rules, so parents are warned early
    (Yellow/Orange/Red) instead of being surprised by a report card.

    The evaluation itself never hard-codes a grade-reading formula: it
    delegates to each ``school_academic_alert_level``'s ``python_code``
    (evaluated via ``mixin.localdict``'s safe-eval mechanism), optionally
    seeded with extra variables from this document's own
    ``evaluation_context``. Only Orange/Red outcomes are allowed to create
    a linked ``school_incident`` (via ``action_create_incident``). The
    approval workflow mirrors ``school_incident``'s: Draft -> Confirm ->
    Approve -> Open -> Done / Cancel.
    """

    _name = "school_academic_alert"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.localdict",
    ]
    _description = "School Academic Alert"

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

    date_alert = fields.Date(
        string="Alert Date",
        default=lambda r: datetime_date.today(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The date this academic warning check is being performed for "
            "the student. Used as the sequence date field when a document "
            "number is generated."
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
        help="The student whose academic standing is being evaluated.",
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
            "The student's homeroom class at the time of this alert, "
            "automatically derived from the student's active enrollment "
            "when the Student is selected."
        ),
    )
    subject_note = fields.Char(
        string="Subject Note",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "Free-text context for this alert, e.g. which subject(s) are "
            "below the passing grade. Also used as part of the auto-"
            "generated description when an Incident is created from this "
            "alert."
        ),
    )
    evaluation_context = fields.Text(
        string="Evaluation Context",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "Optional Python source, evaluated the same way as the "
            "Academic Alert Level's Python Code (safe_eval), used to seed "
            "extra local variables BEFORE the level rules run. This is "
            "how the actual grade-reading numbers get into the "
            "evaluation without this module hard-coding any grade "
            "formula: write plain assignments here, e.g. "
            "'trigger_count = 3', and reference 'trigger_count' (or "
            "whatever name chosen) from the Academic Alert Level's Python "
            "Code."
        ),
    )
    alert_level_id = fields.Many2one(
        string="Alert Level",
        comodel_name="school_academic_alert_level",
        readonly=True,
        copy=False,
        help=(
            "Academic Alert Level triggered by the last evaluation (via "
            "the Evaluate button). Left empty when no configured level "
            "triggers for the current Evaluation Context."
        ),
    )
    color = fields.Selection(
        string="Color",
        related="alert_level_id.color",
        store=True,
        readonly=True,
        compute_sudo=True,
        help=(
            "Warning color of the triggered Alert Level, kept in sync for "
            "use in list view decorations and search filters/group-by."
        ),
    )
    incident_id = fields.Many2one(
        string="Incident",
        comodel_name="school_incident",
        readonly=True,
        copy=False,
        help=(
            "School Incident created from this alert via the Create "
            "Incident button. Only ever set for Orange/Red alerts."
        ),
    )
    evaluate_ok = fields.Boolean(
        string="Can Evaluate",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help=(
            "Policy that determines whether this alert can be evaluated "
            "against the configured Academic Alert Levels, taking into "
            "account the current document state and the user's group, as "
            "configured in the Policy Template."
        ),
    )
    create_incident_ok = fields.Boolean(
        string="Can Create Incident",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help=(
            "Policy that determines whether a School Incident can be "
            "created from this alert, taking into account the current "
            "document state and the user's group, as configured in the "
            "Policy Template. Business rule enforcement (Orange/Red only) "
            "is separate and always applied regardless of this policy."
        ),
    )

    @api.onchange(
        "student_id",
    )
    def onchange_grade_class_id(self):
        self.grade_class_id = False
        if self.student_id:
            self.grade_class_id = self.student_id.grade_class_id

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
            "evaluate_ok",
            "create_incident_ok",
        ]
        res += policy_field
        return res

    def action_evaluate(self):
        for record in self.sudo():
            record._evaluate_alert_level()

    def _evaluate_alert_level(self):
        self.ensure_one()
        localdict = self._get_default_localdict()

        if self.evaluation_context:
            try:
                safe_eval(
                    self.evaluation_context,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
            except Exception as error:
                error_message = _(
                    """
Context: Evaluate Academic Alert
Database ID: %s
Problem: Evaluation Context could not be evaluated: %s
Solution: Fix the Evaluation Context so it is valid Python source that
only assigns local variables, e.g. 'trigger_count = 3'
"""
                    % (self.id, error)
                )
                raise UserError(error_message)

        triggered_level = self.env["school_academic_alert_level"]
        levels = self.env["school_academic_alert_level"].search(
            [], order="sequence desc"
        )
        for level in levels:
            # Discard any stale 'result' left over from a previous level's
            # evaluation so a level whose Python Code forgets to set
            # 'result' can never inherit a previous truthy value.
            localdict.pop("result", None)
            try:
                safe_eval(
                    level.python_code,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
            except Exception as error:
                error_message = _(
                    """
Context: Evaluate Academic Alert
Database ID: %s
Problem: Python Code of Academic Alert Level '%s' could not be evaluated: %s
Solution: Fix the Python Code of that Academic Alert Level so it sets a
boolean local variable named 'result'
"""
                    % (self.id, level.name, error)
                )
                raise UserError(error_message)
            if localdict.get("result"):
                triggered_level = level
                break

        self.alert_level_id = triggered_level.id if triggered_level else False

    def action_create_incident(self):
        result = None
        for record in self.sudo():
            result = record._create_incident()
        return result

    def _create_incident(self):
        self.ensure_one()
        color = self.alert_level_id.color
        if not self.alert_level_id or color not in INCIDENT_ALLOWED_COLORS:
            error_message = _(
                """
Context: Create Incident from Academic Alert
Database ID: %s
Problem: Creating an Incident is only allowed for Orange or Red alert
levels
Solution: Evaluate this alert first (button Evaluate) using an Evaluation
Context that triggers an Orange/Red Academic Alert Level, then try again
"""
                % (self.id,)
            )
            raise UserError(error_message)

        incident_type = self._get_academic_incident_type()
        incident = self.env["school_incident"].create(
            self._prepare_incident_data(incident_type)
        )
        self.incident_id = incident.id

        waction = self.env.ref("ssi_school_incident.school_incident_action").read()[0]
        waction.update(
            {
                "view_mode": "form",
                "views": [(False, "form")],
                "res_id": incident.id,
            }
        )
        return waction

    def _get_academic_incident_type(self):
        self.ensure_one()
        return self.env.ref("ssi_school_incident.school_incident_type_academic")

    def _prepare_incident_data(self, incident_type):
        self.ensure_one()
        description = _("Academic Alert (%s): %s") % (
            (self.alert_level_id.color or "").capitalize(),
            self.subject_note or self.alert_level_id.action_guideline or self.name,
        )
        return {
            "date_incident": self.date_alert,
            "student_id": self.student_id.id,
            "grade_class_id": self.grade_class_id.id,
            "incident_type_id": incident_type.id,
            "handling_level": incident_type.default_handling_level,
            "description": description,
        }

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
