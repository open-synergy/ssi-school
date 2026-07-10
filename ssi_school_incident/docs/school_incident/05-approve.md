# Approve School Incident

## Pre-Condition

- Record is in **Waiting for Approval** status.
- User is registered as an approver on the active approval template (belongs to the
  Officer (Counselor/Vice Principal) group or higher).
- User has _Can Approve_ access right.

## Flow

1. Open the **School > Incident > Incidents** menu.
2. Open the School Incident record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- The approval template for this case has a single approval level (Officer group), so
  approving it fulfills the whole approval workflow immediately.
- Status automatically moves to **Open** right after this approval (the system moves the
  document from Waiting for Approval directly to Open; there is no separate manual
  "Start" step).
- A Document Number is generated once the record reaches **Open** status.
