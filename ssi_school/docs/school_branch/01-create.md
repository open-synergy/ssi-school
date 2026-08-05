# Create Branch

> **Module:** ssi_school\
> **Model:** `school_branch`\
> **Menu:** School > Configuration > Branches\
> **Actor:** user in group `Branch`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group `Branch`.

## Flow

1. Open the **School > Configuration > Branches** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the branch.
   - **Code** _(required)_: Enter a unique code identifying this branch, or enter **/**
     to assign it later using **Generate Code**.
   - **Center**: Automatically filled from the current company. Change if needed.
4. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `school_branch`. This requires an active
   `sequence.template` for this model — without one, the action fails with an error. You
   may also leave the Code field as **/** or type a code manually instead.
5. Click **Save**.

## Post-Condition

- A new Branch record is created and active.
- The new Branch becomes selectable from the Branch field of a School.

## Related Views

- The **School Units** smart button in the header opens the list of Schools overseen by
  this Branch. It only navigates to a filtered list — it does not modify any record, so
  it is not documented as a separate step.
