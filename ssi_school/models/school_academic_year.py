# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolAcademicYear(models.Model):  # pylint: disable=too-few-public-methods
    """
    Represents an academic year of a school.
    An academic year defines a full year of study consisting of one or more
    semesters/terms. The system automatically determines the first (first_term_id)
    and last (last_term_id) term based on the one2many relation to
    school_academic_term. This information is used by enrollment to
    determine whether a student is in the first or a subsequent term.
    """

    _name = "school_academic_year"
    _inherit = ["mixin.master_data"]
    _description = "School Academic Year"
    _order = "date_start asc, id asc"

    date_start = fields.Date(
        string="Date Start",
        required=True,
        help="The start date of this academic year.",
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
        help="The end date of this academic year.",
    )
    term_ids = fields.One2many(
        string="Terms",
        comodel_name="school_academic_term",
        inverse_name="year_id",
        readonly=True,
        help="List of semesters/terms belonging to this academic year.",
    )
    first_term_id = fields.Many2one(
        string="First Term",
        comodel_name="school_academic_term",
        compute="_compute_first_last_term",
        store=True,
        compute_sudo=True,
        help="The first term of the academic year, automatically computed.",
    )
    last_term_id = fields.Many2one(
        string="Last Term",
        comodel_name="school_academic_term",
        compute="_compute_first_last_term",
        store=True,
        compute_sudo=True,
        help="The last term of the academic year, automatically computed.",
    )

    @api.depends(
        "term_ids",
    )
    def _compute_first_last_term(self):
        """Pick the opening and closing term of the academic year.

        ``term_ids`` is read in the model order of
        ``school_academic_term`` (year, then ``date_start``, then
        ``id``), so its first element becomes ``first_term_id`` and its
        last element ``last_term_id``. Both fields are set to ``False``
        while the year still has no term.
        """
        for record in self:
            first_term = last_term = False
            if record.term_ids:
                first_term = record.term_ids[0]
                last_term = record.term_ids[-1]
            record.first_term_id = first_term
            record.last_term_id = last_term

    @api.constrains("date_start", "date_end")
    def _check_date_coherence(self):
        """Enforce that the academic year ends after it starts.

        Runs on every create or write touching ``date_start`` or
        ``date_end``. Records where either date is still empty pass
        untouched; a year whose ``date_end`` is earlier than or equal to
        its ``date_start`` is rejected.

        :raises ValidationError: ``date_end`` is not strictly later than
            ``date_start``.
        """
        for record in self:
            if (
                record.date_start
                and record.date_end
                and record.date_end <= record.date_start
            ):
                error_message = (
                    _(
                        """
Context: Set academic year dates
Database ID: %s
Problem: Date End must be after Date Start
Solution: Set Date End to a date later than Date Start
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)
