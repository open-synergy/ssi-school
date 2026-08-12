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
        """Expose the first Teacher record of this employee.

        ``teacher_ids`` may technically hold several ``school_teacher``
        records pointing at the same employee; ``teacher_id`` keeps the
        first of them, or ``False`` when the employee has no Teacher
        yet. The create and open buttons rely on this field to decide
        whether a Teacher already exists.
        """
        for record in self:
            record.teacher_id = record.teacher_ids and record.teacher_ids[0] or False

    def action_create_teacher(self):
        """Create Teacher records for the selected employees.

        Meant to be launched from the Action menu of the Employee list
        view, typically on a multi-record selection: ``_create_teacher``
        is called as superuser on every employee, and employees that
        already have a Teacher are skipped instead of duplicated.
        Nothing is returned, so the client keeps the current view.
        """
        for record in self.sudo():
            record._create_teacher()

    def action_open_teacher(self):
        """Open the Teacher form of this employee.

        Builds the window action through ``_open_teacher`` for every
        record and returns the one produced for the last record, so the
        button is meant to be used on a single employee.

        :return: window action opening the Teacher in form view.
        """
        for record in self.sudo():
            result = record._open_teacher()
        return result

    def _create_teacher(self):
        """Create the Teacher of one employee unless it already exists.

        Returns the existing ``teacher_id`` untouched when the employee
        already has one, which is what makes ``action_create_teacher``
        safe to run twice on the same selection; otherwise a
        ``school_teacher`` record is created from
        ``_prepare_teacher_data``.

        :return: the existing or newly created ``school_teacher``.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        if self.teacher_id:
            return self.teacher_id
        return self.env["school_teacher"].create(self._prepare_teacher_data())

    def _open_teacher(self):
        """Build the window action showing this employee's Teacher.

        Reads the ``ssi_school.school_teacher_action`` window action and
        narrows it down to the form view of ``teacher_id``.

        :return: window action dictionary.
        :raises ValueError: ``self`` is not a single record.
        """
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
        """Build the values of the Teacher created from an employee.

        Reuses the employee's ``name``, takes its ``barcode`` as Teacher
        code with the ``/`` placeholder as fallback, and links the
        Teacher back through ``employee_id``. Extension point: override
        it to carry more employee data over to the Teacher.

        :return: dictionary of values for ``school_teacher.create``.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        return {
            "name": self.name,
            "code": self.barcode or "/",
            "employee_id": self.id,
        }
