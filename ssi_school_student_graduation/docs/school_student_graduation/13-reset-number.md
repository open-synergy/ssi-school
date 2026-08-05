# Reset Document Number — Student Graduation

> **Module:** ssi*school_student_graduation\
> **Model:** `school_student_graduation`\
> **Menu:** School > Student Activities > Student Graduations\
> **Actor:** user in group \_School Student Graduation — Validator*\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `sequence.template` exists for this model.
- **Config:** An active `policy.template` grants `manual_number_ok` for state `draft` to
  the actor's group.
- **Access:** User is in group _School Student Graduation — Validator_.

## Flow

1. Open the **School > Student Activities > Student Graduations** menu.
2. Open the record whose document number will be reset.
3. Click the **Reset Document Number** button (or edit the **# Document** field directly
   and change it to **/**).
4. Click **OK** on the confirmation dialog (only when the button was used).

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number when it transitions to **Done**, according
  to the configured sequence.
