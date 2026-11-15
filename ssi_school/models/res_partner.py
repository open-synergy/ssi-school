# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    """Expose the NISN and NUPTK identification numbers on a contact.

    The values are not stored on ``res.partner`` itself. Each is kept as
    a ``res.partner.id_number`` record whose category code is ``nisn`` or
    ``nuptk``, and surfaced here as a ``Char`` field through the helper
    methods provided by ``partner_identification``.
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
    nuptk = fields.Char(
        string="NUPTK",
        compute=lambda s: s._compute_identification(
            "nuptk",
            "nuptk",
        ),
        inverse=lambda s: s._inverse_identification(
            "nuptk",
            "nuptk",
        ),
        search=lambda s, *a: s._search_identification("nuptk", *a),
        help="Nomor Unik Pendidik dan Tenaga Kependidikan (NUPTK), the "
        "unique number of an educator or education staff member, stored "
        "as an ID number record under the NUPTK category. Emptying this "
        "field archives the related ID number record instead of deleting "
        "it, so the history is preserved. When the contact already has "
        "more than one ID number under the NUPTK category, writing "
        "through this field is rejected with a validation error and the "
        "ID Numbers tab must be used instead.",
    )
