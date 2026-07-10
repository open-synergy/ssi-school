# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "School Student Graduation - Operating Unit",
    "version": "14.0.1.2.0",
    "website": "https://simetri-sinergi.id",
    "author": (
        "OpenSynergy Indonesia, "
        "PT. Simetri Sinergi Indonesia, "
        "Odoo Community Association (OCA)"
    ),
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_school_student_graduation",
        "ssi_operating_unit_mixin",
    ],
    "data": [
        "security/res_groups/school_student_graduation.xml",
        "security/ir_rule/school_student_graduation.xml",
        "views/school_student_graduation.xml",
        "security/res_groups/school_student_graduation_batch.xml",
        "security/ir_rule/school_student_graduation_batch.xml",
        "views/school_student_graduation_batch.xml",
    ],
    "demo": [],
}
