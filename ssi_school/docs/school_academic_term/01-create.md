# Create School Academic Term

> **Module:** ssi_school\
> **Model:** `school_academic_term`\
> **Menu:** School > Configuration > Period > Academic Terms\
> **Actor:** user in group `Academic Term`\
> **State:** `—` → `draft`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Data:** At least one **Academic Year** record exists to link this term to.
- **Access:** User is in group `Academic Term`.

## Flow

1. Open the **School > Configuration > Period > Academic Terms** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the term (e.g. "Semester 1").
   - **Code** _(required)_: Enter a unique code identifying this term, or enter **/** to
     assign it later using **Generate Code**.
   - **Academic Year** _(required)_: Select the Academic Year this term belongs to.
   - **Date Start** _(required)_: Enter the first date of this term.
   - **Date End** _(required)_: Enter the last date of this term. Must be after **Date
     Start**, and both dates must fall within the selected Academic Year's date range.
4. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `school_academic_term`. This requires an active
   `sequence.template` for this model — without one, the action fails with an error. You
   may also leave the Code field as **/** or type a code manually instead.
5. Click **Save**. Saving fails with a validation error if **Date End** is not after
   **Date Start**, or if the term dates fall outside the Academic Year's date range.

## Post-Condition

- A new record is created in **Unstarted** status, with **Enrollment State** set to
  **Close**.
- **First Term of Academic Year?** and **Last Term of Academic Year?** are computed
  automatically based on whether this record matches the selected Academic Year's First
  Term / Last Term selection.
