# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    """Expose the national student number (NISN) on a contact.

    The value is not stored on ``res.partner`` itself. It is kept as a
    ``res.partner.id_number`` record whose category code is ``nisn``, and
    surfaced here as a ``Char`` field through the helper methods provided
    by ``partner_identification``.
    """

    _inherit = "res.partner"

    nisn = fields.Char(
        string="NISN",
        compute=lambda s: s._compute_identification(
            "nisn",
            "nisn",
        ),
        inverse=lambda s: s._inverse_identification(
            "nisn",
            "nisn",
        ),
        search=lambda s, *a: s._search_identification("nisn", *a),
        help="National student number (Nomor Induk Siswa Nasional) of this "
        "contact, stored as an ID number record under the NISN category. "
        "Emptying this field archives the related ID number record instead "
        "of deleting it, so the history is preserved. When the contact "
        "already has more than one ID number under the NISN category, "
        "writing through this field is rejected with a validation error and "
        "the ID Numbers tab must be used instead.",
    )
