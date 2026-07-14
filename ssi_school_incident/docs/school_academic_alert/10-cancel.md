# Cancel School Academic Alert

## Pre-Condition

- Record is in **Draft**, **Waiting for Approval**, or **Open** status.
- User has _Can Cancel_ access right (belongs to the Officer (Counselor/Vice Principal)
  group or higher).

## Flow

### Single Record

1. Open the **School > Incident > Academic Alerts** menu.
2. Open the School Academic Alert record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.

### Bulk (Multiple Records)

1. Open the **School > Incident > Academic Alerts** menu.
2. In the list view, open the **Filters** panel and select **Draft**, **Waiting for
   Approval**, and **In Progress** together (multiple filters combine as OR) so only
   cancellable records are shown — records already **Done** or **Cancelled** must not be
   included.
3. Select the checkbox of each record to cancel (or use the header checkbox to select
   all filtered records).
4. Click the **Cancel** button that appears above the list.
5. In the wizard that appears, select the **Cancellation Reason** — this single reason
   is applied to every selected record.
6. Click **Confirm**.

## Post-Condition

- Status changes to **Cancelled**.
- When cancelled in bulk, every selected record moves to **Cancelled** in the same
  action, with the same Cancellation Reason recorded on each.
