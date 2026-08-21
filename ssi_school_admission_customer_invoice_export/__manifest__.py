# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "School Admission - Customer Invoice Export",
    "version": "14.0.1.1.3",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_school_admission",
        "ssi_school_customer_invoice_export",
        "web_tour",
    ],
    "data": [
        # Security - access
        "security/ir_model_access/school_admission_wizard_create_invoice_export.xml",
        # Policy template
        "policy_template/school_admission.xml",
        # Views
        "views/school_admission.xml",
        "views/assets.xml",
        "wizards/school_admission_create_invoice_export.xml",
    ],
    "demo": [],
}
