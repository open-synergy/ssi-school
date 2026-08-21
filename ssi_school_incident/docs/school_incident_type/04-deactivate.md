# Deactivate Incident Type

> **Module:** ssi*school_incident\
> **Model:** `school_incident_type`\
> **Menu:** School > Configuration > Incident > Incident Types\
> **Actor:** user in group \_Manager (Principal)*\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- None.

## Flow

1. Open the **School > Configuration > Incident > Incident Types** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated Incident Types cannot be selected on new School Incident records.
- School Incident records already using a deactivated Incident Type can still be viewed.
