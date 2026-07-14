# Approve School Incident Weekly Review

## Pre-Condition

- Record is in **Waiting for Approval** status.
- User is registered as an approver on the active approval template (belongs to the
  Manager (Principal) group).
- User has _Can Approve_ access right.

## Flow

### Single Record

1. Open the **School > Incident > Weekly Case Reviews** menu.
2. Open the Weekly Case Review record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

### Bulk (Multiple Records)

1. Open the **School > Incident > Weekly Case Reviews** menu.
2. In the list view, open the **Filters** panel and select **Waiting for Approval** so
   only records awaiting approval are shown.
3. Select the checkbox of each record to approve — select only records where the active
   user is a valid approver, since a single ineligible record in the selection aborts
   the whole action and none of the selected records are approved.
4. Click the **Approve** button that appears above the list.
5. Click **OK** on the confirmation dialog.

## Post-Condition

- The approval template for this review has a single approval level (Manager group), so
  approving it fulfills the whole approval workflow immediately.
- Status automatically moves to **Done** right after this approval (this model has no
  separate Open state and no manual "Done"/"Finish" button: the system moves the
  document from Waiting for Approval directly to Done).
- A Document Number is generated once the record reaches **Done** status.
- When approved in bulk, each selected record's approval is evaluated independently:
  every selected record moves to **Done** by the same rule as the single-record flow
  above.
