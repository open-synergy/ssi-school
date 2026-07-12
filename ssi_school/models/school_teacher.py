# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class SchoolTeacher(models.Model):  # pylint: disable=too-few-public-methods
    """
    Represents a teacher or instructor in a school.
    The teacher is linked to an employee (hr.employee) as the source of
    personal information such as address, phone number, email, and other
    personal data. Address, contact, and personal fields are relayed from
    employee_id.address_home_id (the employee's Home Address) so changes
    can be made directly from the teacher form.
    """

    _name = "school_teacher"
    _inherit = ["mixin.master_data"]
    _description = "Teacher"

    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        required=True,
        ondelete="restrict",
        help="The employee record representing this teacher.",
    )
    image_1920 = fields.Image(
        related="employee_id.address_home_id.image_1920",
        store=False,
        readonly=False,
        help="Teacher photo, taken from the employee's home address.",
    )
    street = fields.Char(
        related="employee_id.address_home_id.street",
        store=True,
        readonly=False,
        help=(
            "Street address of the teacher, synchronized from the "
            "employee's home address."
        ),
    )
    street2 = fields.Char(
        related="employee_id.address_home_id.street2",
        store=True,
        readonly=False,
        help=(
            "Second line of the teacher's address, synchronized from the "
            "employee's home address."
        ),
    )
    zip = fields.Char(
        related="employee_id.address_home_id.zip",
        store=True,
        readonly=False,
        help=(
            "Postal code of the teacher's address, synchronized from the "
            "employee's home address."
        ),
    )
    city_id = fields.Many2one(
        related="employee_id.address_home_id.city_id",
        store=True,
        readonly=False,
        help=(
            "City of the teacher's address, synchronized from the "
            "employee's home address."
        ),
    )
    state_id = fields.Many2one(
        related="employee_id.address_home_id.state_id",
        store=True,
        readonly=False,
        help=(
            "Province/state of the teacher's address, synchronized from "
            "the employee's home address."
        ),
    )
    country_id = fields.Many2one(
        related="employee_id.address_home_id.country_id",
        store=True,
        readonly=False,
        help=(
            "Country of the teacher's address, synchronized from the "
            "employee's home address."
        ),
    )
    phone = fields.Char(
        related="employee_id.address_home_id.phone",
        store=True,
        readonly=False,
        help=(
            "Phone number of the teacher, synchronized from the "
            "employee's home address."
        ),
    )
    mobile = fields.Char(
        related="employee_id.address_home_id.mobile",
        store=True,
        readonly=False,
        help=(
            "Mobile number of the teacher, synchronized from the "
            "employee's home address."
        ),
    )
    email = fields.Char(
        related="employee_id.address_home_id.email",
        store=True,
        readonly=False,
        help=(
            "Email address of the teacher, synchronized from the "
            "employee's home address."
        ),
    )

    # Personal Information
    gender = fields.Selection(
        related="employee_id.address_home_id.gender",
        store=True,
        readonly=False,
        help=(
            "Gender of the teacher, synchronized from the employee's " "home address."
        ),
    )
    birthdate_date = fields.Date(
        related="employee_id.address_home_id.birthdate_date",
        store=True,
        readonly=False,
        help=(
            "Date of birth of the teacher, synchronized from the "
            "employee's home address."
        ),
    )
    age = fields.Integer(
        related="employee_id.address_home_id.age",
        readonly=True,
        help=(
            "Current age of the teacher, computed live from the "
            "employee's home address date of birth."
        ),
    )
    birth_city = fields.Char(
        related="employee_id.address_home_id.birth_city",
        store=True,
        readonly=False,
        help=(
            "City of birth of the teacher, synchronized from the "
            "employee's home address."
        ),
    )
    birth_state_id = fields.Many2one(
        related="employee_id.address_home_id.birth_state_id",
        store=True,
        readonly=False,
        help=(
            "State/province of birth of the teacher, synchronized from "
            "the employee's home address."
        ),
    )
    birth_country_id = fields.Many2one(
        related="employee_id.address_home_id.birth_country_id",
        store=True,
        readonly=False,
        help=(
            "Country of birth of the teacher, synchronized from the "
            "employee's home address."
        ),
    )
    nationality_id = fields.Many2one(
        related="employee_id.address_home_id.nationality_id",
        store=True,
        readonly=False,
        help=(
            "Nationality of the teacher, synchronized from the "
            "employee's home address."
        ),
    )
    blood_type = fields.Selection(
        related="employee_id.address_home_id.blood_type",
        store=True,
        readonly=False,
        help=(
            "ABO blood type of the teacher, synchronized from the "
            "employee's home address."
        ),
    )
    blood_type_rhesus = fields.Selection(
        related="employee_id.address_home_id.blood_type_rhesus",
        store=True,
        readonly=False,
        help=(
            "Rhesus blood type of the teacher, synchronized from the "
            "employee's home address."
        ),
    )
    religion_id = fields.Many2one(
        related="employee_id.address_home_id.religion_id",
        store=True,
        readonly=False,
        help=(
            "Religion of the teacher, synchronized from the employee's " "home address."
        ),
    )
    ethnicity_id = fields.Many2one(
        related="employee_id.address_home_id.ethnicity_id",
        store=True,
        readonly=False,
        help=(
            "Ethnicity of the teacher, synchronized from the employee's "
            "home address."
        ),
    )
    marital = fields.Selection(
        related="employee_id.address_home_id.marital",
        store=True,
        readonly=False,
        help=(
            "Marital status of the teacher, synchronized from the "
            "employee's home address."
        ),
    )

    # Bank Accounts
    bank_ids = fields.One2many(
        string="Bank Accounts",
        related="employee_id.address_home_id.bank_ids",
        readonly=False,
        help=(
            "Bank accounts of the teacher, managed through the "
            "employee's home address."
        ),
    )
