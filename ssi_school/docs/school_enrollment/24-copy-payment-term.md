# Copy Payment Terms — Enrollment

> **Module:** `ssi_school`\
> **Model:** `school_enrollment`\
> **Menu:** School > Student Activities > Enrollments\
> **Actor:** user in group _Enrollment — User_ (`school_enrollment_user_group`)\
> **Requires:** `01-create`

This action has no button on the form. It is a contextual action, reached from the
**Action** menu of the Enrollments **list** view, and it acts on every enrollment ticked
there — so it is not a step in this model's own lifecycle and no `State:` is declared
above.

## Pre-Condition

- **Record:** Every target enrollment is in status **Draft**. A target in any other
  status is rejected by name when the wizard is confirmed, and nothing is copied.
- **Record:** Every target enrollment has the same **Academic Term**, **School**, and
  **Grade** as the source enrollment. Mismatched targets are rejected by name, and
  nothing is copied.
- **Data:** A source enrollment exists and already carries the Payment Terms to copy.
  The source is chosen inside the wizard and may be in any status — only the targets are
  restricted.
- **Config:** An active `policy.template` for this model grants `copy_payment_term_ok`
  for state `draft` to the actor's group.
- **Access:** User is in group _Enrollment — User_ (`school_enrollment_user_group`).

## Flow

1. Open the **School > Student Activities > Enrollments** menu.
2. In the list view, tick the checkbox of every enrollment that will **receive** the
   payment terms.
3. Click **Action** > **Copy Payment Terms**.
4. In the wizard, the ticked records are shown read-only in **Target Enrollments**. To
   change the selection, close the wizard and tick a different set.
5. Fill in the fields:
   - **Source Enrollment** _(required)_: the enrollment whose Payment Terms (and their
     detail lines) are copied. The ticked targets are excluded from the choices.
   - **Mode** _(required)_: **Replace** (default) deletes the existing Payment Terms on
     each target before copying; **Add** appends the source terms to the terms each
     target already has.
6. Click **Copy Payment Terms** (`action_copy_payment_term`) in the wizard footer.

## Post-Condition

- Every target enrollment carries a copy of the source enrollment's Payment Terms,
  including their detail lines. With **Replace**, the terms each target had before are
  gone; with **Add**, they are kept alongside the copied ones.
- The copies are **uninvoiced**: the link to the source's customer invoice and invoice
  lines is cleared on each copied term and detail, so they can still be invoiced through
  the target's own **Create Due Invoice** (see `19-create-due-invoice.md`).
- No status changes on either the source or the targets.
- If any target fails a check, **no** target is changed — every target is validated
  before the first copy is made — and the wizard reports the offending enrollments by
  name.
