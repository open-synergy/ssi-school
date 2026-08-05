# Restart Approval Process — School Incident Weekly Review

> **Module:** ssi*school_incident\
> **Model:** `school_incident_weekly_review`\
> **Menu:** School > Incident > Weekly Case Reviews\
> **Actor:** user in group \_Officer (Counselor/Vice Principal)* or higher\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**, and the approval process is stalled
  (for example, the record currently has no approval template assigned, or the assigned
  template no longer matches).
- **Config:** An active `policy.template` for this model grants `restart_approval_ok`
  for state `confirm` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record, with an
  approver group configured for its approval level, so the process can be rebuilt once
  restarted.
- **Access:** User is in group _Officer (Counselor/Vice Principal)_ or higher.

## Flow

1. Open the **School > Incident > Weekly Case Reviews** menu.
2. Open the record whose approval process is stalled.
3. Click the **Restart Approval Process** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status remains **Waiting for Approval**.
- The existing approval records are discarded and a new approval process is created from
  the approval template that now matches the record.
