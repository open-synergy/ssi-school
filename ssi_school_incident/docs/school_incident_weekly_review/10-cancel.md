# Cancel School Incident Weekly Review

## Pre-Condition

- Record is in **Draft**, **Waiting for Approval**, or **Rejected** status.
- User has _Can Cancel_ access right (belongs to the Manager (Principal) group).

## Flow

### Single Record

1. Open the **School > Incident > Weekly Case Reviews** menu.
2. Open the Weekly Case Review record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.

### Bulk (Multiple Records)

1. Open the **School > Incident > Weekly Case Reviews** menu.
2. In the list view, open the **Filters** panel and select **Draft**, **Waiting for
   Approval**, and **Reject** together (multiple filters combine as OR) so only
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
