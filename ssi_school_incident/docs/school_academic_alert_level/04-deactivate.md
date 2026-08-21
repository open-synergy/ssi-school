# Deactivate Academic Alert Level

> **Module:** ssi*school_incident\
> **Model:** `school_academic_alert_level`\
> **Menu:** School > Configuration > Incident > Academic Alert Levels\
> **Actor:** user in group \_Manager (Principal)*\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- None.

## Flow

1. Open the **School > Configuration > Incident > Academic Alert Levels** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated Academic Alert Levels are excluded from the next Evaluate run of a School
  Academic Alert.
- School Academic Alert records that already reference an archived level can still be
  viewed.
