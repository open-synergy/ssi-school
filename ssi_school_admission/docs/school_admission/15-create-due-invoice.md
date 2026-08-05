# Create Due Invoice — Admission

> **Module:** ssi*school_admission\
> **Model:** `school_admission`\
> **Menu:** School > Admission > Admissions\
> **Actor:** user in group \_Admission — User*\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Record:** At least one **Payment Terms** line is **Uninvoiced** with an estimated
  invoice date (**Date Invoice**) at or before today (or before the **Date End** used in
  step 4).
- **Config:** An active `policy.template` for this model grants `create_invoice_ok` for
  state `open` to the actor's group.
- **Access:** User is in group _Admission — User_.

## Flow

1. Open the **School > Admission > Admissions** menu.
2. Open the record (status **On Progress**) whose due payment terms should be invoiced.
3. Click the **Create Due Invoice** button (`action_open_create_due_invoice_wizard`) in
   the header.
4. In the **Create Due Invoice** wizard:
   - **Admissions**: Pre-filled with this record.
   - **Date Start**: Optional. Leave empty for no lower bound.
   - **Date End**: Optional. Leave empty to process up to today.
5. Click **Create Due Invoice** (`action_create_due_invoice`) in the wizard footer.

## Post-Condition

- A customer invoice is created for each **Uninvoiced**, non-manual **Payment Terms**
  line whose **Date Invoice** falls within the selected range, and each such line's
  **Customer Invoice** field is linked to the resulting invoice.
- The wizard closes; no navigation occurs.

> **Note:** This wizard can also be run in bulk over several admissions selected from
> the\
> **School > Admission > Admissions** list view, via **Action > Create Due Invoice** —\
> every selected admission must individually pass the `create_invoice_ok` policy.
