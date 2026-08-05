# Approve School Incident

> **Module:** ssi*school_incident\
> **Model:** `school_incident`\
> **Menu:** School > Incident > Incidents\
> **Actor:** approver in group \_Officer (Counselor/Vice Principal)* or higher\
> **State:** `confirm` → `open`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Access:** User is registered as an approver on the active approval template (belongs
  to the Officer (Counselor/Vice Principal) group or higher).
- **Access:** User has _Can Approve_ access right.

## Flow

### Single Record

1. Open the **School > Incident > Incidents** menu.
2. Open the School Incident record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

### Bulk (Multiple Records)

1. Open the **School > Incident > Incidents** menu.
2. In the list view, open the **Filters** panel and select **Waiting for Approval** so
   only records awaiting approval are shown.
3. Select the checkbox of each record to approve — select only records where the active
   user is a valid approver, since a single ineligible record in the selection aborts
   the whole action and none of the selected records are approved.
4. Click the **Approve** button that appears above the list.
5. Click **OK** on the confirmation dialog.

## Post-Condition

- The approval template for this case has a single approval level (Officer group), so
  approving it fulfills the whole approval workflow immediately.
- Status automatically moves to **Open** right after this approval (the system moves the
  document from Waiting for Approval directly to Open; there is no separate manual
  "Start" step).
- A Document Number is generated once the record reaches **Open** status.
- When approved in bulk, each selected record's approval is evaluated independently:
  every selected record moves to **Open** by the same rule as the single-record flow
  above.
