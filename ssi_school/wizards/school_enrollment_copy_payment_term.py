# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SchoolEnrollmentWizardCopyPaymentTerm(models.TransientModel):
    """
    Wizard that copies all payment terms (and their detail lines) from one source
    enrollment to one or more target enrollments selected from the school_enrollment
    list view. Mode "replace" deletes the existing payment terms on each target before
    copying; mode "add" appends the source terms to each target's existing terms. Every
    target must be allowed by the copy_payment_term_ok policy (state and group,
    configurable via Policy Template) and must share the same academic term, school,
    and grade as the source. All targets are validated before any change is applied.
    """

    _name = "school_enrollment.wizard_copy_payment_term"
    _description = "Copy Payment Terms Between Enrollments"

    target_enrollment_ids = fields.Many2many(
        string="Target Enrollments",
        comodel_name="school_enrollment",
        relation="rel_school_enrollment_copy_payment_term_target",
        column1="wizard_id",
        column2="enrollment_id",
        readonly=True,
        help=(
            "Draft enrollments selected from the list view that will "
            "receive the copied payment terms."
        ),
    )
    source_enrollment_id = fields.Many2one(
        string="Source Enrollment",
        comodel_name="school_enrollment",
        required=True,
        domain="[('id', 'not in', target_enrollment_ids)]",
        help="The enrollment whose payment terms (and detail lines) will be copied.",
    )
    mode = fields.Selection(
        string="Mode",
        selection=[
            ("replace", "Replace"),
            ("add", "Add"),
        ],
        default="replace",
        required=True,
        help=(
            "Replace: delete existing payment terms on each target before copying. "
            "Add: append source terms to each target's existing terms."
        ),
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self.env.context.get("active_model") == "school_enrollment":
            active_ids = self.env.context.get("active_ids", [])
            res["target_enrollment_ids"] = [(6, 0, active_ids)]
        return res

    def action_copy_payment_term(self):
        for record in self.sudo():
            record._copy_payment_term()  # pylint: disable=protected-access
        return {"type": "ir.actions.act_window_close"}

    def _copy_payment_term(self):
        self.ensure_one()
        if not self.target_enrollment_ids:
            error_message = (
                _(
                    """
Context: Copy payment terms between enrollments
Database ID: %s
Problem: No target enrollment selected
Solution: Select at least one draft enrollment from the list view before running this wizard
"""
                )
                % (self.id,)
            )
            raise UserError(error_message)
        self._check_target_enrollments()
        source = self.source_enrollment_id
        for target in self.target_enrollment_ids:
            if self.mode == "replace":
                target.payment_term_ids.unlink()
            for term in source.payment_term_ids.sorted("sequence"):
                new_term = term.copy(
                    {
                        "enrollment_id": target.id,
                        "invoice_id": False,
                    }
                )
                new_term.detail_ids.write({"invoice_line_id": False})

    def _check_target_enrollments(self):
        self.ensure_one()
        source = self.source_enrollment_id
        problems = []
        for target in self.target_enrollment_ids:
            if not target.copy_payment_term_ok:
                problems.append(
                    _("- %s: not allowed to receive payment terms (check state/policy)")
                    % target.name
                )
            elif (
                target.academic_term_id != source.academic_term_id
                or target.school_id != source.school_id
                or target.grade_id != source.grade_id
            ):
                problems.append(
                    _("- %s: academic term/school/grade does not match the source")
                    % target.name
                )
        if problems:
            error_message = (
                _(
                    """
Context: Copy payment terms from enrollment '%s'
Database ID: %s
Problem: The following target enrollment(s) cannot receive payment terms:
%s
Solution: Deselect the listed enrollment(s), or make sure they are draft, allowed by
the copy payment term policy, and share the same academic term/school/grade as the
source
"""
                )
                % (
                    source.name,
                    self.id,
                    "\n".join(problems),
                )
            )
            raise UserError(error_message)
