# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class SchoolStudent(models.Model):
    """
    Represents a student's data in a school.
    A student is linked to a contact entity (res.partner) as the source
    of personal data.
    The system automatically tracks the student's current grade (current_grade_id)
    and next grade (next_grade_id) based on the enrollment history.
    The student's state reflects their actual status, ranging from waiting for
    enrollment, actively enrolled, on leave, suspended, graduated, transferred,
    dropped out, resigned, or deceased.
    """

    _name = "school_student"
    _inherit = ["mixin.master_data"]
    _description = "Student"

    contact_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
        required=True,
        ondelete="restrict",
        help="The contact (partner) representing the personal data of this student.",
    )
    image_1920 = fields.Image(
        related="contact_id.image_1920",
        store=False,
        readonly=False,
        help="Student photo, taken from the linked contact record.",
    )
    street = fields.Char(
        related="contact_id.street",
        store=True,
        readonly=False,
        help="Street address of the student, synchronized from the contact.",
    )
    street2 = fields.Char(
        related="contact_id.street2",
        store=True,
        readonly=False,
        help="Second line of the student's address, synchronized from the contact.",
    )
    zip = fields.Char(
        related="contact_id.zip",
        store=True,
        readonly=False,
        help="Postal code of the student's address, synchronized from the contact.",
    )
    city_id = fields.Many2one(
        related="contact_id.city_id",
        store=True,
        readonly=False,
        help="City of the student's address, synchronized from the contact.",
    )
    state_id = fields.Many2one(
        related="contact_id.state_id",
        store=True,
        readonly=False,
        help="Province/state of the student's address, synchronized from the contact.",
    )
    country_id = fields.Many2one(
        related="contact_id.country_id",
        store=True,
        readonly=False,
        help="Country of the student's address, synchronized from the contact.",
    )
    phone = fields.Char(
        related="contact_id.phone",
        store=True,
        readonly=False,
        help="Phone number of the student, synchronized from the contact.",
    )
    mobile = fields.Char(
        related="contact_id.mobile",
        store=True,
        readonly=False,
        help="Mobile number of the student, synchronized from the contact.",
    )
    email = fields.Char(
        related="contact_id.email",
        store=True,
        readonly=False,
        help="Email address of the student, synchronized from the contact.",
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=True,
        ondelete="restrict",
        help="The school where this student is enrolled.",
    )
    initial_grade_type_id = fields.Many2one(
        string="Initial Grade Type",
        related="school_id.grade_type_id",
        store=True,
        help=(
            "The initial grade type from the school, "
            "automatically populated from school data."
        ),
    )
    initial_grade_id = fields.Many2one(
        string="Initial Grade",
        comodel_name="school_grade",
        required=False,
        help=(
            "The student's class when first entering school "
            "before having any enrollment history."
        ),
    )
    current_grade_id = fields.Many2one(
        string="Current Grade",
        comodel_name="school_grade",
        compute="_compute_current_grade_id",
        store=True,
        compute_sudo=True,
        help=(
            "The student's current grade, automatically computed "
            "based on completed (done) enrollment history."
        ),
    )
    current_grade_type_id = fields.Many2one(
        string="Current Grade Type",
        related="current_grade_id.type_id",
        store=True,
        help=(
            "The grade type of the student's current grade, "
            "derived from the active grade."
        ),
    )
    next_grade_id = fields.Many2one(
        string="Next Grade",
        comodel_name="school_grade",
        related=False,
        compute="_compute_next_grade_id",
        store=True,
        compute_sudo=True,
        help=(
            "The next grade for the student, automatically computed "
            "based on grade ordering and last enrollment result."
        ),
    )
    enrollment_ids = fields.One2many(
        string="Enrollments",
        comodel_name="school_enrollment",
        inverse_name="student_id",
        readonly=True,
        help="The complete enrollment history of this student.",
    )
    active_enrollment_id = fields.Many2one(
        string="Active Enrollment",
        comodel_name="school_enrollment",
        compute="_compute_active_enrollment_id",
        store=True,
        compute_sudo=True,
        help="The currently active enrollment (status open) of this student.",
    )
    grade_class_id = fields.Many2one(
        string="Grade Class",
        comodel_name="school_grade_class",
        related="active_enrollment_id.grade_class_id",
        store=True,
        help="The student's active homeroom class, derived from the active enrollment.",
    )

    # Family
    father_id = fields.Many2one(
        string="Father",
        comodel_name="res.partner",
        help="Contact data of the student's father.",
    )
    mother_id = fields.Many2one(
        string="Mother",
        comodel_name="res.partner",
        help="Contact data of the student's mother.",
    )
    guardian_id = fields.Many2one(
        string="Guardian",
        comodel_name="res.partner",
        help="Contact data of the student's guardian if parents cannot be reached.",
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
        help=(
            "Current status of the student, from waiting for enrollment "
            "to actively enrolled, graduated, or exited."
        ),
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
            record._set_to_draft()  # pylint: disable=protected-access

    def action_set_to_enroll(self):
        for record in self.sudo():
            record._set_to_enroll()  # pylint: disable=protected-access

    def action_set_to_on_leave(self):
        for record in self.sudo():
            record._set_to_on_leave()  # pylint: disable=protected-access

    def action_set_to_suspended(self):
        for record in self.sudo():
            record._set_to_suspended()  # pylint: disable=protected-access

    def action_set_to_graduate(self):
        for record in self.sudo():
            record._set_to_graduate()  # pylint: disable=protected-access

    def action_set_to_transferred(self):
        for record in self.sudo():
            record._set_to_transferred()  # pylint: disable=protected-access

    def action_set_to_dropped(self):
        for record in self.sudo():
            record._set_to_dropped()  # pylint: disable=protected-access

    def action_set_to_resigned(self):
        for record in self.sudo():
            record._set_to_resigned()  # pylint: disable=protected-access

    def action_set_to_deceased(self):
        for record in self.sudo():
            record._set_to_deceased()  # pylint: disable=protected-access

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
