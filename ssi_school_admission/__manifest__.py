# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "School Admission",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_school",
    ],
    "data": [
        "res_group/res_group.xml",
        "ir_model_access/school_admission_period.xml",
        "views/school_admission_period.xml",
    ],
    "demo": [
        "demo/school_admission_period.xml",
    ],
}
