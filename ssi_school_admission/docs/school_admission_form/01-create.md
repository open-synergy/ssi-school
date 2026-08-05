# Create Admission Form

> **Module:** ssi*school_admission\
> **Model:** `school_admission_form`\
> **Menu:** School > Admission > Forms\
> **Actor:** user in group \_Admission Form — User*\
> **State:** `—` → `draft`\
> **Inline Actions:** `action_compute_fee` (Compute Fee), `action_compute_tax` (Compute Tax)

## Pre-Condition

- **Config:** An active `sequence.template` exists for this model, so the form receives
  a document number once it reaches **On Progress**.
- **Data:** The **Student**, **Parent**, **School**, **Grade**, and **Pricelist**
  records already exist.
- **Data:** (Optional) An active `school_admission_fee_template` exists for the selected
  **School**/**Grade**, so fee lines can be generated with **Compute Fee** instead of
  entered manually.
- **Access:** User is in group _Admission Form — User_.

## Flow

1. Open the **School > Admission > Forms** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Date**: Automatically filled with today's date. Change if needed.
   - **Academic Year** _(required)_: Select the academic year for this admission.
   - **Academic Term** _(required)_: Select the academic term. The list is filtered by
     the selected **Academic Year**.
   - **Student Name** _(required)_: Select the prospective student.
   - **Parent Name** _(required)_: Select the parent or guardian used as the billing
     partner.
   - **School** _(required)_: Select the school.
   - **Grade** _(required)_: Select the grade level applied for.
   - **Pricelist** _(required)_: Select the pricelist used for fee calculation.
4. On the **Fee Details** tab, optionally select a **Fee Template** (filtered by the
   selected **School**/**Grade**). This automatically fills **Journal** and **Account**
   on the **Accounting** tab from the template. Change if needed.
5. Click **Compute Fee** to populate the **Fee Details** lines from the selected **Fee
   Template**, replacing any existing lines. Click **OK** on the confirmation dialog.
   You may also add or edit fee lines manually instead — a **Fee Template** is not
   required. If no fee lines exist when the form is opened, its total is zero and it is
   treated as a free admission (see Post-Condition of `09-finish`).
6. On the **Accounting** tab, click **Compute Tax** to (re)compute the **Taxes** lines
   from the taxes configured on the fee lines. Skip this if the fee lines carry no
   taxes.
7. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
