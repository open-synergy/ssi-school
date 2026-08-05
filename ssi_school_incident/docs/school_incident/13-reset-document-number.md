# Reset Document Number — School Incident

> **Module:** ssi*school_incident\
> **Model:** `school_incident`\
> **Menu:** School > Incident > Incidents\
> **Actor:** user in group \_Officer (Counselor/Vice Principal)* or higher\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User has _Can Input Manual Document Number_ access right (belongs to the
  Officer (Counselor/Vice Principal) group or higher).

## Flow

1. Open the **School > Incident > Incidents** menu.
2. Open the School Incident record whose document number will be reset.
3. Click the **Reset Document Number** button (or edit the number field and change it to
   **/**).

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number when it transitions to **Open** status,
  according to the sequence template configuration.
