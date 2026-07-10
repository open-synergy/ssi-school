# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "School Student Leave - Operating Unit",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    # pylint: disable=line-too-long
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia, Odoo Community Association (OCA)",  # noqa: B950
    # pylint: enable=line-too-long
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_school_student_leave",
        "ssi_operating_unit_mixin",
    ],
    "data": [
        "security/res_groups/school_student_leave.xml",
        "security/ir_rule/school_student_leave.xml",
        "views/school_student_leave.xml",
    ],
    "demo": [],
}
