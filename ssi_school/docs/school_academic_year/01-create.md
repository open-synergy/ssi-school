# Create Academic Year

> **Module:** ssi_school\
> **Model:** `school_academic_year`\
> **Menu:** School > Configuration > Period > Academic Years\
> **Actor:** user in group `Academic Year`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group `Academic Year`.

## Flow

1. Open the **School > Configuration > Period > Academic Years** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the academic year (e.g. "2024/2025").
   - **Code** _(required)_: Enter a unique code identifying this academic year, or enter
     **/** to assign it later using **Generate Code**.
   - **Date Start** _(required)_: Enter the start date of this academic year.
   - **Date End** _(required if **Date Start** is filled)_: Enter the end date of this
     academic year. Must be after **Date Start**.
4. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `school_academic_year`. This requires an active
   `sequence.template` for this model — without one, the action fails with an error. You
   may also leave the Code field as **/** or type a code manually instead.
5. Click **Save**. Saving fails with a validation error if **Date End** is not after
   **Date Start**.

## Post-Condition

- A new Academic Year record is created and active.
- The **Terms** tab starts empty. **First Term** and **Last Term** remain empty until
  School Academic Term records for this Academic Year are created (outside the scope of
  this Instruction).
