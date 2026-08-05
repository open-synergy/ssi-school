# Deactivate Incident Escalation Criteria

> **Module:** ssi*school_incident\
> **Model:** `school_incident_escalation_criteria`\
> **Menu:** School > Configuration > Configuration > Escalation Criteria\
> **Actor:** user in group \_Manager (Principal)*\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- None.

## Flow

1. Open the **School > Configuration > Configuration > Escalation Criteria** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated Escalation Criteria cannot be selected in the Escalate wizard on new
  escalations.
- School Incident records that already reference an archived criterion in their
  escalation history can still be viewed.
