# Cancel Student Class Mutation

> **Module:** ssi*school\
> **Model:** `school_student_mutation`\
> **Menu:** School > Student Activities > Student Class Mutations\
> **Actor:** user in group \_Student Class Mutation — Validator*\
> **State:** `draft` | `confirm` | `reject` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, or **Rejected**. Once the
  mutation reaches **Done**, it is terminal and can no longer be cancelled.
- **Config:** An active `policy.template` grants `cancel_ok` for that state to the
  actor's group.
- **Access:** User is in group _Student Class Mutation — Validator_.

## Flow

1. Open the **School > Student Activities > Student Class Mutations** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
