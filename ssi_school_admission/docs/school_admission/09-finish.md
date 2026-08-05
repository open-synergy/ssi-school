# Finish Admission

> **Module:** ssi*school_admission\
> **Model:** `school_admission`\
> **Menu:** School > Admission > Admissions\
> **Actor:** user in group \_Admission — User*\
> **State:** `open` → `done`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Config:** An active `policy.template` grants `done_ok` for state `open` to the
  actor's group.
- **Access:** User is in group _Admission — User_.

## Flow

1. Open the **School > Admission > Admissions** menu.
2. Open the record to finish.
3. Click the **Done** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
