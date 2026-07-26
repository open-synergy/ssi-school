# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    """
    Extends the company model with M2O Configurator fields used to
    restrict which partners can be selected as the previous school of a
    prospective student on a CRM lead, without requiring a code change.
    """

    _name = "res.company"
    _inherit = [
        "res.company",
        "mixin.many2one_configurator",
    ]

    previous_school_selection_method = fields.Selection(
        string="Previous School Selection Method",
        selection=[
            ("manual", "Manual"),
            ("domain", "Domain"),
            ("code", "Python Code"),
        ],
        default="domain",
        required=True,
        help=(
            "Method used to filter the partners that can be selected as "
            "the previous school of a prospective student on a CRM lead. "
            "Manual: select from a fixed list. Domain: filter using an "
            "Odoo domain expression. Python Code: compute the allowed "
            "partners programmatically."
        ),
    )
    previous_school_ids = fields.Many2many(
        string="Previous Schools",
        comodel_name="res.partner",
        relation="rel_res_company_2_previous_school",
        column1="company_id",
        column2="partner_id",
        help=(
            "Partners allowed as the previous school of a prospective "
            "student when the selection method is set to Manual."
        ),
    )
    previous_school_domain = fields.Text(
        string="Previous School Domain",
        default="[('is_company', '=', True), ('parent_id', '=', False)]",
        help=(
            "Odoo domain expression used to filter the partners allowed "
            "as the previous school of a prospective student when the "
            "selection method is Domain."
        ),
    )
    previous_school_python_code = fields.Text(
        string="Previous School Python Code",
        default="result = []",
        help=(
            "Python code that returns a recordset (or list of IDs) of "
            "partners allowed as the previous school of a prospective "
            "student when the selection method is Python Code."
        ),
    )
