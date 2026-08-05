# Approve Student Graduation

> **Module:** ssi_school_student_graduation\
> **Model:** `school_student_graduation`\
> **Menu:** School > Student Activities > Student Graduations\
> **Actor:** approver on the pending approval level\
> **State:** `confirm` → `done`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Record:** The student is still in the **Enrolled** state.
- **Config:** An active `policy.template` grants `approve_ok` to the actor's group.
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. When the template uses sequential approval, only the first unapproved
  level is pending.

## Flow

1. Open the **School > Student Activities > Student Graduations** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, status changes automatically to **Done**, the
  student is moved to the **Graduate** state, and — if the student has an active
  enrollment — that enrollment's academic year result is set to **Graduate**. Once Done,
  the graduation is terminal and can no longer be cancelled or reverted.
- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.

> **Note:** `school_student_graduation` does **not** have a manual Finish button
> (`_automatically_insert_done_button` is disabled). The transition to **Done** always
> happens automatically as soon as the last approval level is fulfilled — there is no
> `07-start.md` or `09-finish.md` for this model.
