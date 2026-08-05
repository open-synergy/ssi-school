# Delete Admission

> **Module:** ssi*school_admission\
> **Model:** `school_admission`\
> **Menu:** School > Admission > Admissions\
> **Actor:** user in group \_Admission — User*\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** Document number is still **/** (not yet generated).
- **Access:** User is in group _Admission — User_.

## Flow

1. Open the **School > Admission > Admissions** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
