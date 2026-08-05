# Approve Student Class Mutation

> **Module:** ssi_school\
> **Model:** `school_student_mutation`\
> **Menu:** School > Student Activities > Student Class Mutations\
> **Actor:** approver on the pending approval level\
> **State:** `confirm` → `done`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Record:** The Enrollment is still **On Progress**.
- **Record:** The Destination Grade Class is not already at full capacity.
- **Config:** An active `policy.template` grants `approve_ok` to the actor's group.
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. When the template uses sequential approval, only the first unapproved
  level is pending.

## Flow

1. Open the **School > Student Activities > Student Class Mutations** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, status changes automatically to **Done** and the
  linked Enrollment's Grade Class and Homeroom are updated to the Destination Grade
  Class and Destination Homeroom. Once Done, the mutation is terminal and can no longer
  be cancelled or reverted — to undo it, create a new mutation in the opposite
  direction.
- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.

> **Note:** `school_student_mutation` does **not** inherit `mixin.transaction_open` and
> has no manual Finish button (`_automatically_insert_done_button` is disabled). The
> transition to **Done** always happens automatically as soon as the last approval level
> is fulfilled — there is no `07-start.md` or `09-finish.md` for this model.
