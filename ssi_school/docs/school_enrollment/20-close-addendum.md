# Close Addendum — Enrollment

> **Module:** ssi*school\
> **Model:** `school_enrollment`\
> **Menu:** School > Student Activities > Enrollments\
> **Actor:** user in group \_Enrollment — Validator*\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Record:** At least one Payment Term or Payment Term Detail line is currently
  unlocked (for example, one added after the enrollment opened).
- **Config:** An active `policy.template` for this model grants `addendum_ok` for state
  `open` to the actor's group.
- **Access:** User is in group _Enrollment — Validator_.

## Flow

1. Open the **School > Student Activities > Enrollments** menu.
2. Open the record whose addendum Payment Terms will be locked.
3. On the **Billing** tab, click the **Close Addendum** button
   (`action_close_addendum`).
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status remains **On Progress**.
- Every currently unlocked Payment Term and Payment Term Detail line becomes locked and
  can no longer be changed, until the enrollment is restarted (`12-restart`).
