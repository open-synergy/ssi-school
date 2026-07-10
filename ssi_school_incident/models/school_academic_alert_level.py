# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolAcademicAlertLevel(models.Model):
    """
    Represents one tier of the Three-Color Academic Warning System (Bab 8.3
    of the YPII Incident & Parent Complaint Handling Guideline v2.0):
    Yellow, Orange, or Red. The guideline's own example triggers are
    grade-based (e.g. 2 subjects below 60, 3 subjects below 60, 4 subjects
    below 50), but this model deliberately does **not** hard-code any
    grade-reading logic: each level owns a ``python_code`` expression
    evaluated with ``safe_eval`` against the localdict supplied by the
    ``school_academic_alert`` document being evaluated (the same mechanism
    used by ``mixin.many2one_configurator``'s ``python_code`` strategy, via
    the ``mixin.localdict`` this model also inherits), so every school unit
    can define its own formula without touching code.

    Levels are evaluated from the most severe down to the least severe
    (highest ``sequence`` first): the first level whose ``python_code``
    sets local variable ``result`` to a truthy value wins.
    """

    _name = "school_academic_alert_level"
    _inherit = [
        "mixin.master_data",
        "mixin.localdict",
    ]
    _description = "Academic Alert Level"
    _order = "sequence desc, id"

    color = fields.Selection(
        string="Color",
        selection=[
            ("yellow", "Yellow"),
            ("orange", "Orange"),
            ("red", "Red"),
        ],
        required=True,
        help="Warning color of this level in the Three-Color Academic "
        "Warning System (Bab 8.3 of the YPII Guideline): Yellow = early "
        "warning, Orange = serious warning, Red = critical warning. Only "
        "Orange and Red levels are allowed to generate a School Incident "
        "from a School Academic Alert.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
        help="Severity ordering, NOT display ordering: higher value means "
        "a MORE severe level, and levels are evaluated from the highest "
        "sequence down to the lowest so the most severe rule is always "
        "checked first. The first level whose Python Code triggers wins "
        "(e.g. Red=30, Orange=20, Yellow=10).",
    )
    python_code = fields.Text(
        string="Python Code",
        help="Python source evaluated with safe_eval against the localdict "
        "supplied by the School Academic Alert being evaluated (student, "
        "subject note, and any extra variables seeded by that alert's "
        "Evaluation Context). Must set a boolean local variable named "
        "'result' that decides whether this level is triggered. "
        "Example: result = trigger_count >= 2",
    )
    action_guideline = fields.Text(
        string="Action Guideline",
        help="Narrative description of the action the school is required "
        "to take when this level triggers (the 'Tindakan Sekolah' column "
        "of Bab 8.3 of the YPII Guideline), e.g. who must be notified and "
        "what meeting or intervention must follow.",
    )
    sla_text = fields.Char(
        string="SLA",
        help="Free-text description of the service-level agreement that "
        "applies once this level triggers, e.g. how soon the parent must "
        "be contacted or a meeting must be scheduled.",
    )
