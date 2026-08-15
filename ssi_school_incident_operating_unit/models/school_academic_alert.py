# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolAcademicAlert(models.Model):
    """
    Extends School Academic Alert with single operating unit support,
    restricting each academic warning check to one operating unit and
    propagating that operating unit to the school_incident document
    generated from an Orange/Red alert level.
    """

    _name = "school_academic_alert"
    _inherit = [
        "school_academic_alert",
        "mixin.single_operating_unit",
    ]

    def _prepare_incident_data(self, incident_type):
        """Add this alert's operating unit to the incident values.

        Without this override, the school_incident created by
        ``action_create_incident`` falls back to the default of
        ``mixin.single_operating_unit``, which is the operating unit of
        the user pressing the button rather than the operating unit of
        the academic alert itself. That silently hides the generated
        incident from the alert's own operating unit.

        :param incident_type: school_incident_type record used for the
            generated incident
        :return: incident creation values, with ``operating_unit_id``
            taken from this academic alert
        """
        res = super()._prepare_incident_data(incident_type)
        res["operating_unit_id"] = self.operating_unit_id.id
        return res
