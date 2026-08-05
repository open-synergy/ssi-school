# Finish Homeroom

> **Module:** ssi*school\
> **Model:** `school_homeroom`\
> **Menu:** School > Student Activities > Homerooms\
> **Actor:** user in group \_Homeroom — User*\
> **State:** `open` → `done`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Config:** An active `policy.template` grants `done_ok` for state `open` to the
  actor's group.
- **Access:** User is in group _Homeroom — User_.

## Flow

1. Open the **School > Student Activities > Homerooms** menu.
2. Open the record to finish.
3. Click the **Done** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
