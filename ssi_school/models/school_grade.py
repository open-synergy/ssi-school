# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class SchoolGrade(models.Model):
    """
    Represents a class level within an education level type.
    Defines the ordered sequence of class levels within a grade type,
    e.g. Grade 1, Grade 2, Grade 3 for Elementary. The system automatically
    computes and updates previous_grade_id and next_grade_id whenever grade
    data changes (create, write, unlink) to keep the ordering chain consistent.
    """

    _name = "school_grade"
    _inherit = ["mixin.master_data"]
    _description = "School Grade"
    _order = "type_id asc, sequence asc, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
        help=(
            "Order of the class level within the education level type. "
            "Lower values represent lower grades."
        ),
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="school_grade_type",
        required=True,
        ondelete="restrict",
        help="The education level type that this grade belongs to.",
    )
    previous_grade_id = fields.Many2one(
        string="Previous Grade",
        comodel_name="school_grade",
        compute=False,
        readonly=True,
        help=(
            "The previous grade in the ordering sequence, "
            "automatically computed and updated by the system."
        ),
    )
    next_grade_id = fields.Many2one(
        string="Next Grade",
        comodel_name="school_grade",
        compute=False,
        readonly=True,
        help=(
            "The next grade in the ordering sequence, "
            "automatically computed and updated by the system."
        ),
    )

    def write(self, values):
        """Rebuild the grade chain after an ordering change.

        Overridden because ``previous_grade_id`` and ``next_grade_id``
        are plain stored fields maintained by code instead of computes:
        a write touching ``type_id`` or ``sequence`` reorders the grades
        and would leave the chain stale, so ``_recompute_next_previous``
        is replayed on every grade of the database afterwards.

        :param values: field values handed over to the parent ``write``.
        :return: always ``True``.
        """
        _super = super(SchoolGrade, self)  # pylint: disable=super-with-arguments
        _super.write(values)
        if values.get("type_id", False) or values.get("sequence", False):
            self._recompute_next_previous()
        return True

    @api.model
    def create(self, values):
        """Rebuild the grade chain after a grade is inserted.

        Overridden because a grade inserted into an existing
        ``type_id`` shifts the ordering of its neighbours, whose
        ``previous_grade_id`` and ``next_grade_id`` are maintained by
        code; ``_recompute_next_previous`` is therefore replayed once
        the record exists.

        :param values: field values handed over to the parent
            ``create``.
        :return: the newly created ``school_grade`` record.
        """
        _super = super(SchoolGrade, self)  # pylint: disable=super-with-arguments
        result = _super.create(values)
        if values.get("type_id", False) or values.get("sequence", False):
            self._recompute_next_previous()
        return result

    def unlink(self):
        """Rebuild the grade chain after grades are deleted.

        Overridden because deleting a grade leaves its neighbours
        pointing at a record that no longer exists; once the deletion
        succeeded, ``_recompute_next_previous`` relinks the remaining
        grades of every type.

        :return: always ``True``.
        """
        _super = super(SchoolGrade, self)  # pylint: disable=super-with-arguments
        _super.unlink()
        self._recompute_next_previous()
        return True

    @api.model
    def _recompute_next_previous(self):
        """Relink the previous/next chain of every grade.

        Reads all ``school_grade`` records, groups them per ``type_id``
        and, following the model order (``sequence`` then ``id``),
        writes on each grade its predecessor as ``previous_grade_id``
        and its successor as ``next_grade_id``; the first and the last
        grade of a type get ``False``. It writes on the whole table, so
        it is meant to be called only from ``create``, ``write`` and
        ``unlink``.
        """
        grades = self.env["school_grade"].search([])
        for grade_type in grades.mapped("type_id"):
            type_grades = grades.filtered(lambda g, t=grade_type: g.type_id == t)
            for grade_index, record in enumerate(type_grades):
                if grade_index - 1 < 0:
                    previous_grade = False
                else:
                    previous_grade = type_grades[grade_index - 1]
                try:
                    next_grade = type_grades[grade_index + 1]
                except IndexError:
                    next_grade = False
                record.write(
                    {
                        "previous_grade_id": previous_grade
                        and previous_grade.id
                        or False,
                        "next_grade_id": next_grade and next_grade.id or False,
                    }
                )
