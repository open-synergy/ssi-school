# Confirm Student Class Mutation

> **Module:** ssi*school\
> **Model:** `school_student_mutation`\
> **Menu:** School > Student Activities > Student Class Mutations\
> **Actor:** user in group \_Student Class Mutation — User*\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** The Enrollment is still **On Progress**.
- **Record:** No other Draft or Waiting for Approval mutation already exists for the
  same Enrollment.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** User is in group _Student Class Mutation — User_.

## Flow

1. Open the **School > Student Activities > Student Class Mutations** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for each approver level defined by the approval template.
