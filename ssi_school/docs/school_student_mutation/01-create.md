# Create Student Class Mutation

> **Module:** ssi*school\
> **Model:** `school_student_mutation`\
> **Menu:** School > Student Activities > Student Class Mutations\
> **Actor:** user in group \_Student Class Mutation — User*\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** The student to be moved has an open Enrollment (status **On Progress**).
- **Data:** At least one other Grade Class exists within the same Grade and School as
  the student's current Enrollment, to be selected as the destination.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group (needed later by `04-confirm`).
- **Access:** User is in group _Student Class Mutation — User_.

## Flow

1. Open the **School > Student Activities > Student Class Mutations** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Student** _(required)_: Select the student whose grade class is being changed.
   - **Enrollment** _(required)_: Automatically filled with the student's open
     Enrollment if there is exactly one. Restricted to the student's Enrollments
     currently in **On Progress**. Change if the student has more than one candidate
     (not expected in normal use).
   - **Source Grade Class**: Automatically filled from **Enrollment**.
   - **Source Homeroom**: Automatically filled from **Enrollment**.
   - **Destination Grade Class** _(required)_: Select the grade class the student will
     be moved into, restricted to classes in the same Grade and School as the
     Enrollment, excluding the current class.
   - **Destination Homeroom**: Automatically filled if an open Homeroom batch for the
     selected **Destination Grade Class** (matching the Enrollment's Academic Year,
     Term, and Grade) exists. Change if needed, or leave empty if no batch exists.
   - **Date**: Defaults to today's date. Change if needed.
   - **Reason**: Optional explanation for the mutation.
4. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
