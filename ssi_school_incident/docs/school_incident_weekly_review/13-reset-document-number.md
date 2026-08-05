# Reset Document Number — School Incident Weekly Review

> **Module:** ssi*school_incident\
> **Model:** `school_incident_weekly_review`\
> **Menu:** School > Incident > Weekly Case Reviews\
> **Actor:** user in group \_Officer (Counselor/Vice Principal)* or higher\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User has _Can Input Manual Document Number_ access right (belongs to the
  Officer (Counselor/Vice Principal) group or higher).

## Flow

1. Open the **School > Incident > Weekly Case Reviews** menu.
2. Open the Weekly Case Review record whose document number will be reset.
3. Click the **Reset Document Number** button (or edit the number field and change it to
   **/**).

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number when it transitions to **Done** status,
  according to the sequence template configuration.
