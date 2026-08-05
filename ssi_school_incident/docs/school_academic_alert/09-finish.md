# Finish School Academic Alert

> **Module:** ssi*school_incident\
> **Model:** `school_academic_alert`\
> **Menu:** School > Incident > Academic Alerts\
> **Actor:** user in group \_User (Homeroom Teacher)* or higher\
> **State:** `open` → `done`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **Open**.
- **Access:** User has _Can Finish_ access right (belongs to the User (Homeroom Teacher)
  group or higher).

## Flow

### Single Record

1. Open the **School > Incident > Academic Alerts** menu.
2. Open the School Academic Alert record to finish.
3. Click the **Done** button.

### Bulk (Multiple Records)

1. Open the **School > Incident > Academic Alerts** menu.
2. In the list view, open the **Filters** panel and select **In Progress** so only
   records currently Open are shown.
3. Select the checkbox of each record to finish (or use the header checkbox to select
   all filtered records).
4. Click the **Done** button that appears above the list.
5. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
- When finished in bulk, every selected record moves to **Done** in the same action. If
  any selected record is not in **Open** status, the whole action is cancelled and none
  of the selected records are finished — always filter by **In Progress** first as
  described above.
