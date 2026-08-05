# Create Grade Class

> **Module:** ssi_school\
> **Model:** `school_grade_class`\
> **Menu:** School > Configuration > Grade > Grade Classes\
> **Actor:** user in group `Grade Class`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Data:** At least one **School** and a matching **Grade** already exist.
- **Access:** User is in group `Grade Class`.

## Flow

1. Open the **School > Configuration > Grade > Grade Classes** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the homeroom class (e.g. "Grade 1A").
   - **Code** _(required)_: Enter a unique code identifying this grade class, or enter
     **/** to assign it later using **Generate Code**.
   - **School** _(required)_: Select the school where this homeroom class is located.
   - **Grade Type**: Automatically filled from **School**. Read-only.
   - **Grade** _(required)_: Select the class level for this homeroom. Automatically
     reset to empty whenever **School** is changed.
   - **Capacity**: Maximum number of students this class can hold. Leave at **0** for
     unlimited capacity (no enrollment cap enforced). Optional.
4. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `school_grade_class`. This requires an active
   `sequence.template` for this model — without one, the action fails with an error. You
   may also leave the Code field as **/** or type a code manually instead.
5. Click **Save**.

## Post-Condition

- A new Grade Class record is created and active.
- **Student Count** and **Available Seat** are read-only fields, computed live from
  active (Open state) enrollments assigned to this class.
- The new Grade Class becomes selectable from the Grade Class field of an Enrollment.
