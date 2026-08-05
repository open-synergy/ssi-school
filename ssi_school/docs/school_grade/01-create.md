# Create Grade

> **Module:** ssi_school\
> **Model:** `school_grade`\
> **Menu:** School > Configuration > Grade > Grades\
> **Actor:** user in group `Grade`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Data:** At least one **Grade Type** already exists.
- **Access:** User is in group `Grade`.

## Flow

1. Open the **School > Configuration > Grade > Grades** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the class level (e.g. "Grade 1", "Grade
     2").
   - **Code** _(required)_: Enter a unique code identifying this grade, or enter **/**
     to assign it later using **Generate Code**.
   - **Type** _(required)_: Select the education level type this grade belongs to (e.g.
     Elementary).
   - **Sequence**: Automatically defaulted to **10**. Change it to control the ordering
     of class levels within the selected Type — lower values represent lower grades.
4. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `school_grade`. This requires an active
   `sequence.template` for this model — without one, the action fails with an error. You
   may also leave the Code field as **/** or type a code manually instead.
5. Click **Save**.

## Post-Condition

- A new Grade record is created and active.
- **Previous Grade** and **Next Grade** are read-only fields, automatically computed and
  kept consistent by the system based on the ordering of **Sequence** within the
  selected **Type**.
- The new Grade becomes selectable wherever a Grade is referenced (e.g. Grade Class,
  Student Initial Grade).
