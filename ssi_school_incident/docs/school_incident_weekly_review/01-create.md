# Create School Incident Weekly Review

> **Module:** ssi*school_incident\
> **Model:** `school_incident_weekly_review`\
> **Menu:** School > Incident > Weekly Case Reviews\
> **Actor:** user in group \_Weekly Review User* or higher\
> **State:** `—` → `draft`

## Pre-Condition

- None.

## Flow

1. Open the **School > Incident > Weekly Case Reviews** menu.
2. Click the **New** button.
3. Fill in the required fields:
   - **Date Start**: Defaults to 7 days before today. Change to the start of the period
     this review covers.
   - **Date End**: Defaults to today. Change to the end of the period this review covers
     (normally the Friday the review meeting is held on).
4. Optionally fill in:
   - **School**: Select the School/unit this review is scoped to. Leave empty to review
     all Schools/units together.
5. Click **Save**.

## Post-Condition

- A new Weekly Case Review record is created in **Draft** status.
- The Incidents list is still empty; use the **Collect Incidents** button to pull in
  eligible School Incident cases.

## Related Views

- The **Total**, **Overdue**, **Not Resolved > 7d**, and **Escalated** stat buttons in
  the form's button box (`action_view_total_incidents`, `action_view_overdue_incidents`,
  `action_view_unresolved_over_7d_incidents`, `action_view_escalated_incidents`) open
  the School Incident list, pre-filtered to the corresponding subset of the incidents
  collected into this review. Each one only returns an `act_window` and writes no field,
  so they are pure navigation: informational only, not documented as IK steps or tours
  of their own.
