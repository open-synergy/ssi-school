# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmLead(models.Model):  # pylint: disable=too-few-public-methods
    """
    Extends the CRM Lead model to associate leads with schools
    and prospective students for school admissions management.
    """

    _name = "crm.lead"
    _inherit = "crm.lead"
    _description = "CRM Lead"

    school_id = fields.Many2one(
        comodel_name="school",
        string="School",
        ondelete="restrict",
        help="The school associated with this lead.",
    )
    student_id = fields.Many2one(
        comodel_name="res.partner",
        string="Student",
        ondelete="restrict",
        help="The prospective student associated with this lead.",
    )
