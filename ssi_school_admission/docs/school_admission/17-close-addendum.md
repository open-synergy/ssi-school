# Close Addendum — Admission

> **Module:** ssi*school_admission\
> **Model:** `school_admission`\
> **Menu:** School > Admission > Admissions\
> **Actor:** user in group \_Admission — Validator*\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress**, and at least one **Payment Terms** line or
  detail is currently unlocked (for example after `12-restart`, or after new terms were
  added during the addendum window).
- **Config:** An active `policy.template` for this model grants `addendum_ok` for state
  `open` to the actor's group.
- **Access:** User is in group _Admission — Validator_. The button is only visible to
  this group.

## Flow

1. Open the **School > Admission > Admissions** menu.
2. Open the record whose payment terms should be locked.
3. On the **Fee** tab, click the **Close Addendum** button (`action_close_addendum`).
4. Click **OK** on the confirmation dialog.

## Post-Condition

- All currently unlocked **Payment Terms** lines and details are locked (their **Name**,
  **Date Invoice**, and **Date Due** become read-only).
- Status remains **On Progress**.

> **Note:** While `addendum_ok` grants access, the **Payment Terms** table on this\
> record's **Fee** tab remains editable even though status is **On Progress** — new\
> payment terms may be added and the row buttons from `01-create` used, until this
> action\
> locks them.
