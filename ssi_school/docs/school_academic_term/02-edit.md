# Edit School Academic Term

> **Module:** ssi_school\
> **Model:** `school_academic_term`\
> **Menu:** School > Configuration > Period > Academic Terms\
> **Actor:** user in group `Academic Term`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group `Academic Term`.

## Flow

1. Open the **School > Configuration > Period > Academic Terms** menu.
2. Find and open the record to edit.
3. Change the required fields (**Name**, **Code**, **Academic Year**, **Date Start**,
   **Date End**).
4. Click **Generate Code** in the header to assign a new code from the
   `sequence.template` configured for `school_academic_term` — for example after
   changing the Code field back to **/**. This requires an active `sequence.template`
   for this model — without one, the action fails with an error.
5. Click **Save**. Saving fails with a validation error if **Date End** is not after
   **Date Start**, or if the term dates fall outside the Academic Year's date range.

## Post-Condition

- The record is updated with the new values.
- **First Term of Academic Year?** and **Last Term of Academic Year?** are recomputed if
  **Academic Year** was changed.
