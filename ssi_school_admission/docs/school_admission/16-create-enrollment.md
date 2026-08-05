# Create Enrollment — Admission

> **Module:** ssi*school_admission\
> **Model:** `school_admission`\
> **Menu:** School > Admission > Admissions\
> **Actor:** user in group \_Admission — User*\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress**. This admission's **School Student** (**Result**
  tab) already exists — it is created automatically when the admission opens, see
  `05-approve`.
- **Config:** An active `policy.template` for this model grants `create_enrollment_ok`
  for state `open` to the actor's group.
- **Access:** User is in group _Admission — User_.

## Flow

1. Open the **School > Admission > Admissions** menu.
2. Open the record (status **On Progress**) to generate an enrollment from.
3. Click the **Create Enrollment** button (`action_create_enrollment`) in the header.
4. In the **Create Enrollment** wizard:
   - **Grade Class** _(required)_: Select the homeroom class the student will be placed
     in.
   - **Payment Template**: Optional. Selecting one automatically fills **Customer
     Invoice Type** and **Auto Confirm Customer Invoice** below. Change if needed. If
     left empty, no payment terms are generated on the enrollment.
   - **Currency**: Automatically filled from this admission's **Currency**. Change if
     needed.
   - **Pricelist**: Automatically filled from this admission's **Pricelist**. Change if
     needed.
   - **Receivable Journal**: Automatically filled from this admission's **Receivable
     Journal**. Change if needed.
   - **Receivable Account**: Automatically filled from this admission's **Receivable
     Account**. Change if needed.
   - **Customer Invoice Type**: Automatically filled if **Payment Template** is
     selected. Change if needed.
   - **Auto Confirm Customer Invoice**: Automatically filled if **Payment Template** is
     selected. Change if needed.
5. Click **Create Enrollment** in the wizard footer.

## Post-Condition

- If this admission does not yet have a linked `school_enrollment`, a new one is created
  in **Draft** status, using this admission's **Academic Year**/**Academic Term**/
  **School**/**Grade** and the wizard's **Grade Class**/**Payment Template**/billing
  values. Its form opens directly, and this admission's **Enrollment** field (**Result**
  tab) is linked to it.
- If a `school_enrollment` is already linked to this admission, that existing record is
  opened instead and no new one is created (no wizard is shown in this case).
