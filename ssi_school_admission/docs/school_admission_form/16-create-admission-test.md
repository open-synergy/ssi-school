# Create Admission Test — Admission Form

> **Module:** ssi*school_admission\
> **Model:** `school_admission_form`\
> **Menu:** School > Admission > Forms\
> **Actor:** user in group \_Admission Form — User*\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Done**.
- **Record:** No `school_admission_test` is linked to this form yet.
- **Config:** An active `policy.template` for this model grants
  `create_admission_test_ok` for state `done` to the actor's group.
- **Access:** User is in group _Admission Form — User_.

## Flow

1. Open the **School > Admission > Forms** menu.
2. Open the record (status **Done**) to generate an admission test from.
3. Click the **Create Admission Test** button (`action_create_admission_test`).

## Post-Condition

- A new `school_admission_test` record is created in **Draft** status, pre-filled with
  this form's **Date**, **Academic Year**, **Academic Term**, **School**, **Grade**,
  **Student**, and linked back to this form. Its form opens directly — see
  `ssi_school_admission/school_admission_test/01-create`.
- If this form already has a linked admission test, its form opens instead and no new
  one is created.
- The **Admission Test** field on this form becomes visible, showing the linked test.
