# Create School Admission — Admission Test

> **Module:** ssi*school_admission\
> **Model:** `school_admission_test`\
> **Menu:** School > Admission > Tests\
> **Actor:** user in group \_Admission Test — User*\
> **Requires:** `09-finish`

## Pre-Condition

- **Record:** Status is **Done**, and **Passed** is checked — see `09-finish`.
- **Config:** An active `policy.template` for this model grants
  `create_school_admission_ok` for state `done` to the actor's group.
- **Access:** User is in group _Admission Test — User_.

## Flow

1. Open the **School > Admission > Tests** menu.
2. Open the record (status **Done**, **Passed**) to generate an admission from.
3. Click the **Create School Admission** button.
4. In the **Create School Admission** wizard:
   - **Admission Test**: Pre-filled with this record, read-only.
   - **Currency**: Automatically filled with the company currency. Change if needed.
   - **Pricelist**: Optional. The list is filtered by the selected **Currency**.
   - **Payment Template**: Optional. Selecting one automatically fills **Customer
     Invoice Type** and **Auto Confirm Customer Invoice** below. Change if needed.
   - **Receivable Journal**: Optional.
   - **Receivable Account**: Optional.
   - **Customer Invoice Type**: Automatically filled if **Payment Template** is
     selected. Change if needed.
   - **Auto Confirm Customer Invoice**: Automatically filled if **Payment Template** is
     selected. Change if needed.
5. Click **Create Admission**.

## Post-Condition

- If this admission test does not yet have a linked `school_admission`, a new one is
  created in **Draft** status from the wizard's values (also linked to this test's
  **Admission Form**, if any), and its form opens directly — see
  `ssi_school_admission/school_admission/01-create`.
- If a `school_admission` is already linked to this test, that existing record is opened
  instead and no new one is created.
