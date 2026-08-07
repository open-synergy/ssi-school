# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "School Student Graduation",
    "version": "14.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    # pylint: disable=line-too-long
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia, Odoo Community Association (OCA)",  # noqa: B950
    # pylint: enable=line-too-long
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "ssi_school",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_decorator",
    ],
    "data": [
        "security/ir_module_category/school_student_graduation.xml",
        "security/ir_module_category/school_student_graduation_batch.xml",
        "security/res_group/school_student_graduation.xml",
        "security/res_group/school_student_graduation_batch.xml",
        "security/ir_model_access/school_student_graduation.xml",
        "security/ir_model_access/school_student_graduation_batch.xml",
        "security/ir_rule/school_student_graduation.xml",
        "security/ir_rule/school_student_graduation_batch.xml",
        "ir_sequence/school_student_graduation.xml",
        "ir_sequence/school_student_graduation_batch.xml",
        "sequence_template/school_student_graduation.xml",
        "sequence_template/school_student_graduation_batch.xml",
        "policy_template/school_student_graduation.xml",
        "policy_template/school_student_graduation_batch.xml",
        "approval_template/school_student_graduation.xml",
        "approval_template/school_student_graduation_batch.xml",
        "views/school_student_graduation.xml",
        "views/school_student_graduation_batch.xml",
        "views/assets.xml",
    ],
}
