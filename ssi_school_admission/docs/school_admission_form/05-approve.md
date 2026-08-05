# Approve Admission Form

> **Module:** ssi_school_admission\
> **Model:** `school_admission_form`\
> **Menu:** School > Admission > Forms\
> **Actor:** approver on the pending approval level\
> **State:** `confirm` → `open`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `approve_ok` to the actor's group.
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. When the template uses sequential approval, only the first unapproved
  level is pending.

## Flow

1. Open the **School > Admission > Forms** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, status changes automatically to **On Progress**
  (there is no separate Start step — see note below).
- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.

> **Note:** `school_admission_form` inherits `mixin.transaction_open`, but\
> `_automatically_insert_open_button` is disabled and no manual Start button is rendered.\
> The transition to **On Progress** always happens automatically as soon as the last\
> approval level is fulfilled — there is no `07-start.md` for this model.

> **Note:** If the form has no fee lines (a **free** admission, i.e. its total is
> zero),\
> it also transitions immediately and automatically from **On Progress** to **Done** as\
> soon as it opens — there is no manual Finish step in this case. See `09-finish` for
> the\
> normal (paid) case.
