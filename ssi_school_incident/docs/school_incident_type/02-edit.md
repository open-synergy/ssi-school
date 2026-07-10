# Edit Incident Type

## Pre-Condition

- None.

## Flow

1. Open the **School > Configuration > Configuration > Incident Types** menu.
2. Find and open the Incident Type record to edit.
3. Change the required fields (Code, Name, Default Handling Level, First Contact SLA
   (Hour), Is Health-Related).
4. Click **Save**.

## Post-Condition

- The Incident Type record is updated with the new values.
- School Incident cases already logged with this Incident Type keep their own Handling
  Level and SLA values (they are only defaulted at creation time, via onchange); only
  new cases pick up the updated defaults.
