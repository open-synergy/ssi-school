# Confirm Student Graduation

> **Module:** ssi*school_student_graduation\
> **Model:** `school_student_graduation`\
> **Menu:** School > Student Activities > Student Graduations\
> **Actor:** user in group \_School Student Graduation — User*\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** The student is still in the **Enrolled** state.
- **Record:** No other Draft or Waiting for Approval graduation already exists for the
  same student.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** User is in group _School Student Graduation — User_.

## Flow

1. Open the **School > Student Activities > Student Graduations** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for each approver level defined by the approval template.
