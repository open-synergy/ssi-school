# Fill in the Weekly Case Review Checklist

> **Module:** ssi*school_incident\
> **Model:** `school_incident_weekly_review`\
> **Menu:** School > Incident > Weekly Case Reviews\
> **Actor:** user in group \_Weekly Review User* or higher\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, or **Waiting for Approval**/**Rejected** if the
  checklist still needs correction before re-confirming.

## Flow

1. Open the **School > Incident > Weekly Case Reviews** menu.
2. Open the Weekly Case Review record.
3. Open the **Weekly Review Checklist** page.
4. After manually verifying each item against the collected Incidents (and the Master
   Log), tick the corresponding checkbox:
   - **Master Log Updated** (Agenda 1): every case that occurred in the period has a
     corresponding School Incident record.
   - **Not Resolved > 7 Days Flagged** (Agenda 2): every case counted in the **Not
     Resolved > 7 Days** stat button has been flagged/escalated to the handler and/or
     their supervisor for follow-up.
   - **SLA Breach Identified** (Agenda 3): every case counted in the **Overdue** stat
     button has been identified and communicated to the relevant handling tier.
   - **Agenda 5 - Escalation Criteria Audited**: every case counted in the **Escalated**
     stat button has at least one Escalation Criteria entry recorded as its
     justification.
   - **Agenda 6 - Health Case Summary Available**: a summary of this period's
     health-related cases (Incident Type flagged Is Health-Related) has been prepared
     and reviewed.
5. Optionally fill in the **Note** field with free-text minutes or follow-up notes from
   the review meeting.
6. Click **Save**.

## Post-Condition

- The checklist reflects the officer's manual review of this period's cases. Ticking a
  checkbox only records that the manual audit was performed; it does not itself enforce
  or verify compliance.
