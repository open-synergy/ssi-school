# Set Result to Drop Out — Enrollment

> **Module:** ssi*school\
> **Model:** `school_enrollment`\
> **Menu:** School > Student Activities > Enrollments\
> **Actor:** user in group \_Enrollment — User*\
> **State:** `open` → `done`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Record:** The Academic Term of this enrollment is the last term of its Academic Year
  (this button is only available on the last term; use `09-finish` on earlier terms).
- **Config:** An active `policy.template` for this model grants `drop_out_ok` for state
  `open` to the actor's group.
- **Access:** User is in group _Enrollment — User_.

## Flow

1. Open the **School > Student Activities > Enrollments** menu.
2. Open the record to set as Drop Out.
3. Click the **Drop Out** button (`action_set_result_to_drop_out`).
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
- **Academic Year Result** is set to **Drop Out**. **Promote To Grade** is left empty.
- The student's status is set to **Dropped Out / Expelled**.
