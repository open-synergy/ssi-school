# Create School

> **Module:** ssi_school\
> **Model:** `school`\
> **Menu:** School > Configuration > Grade > Schools\
> **Actor:** user in group `School`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Data:** At least one **Grade Type** already exists.
- **Access:** User is in group `School`.

## Flow

1. Open the **School > Configuration > Grade > Schools** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the school entity.
   - **Code** _(required)_: Enter a unique code identifying this school, or enter **/**
     to assign it later using **Generate Code**.
   - **Grade Type** _(required)_: Select the education level type used by this school
     (e.g. Elementary, Junior High, Senior High).
   - **Center**: Automatically filled from the current company. Change if needed.
   - **Branch**: Select the branch that oversees this school unit. Leave empty if the
     unit is directly overseen by the Center. Only branches belonging to the selected
     Center are selectable, and the field is automatically cleared if Center is changed
     to a company that no longer matches the selected Branch's Center. Optional.
4. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `school`. This requires an active
   `sequence.template` for this model — without one, the action fails with an error. You
   may also leave the Code field as **/** or type a code manually instead.
5. Click **Save**. Saving fails with a validation error if **Branch** is set but its
   Center does not match this school's **Center**.

## Post-Condition

- A new School record is created and active.
- The new School becomes selectable from the School field of a Grade Class, Student, or
  Enrollment Payment Template.
