# Create Grade Type

> **Module:** ssi_school\
> **Model:** `school_grade_type`\
> **Menu:** School > Configuration > Grade > Grade Types\
> **Actor:** user in group `Grade Type`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group `Grade Type`.

## Flow

1. Open the **School > Configuration > Grade > Grade Types** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the education level type (e.g.
     "Elementary", "Junior High", "Senior High").
   - **Code** _(required)_: Enter a unique code identifying this grade type, or enter
     **/** to assign it later using **Generate Code**.
   - **Sequence**: Automatically defaulted to **10**. Change it to control the display
     order among Grade Types — lower values appear first.
4. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `school_grade_type`. This requires an active
   `sequence.template` for this model — without one, the action fails with an error. You
   may also leave the Code field as **/** or type a code manually instead.
5. Click **Save**.

## Post-Condition

- A new Grade Type record is created and active.
- The new Grade Type becomes selectable from the Type field of a Grade, and from the
  Grade Type field of a School.
