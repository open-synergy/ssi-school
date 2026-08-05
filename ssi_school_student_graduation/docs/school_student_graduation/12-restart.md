# Restart Student Graduation

> **Module:** ssi*school_student_graduation\
> **Model:** `school_student_graduation`\
> **Menu:** School > Student Activities > Student Graduations\
> **Actor:** user in group \_School Student Graduation — Validator*\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Config:** An active `policy.template` grants `restart_ok` for that state to the
  actor's group.
- **Access:** User is in group _School Student Graduation — Validator_.

## Flow

1. Open the **School > Student Activities > Student Graduations** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- All approval records are removed and the approval template is cleared. A later Confirm
  starts the approval process from the beginning.
