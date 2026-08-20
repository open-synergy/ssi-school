# Restart School Academic Alert

> **Module:** ssi*school_incident\
> **Model:** `school_academic_alert`\
> **Menu:** School > Incident > Academic Alerts\
> **Actor:** user in group \_Academic Alert Validator* or higher\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Access:** User has _Can Restart_ access right (belongs to the Academic Alert
  Validator group or higher).

## Flow

1. Open the **School > Incident > Academic Alerts** menu.
2. Open the School Academic Alert record to restart.
3. Click the **Restart** button.

## Post-Condition

- Status returns to **Draft**.
