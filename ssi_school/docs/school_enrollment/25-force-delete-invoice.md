# Force Delete Invoice — Enrollment

> **Module:** `ssi_school`\
> **Model:** `school_enrollment`\
> **Menu:** School > Student Activities > Enrollments\
> **Actor:** user in group _Enrollment — Validator_ (`school_enrollment_validator_group`)\
> **Requires:** `05-approve`

The **Force Delete Invoice** button sits on a Payment Term line of the **Billing** tab.
It is a term-level action, not a transition of the enrollment itself, so no `State:` is
declared above. It removes the customer invoice of a Payment Term whatever the state of
that invoice, which the **Delete Invoice** button cannot do once the invoice left Draft.

## Pre-Condition

- **Record:** The enrollment is **On Progress** or **Done**.
- **Record:** The Payment Term is **Invoiced** or **Paid** and is linked to a customer
  invoice. A locked term (the enrollment is already open) qualifies.
- **Record:** The customer invoice is not blocked by another document. An invoice whose
  line was already recognized by the enrollment's Revenue Recognition is rejected, and
  so is an invoice that a connected module relies on (for example a fee waiver,
  scholarship, deposit or promotion allocation).
- **Config:** An active `policy.template` for this model grants `force_delete_term_ok`
  for states `open` and `done` to the actor's group.
- **Access:** User is in group _Enrollment — Validator_.

## Flow

1. Open the **School > Student Activities > Enrollments** menu.
2. Open the record whose Payment Term invoice will be deleted.
3. On the **Billing** tab, click the **Force Delete Invoice** button
   (`action_force_delete_invoice`) on the Payment Term line.
4. Click **OK** on the confirmation dialog. It warns that the reconciliation is undone
   and the invoice is deleted.

## Post-Condition

- The customer invoice is deleted. If it was not a draft, its reconciliation with any
  payment is undone first, then the invoice is cancelled, restarted and its document
  number is reset to `/`. The payments themselves stay as unallocated payments.
- The Payment Term is **Uninvoiced** again and its detail lines no longer point to an
  invoice line.
- The enrollment keeps its status.
- The enrollment chatter records a note with the invoice number, its total, its state
  before deletion and the user who deleted it.
- If the invoice is blocked, nothing changes and an error explains which document blocks
  the deletion.
