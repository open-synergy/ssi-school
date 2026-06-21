# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "School - Operating Unit",
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
        "ssi_school",
        "ssi_operating_unit_mixin",
        "ssi_financial_accounting_operating_unit",
    ],
    "data": [
        # Security - transactional (school_enrollment)
        "security/res_groups/school_enrollment.xml",
        "security/ir_rule/school_enrollment.xml",
        # Security - master data (global OU rules)
        "security/ir_rule/school.xml",
        "security/ir_rule/school_grade_type.xml",
        "security/ir_rule/school_grade.xml",
        "security/ir_rule/school_grade_class.xml",
        "security/ir_rule/school_academic_year.xml",
        "security/ir_rule/school_academic_term.xml",
        "security/ir_rule/school_student.xml",
        "security/ir_rule/school_teacher.xml",
        # Views
        "views/school_enrollment.xml",
        "views/school.xml",
        "views/school_grade_type.xml",
        "views/school_grade.xml",
        "views/school_grade_class.xml",
        "views/school_academic_year.xml",
        "views/school_academic_term.xml",
        "views/school_student.xml",
        "views/school_teacher.xml",
    ],
    "demo": [],
}
