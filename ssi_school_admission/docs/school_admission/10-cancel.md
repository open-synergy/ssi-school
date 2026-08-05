# Cancel Admission

> **Module:** ssi*school_admission\
> **Model:** `school_admission`\
> **Menu:** School > Admission > Admissions\
> **Actor:** user in group \_Admission — Validator*\
> **State:** `draft` | `open` | `done` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **On Progress**, or **Done**.
- **Record:** None of the **Payment Terms** lines are linked to a customer invoice. If
  any term already has an invoice, cancellation is rejected — delete or disconnect the
  invoice first (row button **Delete Invoice** / **Disconnect Invoice**, see
  `01-create`).
- **Config:** An active `policy.template` grants `cancel_ok` for that state to the
  actor's group.
- **Access:** User is in group _Admission — Validator_.

## Flow

1. Open the **School > Admission > Admissions** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
