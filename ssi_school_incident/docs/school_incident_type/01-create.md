# Create Incident Type

## Pre-Condition

- None.

## Flow

1. Open the **School > Configuration > Configuration > Incident Types** menu.
2. Click the **New** button.
3. Fill in the required fields:
   - **Code**: Enter a unique code identifying this incident type.
   - **Name**: Enter the name of the incident type (e.g. "Bullying", "Academic").
   - **Default Handling Level**: Select the handling tier that will be assigned by
     default to incidents of this type (Tier 1 - Homeroom Teacher, Tier 2 -
     Counselor/Vice Principal, or Tier 3 - Principal).
   - **First Contact SLA (Hour)**: Enter the maximum number of hours, from the moment an
     incident of this type is logged, before the assigned handler must make first
     contact with the parties involved.
   - **Is Health-Related**: Check this box if this incident type follows the separate
     Health Protocol SLA and escalation path instead of the standard incident handling
     SLA.
4. Click **Save**.

## Post-Condition

- A new Incident Type record is created and active.
- The new Incident Type becomes selectable from the Incident Type field of a School
  Incident.
