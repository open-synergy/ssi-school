# Finish Admission Form

> **Module:** ssi_school_admission\
> **Model:** `school_admission_form`\
> **Menu:** School > Admission > Forms\
> **Actor:** — (automatic, no button)\
> **State:** `open` → `done`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress**, and the form is **not free** (it has at least
  one fee line so its total is greater than zero). A free form (zero total) instead
  moves to **Done** immediately when it opens — see the note in `05-approve`.
- **Record:** The receivable journal item generated for this form's fee (`Journal Item`
  on the **Accounting** tab) is not yet reconciled.

## Flow

This transition has **no button** — `_automatically_insert_done_button` is disabled for
this model, so `done_ok` is always denied by policy. Instead, it is triggered
**automatically** by a `base.automation` rule (`school_admission_form_open_2_done`) as
soon as the linked **Journal Item** becomes fully reconciled — for example when a user
reconciles the parent's payment against the receivable entry from the **Accounting >
Payments** menu, or from manual reconciliation. No action is taken on this
`school_admission_form` record itself; the system reacts to the **Journal Item**'s
`reconciled` flag changing on write.

There is no manual alternative: as long as the amount is unpaid (or the form is free,
see `01-create`), the record stays **On Progress** indefinitely.

## Post-Condition

- Status changes to **Done**.
- If the same **Journal Item** is later unreconciled (e.g. the matching payment is
  undone), the base.automation rule `school_admission_form_done_2_open` automatically
  moves the record back to **On Progress**.
