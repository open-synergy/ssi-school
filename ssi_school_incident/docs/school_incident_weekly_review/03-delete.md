# Delete School Incident Weekly Review

> **Module:** ssi*school_incident\
> **Model:** `school_incident_weekly_review`\
> **Menu:** School > Incident > Weekly Case Reviews\
> **Actor:** user in group \_Weekly Review User* or higher\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** Document number is still **/** (not yet generated).

## Flow

1. Open the **School > Incident > Weekly Case Reviews** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
- The School Incident records that were collected into the deleted review are not
  affected: this review only referenced them, it never created, edited, or cancelled
  them.
