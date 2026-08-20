# Activate Incident Type

> **Module:** ssi*school_incident\
> **Model:** `school_incident_type`\
> **Menu:** School > Configuration > Incident > Incident Types\
> **Actor:** user in group \_Manager (Principal)*\
> **Active:** `false` → `true`\
> **Requires:** `01-create`

## Pre-Condition

- None.

## Flow

1. Open the **School > Configuration > Incident > Incident Types** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The Incident Types can be selected again on new School Incident records.
