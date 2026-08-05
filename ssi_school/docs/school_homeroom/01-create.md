# Create Homeroom

> **Module:** ssi*school\
> **Model:** `school_homeroom`\
> **Menu:** School > Student Activities > Homerooms\
> **Actor:** user in group \_Homeroom — User*\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** The destination Academic Year, Academic Term, School, Grade, and Grade Class
  already exist.
- **Data:** At least one Student is eligible for the selected Grade/Term (a Draft
  student whose `next_grade_id` matches the Grade, on the first term of the year, or
  whose `current_grade_id` matches the Grade on later terms).
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group (needed later by `04-confirm`).
- **Access:** User is in group _Homeroom — User_.

## Flow

1. Open the **School > Student Activities > Homerooms** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Academic Year** _(required)_: Select the academic year of this Homeroom batch.
   - **Academic Term** _(required)_: Select the term, restricted to terms of the
     selected Academic Year.
   - **School** _(required)_: Select the school.
   - **Grade** _(required)_: Select the class level, restricted to the school's Grade
     Type.
   - **Grade Class** _(required)_: Select the physical classroom, restricted to classes
     that belong to the selected Grade and School.
   - **Teacher**: Optional. The homeroom teacher responsible for this batch.
   - **Date**: Defaults to today's date. Change if needed.
   - **Capacity**: Automatically filled from **Grade Class**. Change if needed.
4. On the **Generate Enrollments** tab, select **Candidate Students** manually, or use
   `15-fill-random`/`16-generate-enrollments` after saving to fill and generate them in
   bulk.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
