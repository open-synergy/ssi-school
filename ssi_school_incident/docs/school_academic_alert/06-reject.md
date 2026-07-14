# Reject School Academic Alert

## Pre-Condition

- Record is in **Waiting for Approval** status.
- User is registered as an approver on the active approval template (belongs to the
  Officer (Counselor/Vice Principal) group or higher).
- User has _Can Reject_ access right.

## Flow

### Single Record

1. Open the **School > Incident > Academic Alerts** menu.
2. Open the School Academic Alert record to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

### Bulk (Multiple Records)

1. Open the **School > Incident > Academic Alerts** menu.
2. In the list view, open the **Filters** panel and select **Waiting for Approval** so
   only records awaiting approval are shown.
3. Select the checkbox of each record to reject — select only records where the active
   user is a valid approver, since a single ineligible record in the selection aborts
   the whole action and none of the selected records are rejected.
4. Click the **Reject** button that appears above the list.
5. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**.
- When rejected in bulk, every selected record moves to **Rejected** in the same action.
