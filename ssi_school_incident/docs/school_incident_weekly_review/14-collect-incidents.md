# Collect Incidents into School Incident Weekly Review

## Pre-Condition

- Record is in **Draft** status.
- **Date Start** and **Date End** are filled in.
- User has _Can Collect_ access right (belongs to the Officer (Counselor/Vice Principal)
  group or higher).

## Flow

1. Open the **School > Incident > Weekly Case Reviews** menu.
2. Open the Weekly Case Review record.
3. Fill in (or confirm) **Date Start**, **Date End**, and optionally **School**.
4. Click the **Collect Incidents** button.

## Post-Condition

- The **Incidents** tab (Collected Incidents) is populated with every School Incident
  whose Incident Date falls between Date Start and Date End (and, if School is set,
  whose Student belongs to that School).
- Clicking **Collect Incidents** again re-runs the same criteria and replaces the whole
  Incidents list; it never edits or cancels the underlying School Incident records
  themselves.
- The stat buttons on the form (**Total**, **Overdue**, **Not Resolved > 7d**,
  **Escalated**) update to reflect the counts of the collected incidents.
