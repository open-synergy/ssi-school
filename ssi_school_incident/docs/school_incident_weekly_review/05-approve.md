# Approve School Incident Weekly Review

## Pre-Condition

- Record is in **Waiting for Approval** status.
- User is registered as an approver on the active approval template (belongs to the
  Manager (Principal) group).
- User has _Can Approve_ access right.

## Flow

1. Open the **School > Incident > Weekly Case Reviews** menu.
2. Open the Weekly Case Review record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- The approval template for this review has a single approval level (Manager group), so
  approving it fulfills the whole approval workflow immediately.
- Status automatically moves to **Done** right after this approval (this model has no
  separate Open state and no manual "Done"/"Finish" button: the system moves the
  document from Waiting for Approval directly to Done).
- A Document Number is generated once the record reaches **Done** status.
