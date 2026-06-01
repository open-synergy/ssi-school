# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "School Admission Lead",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": (
        "PT. Simetri Sinergi Indonesia, "
        "OpenSynergy Indonesia, "
        "Odoo Community Association (OCA)"
    ),
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_school_lead",
        "ssi_school_admission",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/crm_lead_create_admission_form.xml",
        "views/crm_lead.xml",
    ],
}
