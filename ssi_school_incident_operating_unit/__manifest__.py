# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "School Incident - Operating Unit",
    "version": "14.0.1.0.0",
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
        "ssi_school_incident",
        "ssi_operating_unit_mixin",
    ],
    "data": [
        # Security - shared "Operating Unit" group + Manager tier wiring
        "security/res_groups/school_incident.xml",
        # Security - transactional (school_incident)
        "security/ir_rule/school_incident.xml",
        # Security - transactional (school_incident_weekly_review)
        "security/ir_rule/school_incident_weekly_review.xml",
        # Views
        "views/school_incident.xml",
        "views/school_incident_weekly_review.xml",
    ],
    "demo": [],
}
