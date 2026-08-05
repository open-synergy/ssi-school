# Delete Grade

> **Module:** ssi_school\
> **Model:** `school_grade`\
> **Menu:** School > Configuration > Grade > Grades\
> **Actor:** user in group `Grade`\
> **Requires:** `01-create`

## Pre-Condition

- **Access:** User is in group `Grade`.

## Flow

1. Open the **School > Configuration > Grade > Grades** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
- **Previous Grade** and **Next Grade** of the remaining Grades in the same Type are
  automatically recomputed to reflect the new ordering.
