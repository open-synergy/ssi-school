# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrEmployee(models.Model):
    """
    Extension of hr.employee to generate school_teacher records.

    Adds the ability to bulk-create Teacher records from selected employees
    (via the Action menu on the Employee list view), guarded so employees
    that already have a Teacher are skipped instead of duplicated.
    """

    _inherit = "hr.employee"

    teacher_ids = fields.One2many(
        string="Teachers",
        comodel_name="school_teacher",
        inverse_name="employee_id",
        help="Teacher records created from this employee.",
    )
    teacher_id = fields.Many2one(
        string="Teacher",
        comodel_name="school_teacher",
        compute="_compute_teacher_id",
        compute_sudo=True,
        store=True,
        help="Teacher record representing this employee, if any.",
    )

    @api.depends("teacher_ids")
    def _compute_teacher_id(self):
        for record in self:
            record.teacher_id = record.teacher_ids and record.teacher_ids[0] or False

    def action_create_teacher(self):
        for record in self.sudo():
            record._create_teacher()

    def action_open_teacher(self):
        for record in self.sudo():
            result = record._open_teacher()
        return result

    def _create_teacher(self):
        self.ensure_one()
        if self.teacher_id:
            return self.teacher_id
        return self.env["school_teacher"].create(self._prepare_teacher_data())

    def _open_teacher(self):
        self.ensure_one()
        waction = self.env.ref("ssi_school.school_teacher_action").read()[0]
        waction.update(
            {
                "view_mode": "form",
                "res_id": self.teacher_id.id,
                "views": [(False, "form")],
            }
        )
        return waction

    def _prepare_teacher_data(self):
        self.ensure_one()
        return {
            "name": self.name,
            "code": self.barcode or "/",
            "employee_id": self.id,
        }
