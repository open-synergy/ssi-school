# Create School Incident

> **Module:** ssi*school_incident\
> **Model:** `school_incident`\
> **Menu:** School > Incident > Incidents\
> **Actor:** user in group \_User (Homeroom Teacher)* or higher\
> **State:** `—` → `draft`

## Pre-Condition

- None.

## Flow

1. Open the **School > Incident > Incidents** menu.
2. Click the **New** button.
3. Fill in the required fields:
   - **Incident Date**: Defaults to today. Change if the case occurred on a different
     date.
   - **Student**: Select the student involved in this incident case.
   - **Enrollment**: Automatically filled from **Student** (the student's active
     enrollment). Change if needed.
   - **Grade Class**: Automatically filled from **Student** (the student's homeroom
     class). Change if needed.
   - **Parent/Guardian Contact**: Automatically filled from **Student** (the student's
     Father, Mother, or Guardian contact, in that order of preference). Change if
     needed.
   - **Incident Type**: Select the category/type of incident or parent complaint being
     logged.
   - **Handling Level**: Automatically filled from **Incident Type** (Default Handling
     Level). Change if needed.
   - **Description**: Enter a one-sentence description of what happened.
4. Optionally fill in the other fields available in Draft status:
   - **Handled By**: Defaults to the current user. Change if a different staff member is
     responsible for handling this case.
   - **Contact Method**: Select the channel that will be used to make first contact with
     the parties involved.
   - **First Contact Date**: Enter the date/time the assigned handler first contacted
     the parties involved, or leave empty until the first Parent Contacts log entry is
     recorded.
   - **Action Taken**: Describe the concrete action(s) taken to handle this case.
   - **Resolution Status**: Defaults to **In Progress**. Change if the case is already
     Resolved, Not Resolved, or Escalated.
   - **Resolution Date**: Required once Resolution Status is set to a Resolved value.
5. Click **Save**.

## Post-Condition

- A new School Incident record is created in **Draft** status.
- The Document Number remains **/** until the record reaches **Open** status.
