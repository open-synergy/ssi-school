# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "School Admission - Operating Unit",
    "version": "14.0.1.3.0",
    "website": "https://simetri-sinergi.id",
    "author": (
        "PT. Simetri Sinergi Indonesia, "
        "OpenSynergy Indonesia, "
        "Odoo Community Association (OCA)"
    ),
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_school_admission",
        "ssi_operating_unit_mixin",
        "ssi_financial_accounting_operating_unit",
    ],
    "data": [
        "security/res_groups/school_admission.xml",
        "security/res_groups/school_admission_form.xml",
        "security/res_groups/school_admission_test.xml",
        "security/ir_rule/school_admission.xml",
        "security/ir_rule/school_admission_form.xml",
        "security/ir_rule/school_admission_test.xml",
        "views/school_admission.xml",
        "views/school_admission_form.xml",
        "views/school_admission_test.xml",
    ],
    "demo": [],
}
