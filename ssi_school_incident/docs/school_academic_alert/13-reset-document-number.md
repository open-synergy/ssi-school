# Reset Document Number — School Academic Alert

> **Module:** ssi*school_incident\
> **Model:** `school_academic_alert`\
> **Menu:** School > Incident > Academic Alerts\
> **Actor:** user in group \_Academic Alert Validator* or higher\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User has _Can Input Manual Document Number_ access right (belongs to the
  Academic Alert Validator group or higher).

## Flow

1. Open the **School > Incident > Academic Alerts** menu.
2. Open the School Academic Alert record whose document number will be reset.
3. Click the **Reset Document Number** button (or edit the number field and change it to
   **/**).

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number when it transitions to **Open** status,
  according to the sequence template configuration.
