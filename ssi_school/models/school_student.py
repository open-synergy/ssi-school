# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class SchoolStudent(models.Model):
    _name = "school_student"
    _inherit = ["mixin.master_data"]
    _description = "Student"

    contact_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
        required=True,
        ondelete="restrict",
    )
    image_1920 = fields.Image(
        related="contact_id.image_1920",
        store=False,
        readonly=False,
    )
    street = fields.Char(
        related="contact_id.street",
        store=True,
        readonly=False,
    )
    street2 = fields.Char(
        related="contact_id.street2",
        store=True,
        readonly=False,
    )
    zip = fields.Char(
        related="contact_id.zip",
        store=True,
        readonly=False,
    )
    city_id = fields.Many2one(
        related="contact_id.city_id",
        store=True,
        readonly=False,
    )
    state_id = fields.Many2one(
        related="contact_id.state_id",
        store=True,
        readonly=False,
    )
    country_id = fields.Many2one(
        related="contact_id.country_id",
        store=True,
        readonly=False,
    )
    phone = fields.Char(
        related="contact_id.phone",
        store=True,
        readonly=False,
    )
    mobile = fields.Char(
        related="contact_id.mobile",
        store=True,
        readonly=False,
    )
    email = fields.Char(
        related="contact_id.email",
        store=True,
        readonly=False,
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=True,
        ondelete="restrict",
    )
    initial_grade_type_id = fields.Many2one(
        string="Initial Grade Type",
        related="school_id.grade_type_id",
        store=True,
    )
    initial_grade_id = fields.Many2one(
        string="Initial Grade",
        comodel_name="school_grade",
        required=False,
    )
    current_grade_id = fields.Many2one(
        string="Current Grade",
        comodel_name="school_grade",
        compute="_compute_current_grade_id",
        store=True,
        compute_sudo=True,
    )
    current_grade_type_id = fields.Many2one(
        string="Current Grade Type",
        related="current_grade_id.type_id",
        store=True,
    )
    next_grade_id = fields.Many2one(
        string="Next Grade",
        comodel_name="school_grade",
        related=False,
        compute="_compute_next_grade_id",
        store=True,
        compute_sudo=True,
    )
    enrollment_ids = fields.One2many(
        string="Enrollments",
        comodel_name="school_enrollment",
        inverse_name="student_id",
        readonly=True,
    )
    active_enrollment_id = fields.Many2one(
        string="Active Enrollment",
        comodel_name="school_enrollment",
        compute="_compute_active_enrollment_id",
        store=True,
        compute_sudo=True,
    )
    grade_class_id = fields.Many2one(
        string="Grade Class",
        comodel_name="school_grade_class",
        related="active_enrollment_id.grade_class_id",
        store=True,
    )

    # Family
    father_id = fields.Many2one(
        string="Father",
        comodel_name="res.partner",
    )
    mother_id = fields.Many2one(
        string="Mother",
        comodel_name="res.partner",
    )
    guardian_id = fields.Many2one(
        string="Guardian",
        comodel_name="res.partner",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Waiting for Enrollment"),
            ("enrol", "Enrolled"),
            ("on_leave", "Cuti / Penangguhan"),
            ("suspended", "Skorsing"),
            ("graduate", "Graduated"),
            ("transferred", "Mutasi Keluar"),
            ("dropped", "Dikeluarkan / Drop Out"),
            ("resigned", "Mengundurkan Diri"),
            ("deceased", "Meninggal Dunia"),
        ],
        default="draft",
    )

    @api.depends("enrollment_ids", "enrollment_ids.state")
    def _compute_active_enrollment_id(self):
        for record in self:
            active_enrollment = record.enrollment_ids.filtered(
                lambda enrollment: enrollment.state == "open"
            )
            record.active_enrollment_id = (
                active_enrollment[:1].id if active_enrollment else False
            )

    @api.depends("initial_grade_id", "enrollment_ids", "enrollment_ids.state")
    def _compute_current_grade_id(self):
        for record in self:
            result = record.initial_grade_id
            criteria = [
                ("state", "in", ["open", "done"]),
                ("student_id", "=", record.id),
            ]
            enrollments = self.env["school_enrollment"].search(criteria)
            if len(enrollments) > 0:
                result = enrollments[-1].grade_id
            record.current_grade_id = result

    @api.depends(
        "initial_grade_id",
        "enrollment_ids",
        "enrollment_ids.state",
    )
    def _compute_next_grade_id(self):
        for record in self:
            result = False
            if not record.initial_grade_id and not record.enrollment_ids:
                result = self.env["school_grade"].search([])[0]
            elif record.initial_grade_id and not record.enrollment_ids:
                result = record.initial_grade_id.next_grade_id
            elif record.enrollment_ids:
                criteria = [
                    ("state", "=", "done"),
                    ("student_id", "=", record.id),
                ]
                enrollments = self.env["school_enrollment"].search(criteria)
                if len(enrollments) > 0:
                    last_enrollment = enrollments[-1]
                    if last_enrollment.last_term:
                        result = (
                            last_enrollment.promote_to_grade_id
                            or last_enrollment.grade_id
                        )
                    else:
                        result = last_enrollment.grade_id
            record.next_grade_id = result

    @api.onchange(
        "school_id",
    )
    def onchange_initial_grade_id(self):
        self.initial_grade_id = False

    def action_set_to_draft(self):
        for record in self.sudo():
            record._set_to_draft()

    def action_set_to_enroll(self):
        for record in self.sudo():
            record._set_to_enroll()

    def action_set_to_on_leave(self):
        for record in self.sudo():
            record._set_to_on_leave()

    def action_set_to_suspended(self):
        for record in self.sudo():
            record._set_to_suspended()

    def action_set_to_graduate(self):
        for record in self.sudo():
            record._set_to_graduate()

    def action_set_to_transferred(self):
        for record in self.sudo():
            record._set_to_transferred()

    def action_set_to_dropped(self):
        for record in self.sudo():
            record._set_to_dropped()

    def action_set_to_resigned(self):
        for record in self.sudo():
            record._set_to_resigned()

    def action_set_to_deceased(self):
        for record in self.sudo():
            record._set_to_deceased()

    def _set_to_draft(self):
        self.ensure_one()
        self.write(
            {
                "state": "draft",
            }
        )

    def _set_to_enroll(self):
        self.ensure_one()
        self.write(
            {
                "state": "enrol",
            }
        )

    def _set_to_on_leave(self):
        self.ensure_one()
        self.write(
            {
                "state": "on_leave",
            }
        )

    def _set_to_suspended(self):
        self.ensure_one()
        self.write(
            {
                "state": "suspended",
            }
        )

    def _set_to_graduate(self):
        self.ensure_one()
        self.write(
            {
                "state": "graduate",
            }
        )

    def _set_to_transferred(self):
        self.ensure_one()
        self.write(
            {
                "state": "transferred",
            }
        )

    def _set_to_dropped(self):
        self.ensure_one()
        self.write(
            {
                "state": "dropped",
            }
        )

    def _set_to_resigned(self):
        self.ensure_one()
        self.write(
            {
                "state": "resigned",
            }
        )

    def _set_to_deceased(self):
        self.ensure_one()
        self.write(
            {
                "state": "deceased",
            }
        )
