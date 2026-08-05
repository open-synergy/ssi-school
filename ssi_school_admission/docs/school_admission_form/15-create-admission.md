# Create Admission — Admission Form

> **Module:** ssi*school_admission\
> **Model:** `school_admission_form`\
> **Menu:** School > Admission > Forms\
> **Actor:** user in group \_Admission Form — User*\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Done**.
- **Config:** An active `policy.template` for this model grants `create_admission_ok`
  for state `done` to the actor's group.
- **Access:** User is in group _Admission Form — User_.

## Flow

1. Open the **School > Admission > Forms** menu.
2. Open the record (status **Done**) to generate an admission from.
3. Click the **Create Admission** button.
4. In the **Create School Admission** wizard:
   - **Admission Form**: Pre-filled with this record, read-only.
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
5. Click **Create Admission** (`action_create_admission`) in the wizard footer.

## Post-Condition

- If this admission form does not yet have a linked `school_admission`, a new one is
  created in **Draft** status from the wizard's values, and its form opens directly.
- If a `school_admission` is already linked to this form, that existing record is opened
  instead and no new one is created.
