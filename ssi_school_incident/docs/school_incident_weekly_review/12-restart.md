# Restart School Incident Weekly Review

> **Module:** ssi*school_incident\
> **Model:** `school_incident_weekly_review`\
> **Menu:** School > Incident > Weekly Case Reviews\
> **Actor:** user in group \_Weekly Review User* or higher\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Access:** User has _Can Restart_ access right (belongs to the Weekly Review User
  group or higher).

## Flow

1. Open the **School > Incident > Weekly Case Reviews** menu.
2. Open the Weekly Case Review record to restart.
3. Click the **Restart** button.

## Post-Condition

- Status returns to **Draft**.
