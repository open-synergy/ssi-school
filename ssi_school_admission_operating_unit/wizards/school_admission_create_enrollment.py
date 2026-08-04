# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class SchoolAdmissionWizardCreateEnrollment(models.TransientModel):
    """Propagate the admission's operating unit to its new enrollment.

    Extends the Create Enrollment wizard so the ``school_enrollment``
    it creates carries the same ``operating_unit_id`` as the source
    ``school_admission``, keeping the admission -> enrollment ->
    customer invoice chain on a single operating unit.
    """

    _name = "school_admission.wizard_create_enrollment"
    _inherit = "school_admission.wizard_create_enrollment"

    def _create_enrollment(self):
        """Create the enrollment, then copy the admission's OU.

        The idempotency guard (``admission_id.enrollment_id``) is read
        **before** calling ``super()``, so a repeated call on an
        admission that already has an enrollment never rewrites that
        enrollment's operating unit — only an enrollment created by
        *this* call is stamped. Admissions without an operating unit
        leave the enrollment's own value untouched.

        :return: the created (or pre-existing) ``school_enrollment``
            record, exactly as returned by ``super()``
        """
        self.ensure_one()
        is_new_enrollment = not self.admission_id.enrollment_id
        enrollment = super()._create_enrollment()
        if is_new_enrollment and self.admission_id.operating_unit_id:
            operating_unit = self.admission_id.operating_unit_id
            enrollment.write({"operating_unit_id": operating_unit.id})
        return enrollment
