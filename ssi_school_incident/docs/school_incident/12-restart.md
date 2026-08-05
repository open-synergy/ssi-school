# Restart School Incident

> **Module:** ssi*school_incident\
> **Model:** `school_incident`\
> **Menu:** School > Incident > Incidents\
> **Actor:** user in group \_Officer (Counselor/Vice Principal)* or higher\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Access:** User has _Can Restart_ access right (belongs to the Officer
  (Counselor/Vice Principal) group or higher).

## Flow

1. Open the **School > Incident > Incidents** menu.
2. Open the School Incident record to restart.
3. Click the **Restart** button.

## Post-Condition

- Status returns to **Draft**.
