# Finish Enrollment

> **Module:** ssi*school\
> **Model:** `school_enrollment`\
> **Menu:** School > Student Activities > Enrollments\
> **Actor:** user in group \_Enrollment — User*\
> **State:** `open` → `done`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Record:** The Academic Term of this enrollment is **not** the last term of its
  Academic Year. When it is the last term, this button is not available — use `15-pass`,
  `16-fail`, `17-drop-out`, or `18-graduate` instead, which record the academic year
  result before finishing the enrollment.
- **Config:** An active `policy.template` grants `done_ok` for state `open` to the
  actor's group.
- **Access:** User is in group _Enrollment — User_.

## Flow

1. Open the **School > Student Activities > Enrollments** menu.
2. Open the record to finish.
3. Click the **Done** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
