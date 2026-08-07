# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "School Health",
    "version": "14.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "ssi_school",
        "ssi_partner_health",
        "web_tour",
    ],
    "data": [
        "views/school_student.xml",
        "views/assets.xml",
    ],
    "demo": [],
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
}
