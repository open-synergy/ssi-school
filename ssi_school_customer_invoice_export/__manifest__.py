# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "School - Customer Invoice Export",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_school",
        "ssi_customer_invoice_export",
    ],
    "data": [
        # Security - access
        "security/ir_model_access/school_enrollment_wizard_create_invoice_export.xml",
        # Policy template
        "policy_template/school_enrollment.xml",
        # Views
        "views/school_enrollment.xml",
        "wizards/school_enrollment_create_invoice_export.xml",
    ],
    "demo": [],
}
