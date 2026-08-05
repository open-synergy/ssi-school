# Create Enrollment

> **Module:** ssi*school\
> **Model:** `school_enrollment`\
> **Menu:** School > Student Activities > Enrollments\
> **Actor:** user in group \_Enrollment — User*\
> **State:** `—` → `draft`\
> **Inline Actions:** `action_compute_payment` (Compute Payment), `action_create_invoice`
> (Create Invoice), `action_delete_invoice` (Delete Invoice), `action_disconnect_invoice`
> (Disconnect Invoice), `action_mark_as_manual` (Mark as Manual), `action_unmark_as_manual`
> (Unmark as Manual), `action_open_duplicate_wizard` (Duplicate)

## Pre-Condition

- **Data:** The destination Academic Year, Academic Term (open for enrollment), School,
  Grade, and Grade Class already exist.
- **Data:** At least one Student is eligible for the selected Grade/Term (a Draft
  student whose `next_grade_id` matches the Grade, on the first term of the year, or
  whose `current_grade_id` matches the Grade on later terms).
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group (needed later by `04-confirm`).
- **Access:** User is in group _Enrollment — User_.

## Flow

1. Open the **School > Student Activities > Enrollments** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Academic Year** _(required)_: Select the academic year of this enrollment.
   - **Academic Term** _(required)_: Select the term, restricted to terms of the
     selected Academic Year that are open for enrollment.
   - **School** _(required)_: Select the destination school.
   - **Grade** _(required)_: Select the class level, restricted to the school's Grade
     Type.
   - **Student** _(required)_: Select the student, restricted to students eligible for
     the selected Grade/Term.
   - **Grade Class** _(required)_: Select the homeroom class, restricted to classes that
     belong to the selected Grade and School.
   - **Homeroom**: Optional. The Homeroom batch this enrollment is generated from or
     linked to, if any.
   - **Date**: Defaults to today's date. Change if needed.
   - **Currency**: Defaults to the company currency. Change if needed.
   - **Pricelist**: Optional. Restricted to pricelists that match the selected Currency.
   - **Payment Template**: Optional. Restricted to templates that match the selected
     Academic Term, School, and Grade (or templates that leave any of these open). Used
     by **Compute Payment** below and by **Homeroom**'s enrollment generation.
4. On the **Billing** tab, click **Compute Payment** to replace the **Payment Terms**
   tab with the billing lines defined by the selected **Payment Template** (each
   template term becomes a Payment Term, with its detail lines copied in). This requires
   a **Payment Template** to be selected first, and only works while the record is in
   Draft. You may also add, edit, or remove Payment Terms manually instead of, or after,
   using this button — skipping it leaves **Payment Terms** empty and no billing will be
   generated for this enrollment.
5. On each Payment Term line (whether added by **Compute Payment** or manually), the
   following buttons may be used once the term is Uninvoiced or Invoiced:
   - **Create Invoice**: Available when the term's status is **Uninvoiced**. Creates a
     customer invoice for that term immediately, instead of waiting for
     `19-create-due-invoice`.
   - **Delete Invoice**: Available when the term's status is **Invoiced**. Deletes the
     linked draft customer invoice and returns the term to **Uninvoiced**.
   - **Disconnect Invoice**: Available when the term's status is **Invoiced**. Removes
     the link to the customer invoice without deleting it.
   - **Mark as Manual**: Available when the term's status is **Uninvoiced**. Flags the
     term as manually handled, excluding it from automatic due-invoice generation
     (`19-create-due-invoice`).
   - **Unmark as Manual**: Available when the term is marked **Manual**. Reverts the
     term to normal automatic handling.
   - **Duplicate**: Available while the enrollment is in Draft. Opens a wizard to create
     a copy of the term (with all its detail lines) under a new **Term Name**,
     **Sequence**, **Estimated Invoice Date**, and **Estimated Due Date**; click
     **Duplicate** (`action_duplicate`) in the wizard footer to confirm. Useful for
     creating a similar billing term without repeating every detail line manually.
6. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- If **Compute Payment** was used, the **Payment Terms** tab is filled according to the
  selected Payment Template, and the **Payment Summary** tab is recomputed from the
  detail lines.
