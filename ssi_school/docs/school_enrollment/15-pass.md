# Set Result to Passed — Enrollment

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
- **Config:** An active `policy.template` for this model grants `pass_ok` for state
  `open` to the actor's group.
- **Access:** User is in group _Enrollment — User_.

## Flow

1. Open the **School > Student Activities > Enrollments** menu.
2. Open the record to set as Passed.
3. Click the **Pass** button (`action_set_result_to_passed`).
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
- **Academic Year Result** is set to **Passed**, and **Promote To Grade** is filled with
  the Grade's configured next grade.
- The student's status returns to **Waiting for Enrollment**, ready for a new enrollment
  on the promoted grade.
- If **Revenue Recognition** is enabled, one Revenue Recognition journal entry is posted
  (see **Recognition Move** on the Accounting page), moving the amount of every invoiced
  payment term detail that carries a **Final Account** from its own account to that
  Final Account. Terms not yet invoiced, and details without a Final Account, are
  skipped.
