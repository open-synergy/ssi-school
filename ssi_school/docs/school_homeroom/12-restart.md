# Restart Homeroom

> **Module:** ssi*school\
> **Model:** `school_homeroom`\
> **Menu:** School > Student Activities > Homerooms\
> **Actor:** user in group \_Homeroom — Validator*\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Config:** An active `policy.template` grants `restart_ok` for that state to the
  actor's group.
- **Access:** User is in group _Homeroom — Validator_.

## Flow

1. Open the **School > Student Activities > Homerooms** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- All approval records are removed and the approval template is cleared. A later Confirm
  starts the approval process from the beginning.
