# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "School Admission + Promotion",
    "version": "14.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    "author": (
        "OpenSynergy Indonesia, "
        "PT. Simetri Sinergi Indonesia, "
        "Odoo Community Association (OCA)"
    ),
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_school_admission",
        "ssi_promotion",
    ],
    "data": [
        "views/school_admission.xml",
    ],
    "demo": [],
}
