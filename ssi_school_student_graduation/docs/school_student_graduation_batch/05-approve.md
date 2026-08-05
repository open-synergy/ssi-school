# Approve Graduation Batch

> **Module:** ssi_school_student_graduation\
> **Model:** `school_student_graduation_batch`\
> **Menu:** School > Student Activities > Graduation Batches\
> **Actor:** approver on the pending approval level\
> **State:** `confirm` → `done`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Record:** At least one student line exists.
- **Record:** Every student line is still in the **Enrolled** state.
- **Config:** An active `policy.template` grants `approve_ok` to the actor's group.
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. When the template uses sequential approval, only the first unapproved
  level is pending.

## Flow

1. Open the **School > Student Activities > Graduation Batches** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, status changes automatically to **Done**. For
  every student line, a **Student Graduation** document is created and driven straight
  through its own Confirm/Done transition, so every guard and side effect defined on the
  individual document (student state check, single-active-graduation check, enrollment
  result update, ...) still applies — the student is moved to the **Graduate** state
  and, if the student has an active enrollment, that enrollment's academic year result
  is set to **Graduate**. Each line keeps a link to the **Student Graduation** document
  generated for it, as an audit trail. Once Done, the batch is terminal and can no
  longer be cancelled or reverted.
- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.

> **Note:** `school_student_graduation_batch` does **not** have a manual Finish button
> (`_automatically_insert_done_button` is disabled). The transition to **Done** always
> happens automatically as soon as the last approval level is fulfilled — there is no
> `07-start.md` or `09-finish.md` for this model.
