# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolStudentMutation(models.Model):  # pylint: disable=too-few-public-methods
    """
    Extends School Student Mutation with single operating unit support,
    restricting each mutation record to one operating unit.
    """

    _name = "school_student_mutation"
    _inherit = [
        "school_student_mutation",
        "mixin.single_operating_unit",
    ]
