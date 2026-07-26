# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """
    Exposes the company's Previous School M2O Configurator fields on the
    Settings screen, so administrators can change the selection method
    (manual/domain/code) without a code release.
    """

    _name = "res.config.settings"
    _inherit = "res.config.settings"

    previous_school_selection_method = fields.Selection(
        related="company_id.previous_school_selection_method",
        readonly=False,
    )
    previous_school_ids = fields.Many2many(
        comodel_name="res.partner",
        related="company_id.previous_school_ids",
        readonly=False,
    )
    previous_school_domain = fields.Text(
        related="company_id.previous_school_domain",
        readonly=False,
    )
    previous_school_python_code = fields.Text(
        related="company_id.previous_school_python_code",
        readonly=False,
    )
