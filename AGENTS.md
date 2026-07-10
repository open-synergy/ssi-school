# AGENTS.md

This file indexes **Instruksi Kerja (IK)** documentation across this repository's
modules, for AI/agent consumption. Each module's IK files live under
`<module>/docs/<model_name>/`, one Markdown file per operational action (Create, Edit,
Delete, Confirm, Approve, ...), each structured as Pre-Condition / Flow /
Post-Condition. See each module's `README.rst` ("Work Instruction" section) for the
human-facing rendered links.

## ssi_school_incident

- `school_incident_type` ->
  [ssi_school_incident/docs/school_incident_type/](ssi_school_incident/docs/school_incident_type/)
- `school_incident_escalation_criteria` ->
  [ssi_school_incident/docs/school_incident_escalation_criteria/](ssi_school_incident/docs/school_incident_escalation_criteria/)
- `school_academic_alert_level` ->
  [ssi_school_incident/docs/school_academic_alert_level/](ssi_school_incident/docs/school_academic_alert_level/)
- `school_incident` ->
  [ssi_school_incident/docs/school_incident/](ssi_school_incident/docs/school_incident/)
- `school_academic_alert` ->
  [ssi_school_incident/docs/school_academic_alert/](ssi_school_incident/docs/school_academic_alert/)
- `school_incident_weekly_review` ->
  [ssi_school_incident/docs/school_incident_weekly_review/](ssi_school_incident/docs/school_incident_weekly_review/)

Note: `school_incident_parent_contact` has no IK — it is a child/detail model (O2M lines
on `school_incident`), not a standalone model.
