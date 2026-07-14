# Confirm School Incident Weekly Review

## Pre-Condition

- Record is in **Draft** status.
- User has _Can Confirm_ access right (belongs to the Officer (Counselor/Vice Principal)
  group or higher).

## Flow

### Single Record

1. Open the **School > Incident > Weekly Case Reviews** menu.
2. Open the Weekly Case Review record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

### Bulk (Multiple Records)

1. Open the **School > Incident > Weekly Case Reviews** menu.
2. In the list view, open the **Filters** panel and select **Draft** so only Draft
   records are shown.
3. Select the checkbox of each record to confirm (or use the header checkbox to select
   all filtered records).
4. Click the **Confirm** button that appears above the list.
5. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- When confirmed in bulk, every selected record moves to **Waiting for Approval** in the
  same action. If any selected record is not in **Draft** status, the whole action is
  cancelled and none of the selected records are confirmed — always filter by **Draft**
  first as described above.
