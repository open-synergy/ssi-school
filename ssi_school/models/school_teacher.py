# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class SchoolTeacher(models.Model):
    """
    Represents a teacher or instructor in a school.
    The teacher is linked to a contact (res.partner) as the source of personal
    information such as address, phone number, and email. Address and contact
    fields are relayed from contact_id so changes can be made directly from
    the teacher form.
    """

    _name = "school_teacher"
    _inherit = ["mixin.master_data"]
    _description = "Teacher"

    contact_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
        required=True,
        ondelete="restrict",
        help="The contact (partner) representing the personal data of this teacher.",
    )
    image_1920 = fields.Image(
        related="contact_id.image_1920",
        store=False,
        readonly=False,
        help="Teacher photo, taken from the linked contact record.",
    )
    street = fields.Char(
        related="contact_id.street",
        store=True,
        readonly=False,
        help="Street address of the teacher, synchronized from the contact.",
    )
    street2 = fields.Char(
        related="contact_id.street2",
        store=True,
        readonly=False,
        help="Second line of the teacher's address, synchronized from the contact.",
    )
    zip = fields.Char(
        related="contact_id.zip",
        store=True,
        readonly=False,
        help="Postal code of the teacher's address, synchronized from the contact.",
    )
    city_id = fields.Many2one(
        related="contact_id.city_id",
        store=True,
        readonly=False,
        help="City of the teacher's address, synchronized from the contact.",
    )
    state_id = fields.Many2one(
        related="contact_id.state_id",
        store=True,
        readonly=False,
        help="Province/state of the teacher's address, synchronized from the contact.",
    )
    country_id = fields.Many2one(
        related="contact_id.country_id",
        store=True,
        readonly=False,
        help="Country of the teacher's address, synchronized from the contact.",
    )
    phone = fields.Char(
        related="contact_id.phone",
        store=True,
        readonly=False,
        help="Phone number of the teacher, synchronized from the contact.",
    )
    mobile = fields.Char(
        related="contact_id.mobile",
        store=True,
        readonly=False,
        help="Mobile number of the teacher, synchronized from the contact.",
    )
    email = fields.Char(
        related="contact_id.email",
        store=True,
        readonly=False,
        help="Email address of the teacher, synchronized from the contact.",
    )
