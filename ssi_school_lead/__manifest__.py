# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "School Lead",
    "version": "14.0.1.13.0",
    "website": "https://simetri-sinergi.id",
    "author": (
        "PT. Simetri Sinergi Indonesia, "
        "OpenSynergy Indonesia, "
        "Odoo Community Association (OCA)"
    ),
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_lead",
        "ssi_partner",
        "ssi_school",
        "ssi_school_admission",
        "web_tour",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/crm_lead_create_admission_view.xml",
        "views/crm_lead_views.xml",
        "views/school_views.xml",
    ],
}
