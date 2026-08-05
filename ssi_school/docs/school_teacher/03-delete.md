# Delete Teacher

> **Module:** ssi_school\
> **Model:** `school_teacher`\
> **Menu:** School > Teachers\
> **Actor:** user in group `Teacher`\
> **Requires:** `01-create`

## Pre-Condition

- **Access:** User is in group `Teacher`.

## Flow

1. Open the **School > Teachers** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system. The linked `hr.employee`
  record itself is not deleted.
