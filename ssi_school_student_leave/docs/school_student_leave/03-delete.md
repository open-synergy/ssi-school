# Delete Student Leave

> **Module:** ssi*school_student_leave\
> **Model:** `school_student_leave`\
> **Menu:** School > Student Activities > Student Leaves\
> **Actor:** user in group \_School Student Leave — User*\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** Document number is still **/** (not yet generated).
- **Access:** User is in group _School Student Leave — User_.

## Flow

1. Open the **School > Student Activities > Student Leaves** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
