# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class SchoolTeacher(models.Model):
    _name = "school_teacher"
    _inherit = ["mixin.master_data"]
    _description = "Teacher"

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
