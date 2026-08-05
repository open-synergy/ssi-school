# Delete Student

> **Module:** ssi_school\
> **Model:** `school_student`\
> **Menu:** School > Students\
> **Actor:** user in group `Student`\
> **Requires:** `01-create`

## Pre-Condition

- **Access:** User is in group `Student`.

## Flow

1. Open the **School > Students** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system. The linked `res.partner`
  contact record itself is not deleted.
