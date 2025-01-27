# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class SchoolGrade(models.Model):
    _name = "school_grade"
    _inherit = ["mixin.master_data"]
    _description = "School Grade"
    _order = "type_id asc, sequence asc, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="school_grade_type",
        required=True,
        ondelete="restrict",
    )
    previous_grade_id = fields.Many2one(
        strinng="Previous Grade",
        comodel_name="school_grade",
        compute=False,
        readonly=True,
    )
    next_grade_id = fields.Many2one(
        string="Next Grade",
        comodel_name="school_grade",
        compute=False,
        readonly=True,
    )

    def write(self, values):
        _super = super(SchoolGrade, self)
        _super.write(values)
        if values.get("type_id", False) or values.get("sequence", False):
            self._recompute_next_previous()
        return True

    @api.model
    def create(self, values):
        _super = super(SchoolGrade, self)
        result = _super.create(values)
        if values.get("type_id", False) or values.get("sequence", False):
            self._recompute_next_previous()
        return result

    def unlink(self):
        _super = super(SchoolGrade, self)
        _super.unlink()
        self._recompute_next_previous()
        return True

    @api.model
    def _recompute_next_previous(self):
        grades = self.env["school_grade"].search([])
        for record in grades:
            grade_index = grades.ids.index(record.id)
            try:
                if grade_index - 1 < 0:
                    previous_grade = False
                else:
                    previous_grade = grades[grade_index - 1]
            except BaseException:
                previous_grade = False
            try:
                next_grade = grades[grade_index + 1]
            except BaseException:
                next_grade = False
            record.write(
                {
                    "previous_grade_id": previous_grade and previous_grade.id or False,
                    "next_grade_id": next_grade and next_grade.id or False,
                }
            )
