# Create Incident from School Academic Alert

> **Module:** ssi_school_incident_operating_unit\
> **Extends:** ssi_school_incident — model `school_academic_alert`, action `15-create-incident`

## Additional Post-Condition

- The School Incident created by the **Create Incident** button now takes its
  **Operating Unit** from this Academic Alert, not from the operating unit of the user
  who pressed the button. An alert of Operating Unit A therefore always produces an
  incident of Operating Unit A, even when the acting Officer belongs to another
  operating unit.
- Because the incident carries the alert's operating unit, it stays visible to the users
  assigned to that operating unit under the incident record rule.
