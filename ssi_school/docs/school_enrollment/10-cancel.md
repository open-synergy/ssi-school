# Cancel Enrollment

> **Module:** ssi*school\
> **Model:** `school_enrollment`\
> **Menu:** School > Student Activities > Enrollments\
> **Actor:** user in group \_Enrollment — Validator*\
> **State:** `draft` | `open` | `done` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **On Progress**, or **Done**.
- **Record:** None of the Payment Terms are linked to a customer invoice.
- **Config:** An active `policy.template` grants `cancel_ok` for that state to the
  actor's group.
- **Access:** User is in group _Enrollment — Validator_.

## Flow

1. Open the **School > Student Activities > Enrollments** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- The student's status is set back to **Draft** (no effect if the student was not yet
  enrolled by this record).
