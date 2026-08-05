# Create Admission

> **Module:** ssi*school_admission\
> **Model:** `school_admission`\
> **Menu:** School > Admission > Admissions\
> **Actor:** user in group \_Admission — User*\
> **State:** `—` → `draft`\
> **Requires:** `ssi_school_admission/school_admission_test/15-create-school-admission`\
> **Inline Actions:** `action_compute_payment` (Compute Payment),
> `action_create_invoice`\
> (Create Invoice), `action_delete_invoice` (Delete Invoice), `action_disconnect_invoice`\
> (Disconnect Invoice), `action_mark_as_manual` (Mark as Manual),
> `action_unmark_as_manual`\
> (Unmark as Manual), `action_open_duplicate_wizard` (Duplicate Term)

## Pre-Condition

- **Config:** An active `sequence.template` exists for this model, so the admission
  receives a document number once it reaches **On Progress**.
- **Data:** The **School**, **Grade**, and **Student** records already exist.
- **Data:** (Optional) An active `school_admission_payment_template` exists for the
  selected **Academic Term**/**School**/**Grade**, so payment terms can be generated
  with **Compute Payment** instead of entered manually.
- **Data:** (Optional) This admission is usually generated from a **Done**
  `school_admission_form` (see
  `ssi_school_admission/school_admission_form/15-create-admission`) or a **Done**+
  **Passed** `school_admission_test` (see
  `ssi_school_admission/school_admission_test/15-create-school-admission`). It can also
  be created directly from this menu without either origin.
- **Access:** User is in group _Admission — User_.

## Flow

1. Open the **School > Admission > Admissions** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Date**: Automatically filled with today's date. Change if needed.
   - **Academic Year** _(required)_: Select the academic year.
   - **Academic Term** _(required)_: Select the academic term. The list is filtered by
     the selected **Academic Year**.
   - **School** _(required)_: Select the school.
   - **Grade** _(required)_: Select the grade level. The list is filtered by the
     school's **Grade Type**.
   - **Student** _(required)_: Select the student being admitted.
   - **Currency**: Automatically filled with the company currency. Change if needed —
     this resets **Pricelist**.
   - **Pricelist**: Optional. The list is filtered by the selected **Currency**.
4. On the **Fee** tab, optionally select a **Payment Template** (filtered by the
   selected **Academic Term**/**School**/**Grade**). This automatically fills
   **Receivable Journal**, **Receivable Account**, **Customer Invoice Type**, and **Auto
   Confirm Customer Invoice** on the **Accounting** tab from the template. Change if
   needed.
5. Click **Compute Payment** to populate the **Payment Terms** lines (and the read-only
   **Product Summary** lines) from the selected **Payment Template**, replacing any
   existing lines. Click **OK** on the confirmation dialog. You may also add or edit
   payment terms manually instead — a **Payment Template** is not required.
6. For each payment term row that needs it, use the row buttons:
   - **Create Invoice** (rows not yet invoiced) to generate a customer invoice for that
     term.
   - **Delete Invoice** / **Disconnect Invoice** (rows already invoiced) to remove the
     generated invoice, or unlink it from the term without deleting it.
   - **Mark as Manual** / **Unmark as Manual** (rows not yet invoiced / marked manual)
     to exclude a term from automatic due-invoice generation, or bring it back in.
   - **Duplicate Term** (`action_open_duplicate_wizard`) to open a small wizard
     pre-filled from the row (**Name**, **Sequence**, **Date Invoice**, **Date Due**);
     click **Duplicate** (`action_duplicate`) in it to create the copy as a new payment
     term line. These row actions are optional; if skipped, the term keeps its default
     **Uninvoiced** state until invoiced later (see `15-create-due-invoice`).
7. On the **Accounting** tab, fill in **Receivable Journal**, **Receivable Account**,
   **Customer Invoice Type**, and **Auto Confirm Customer Invoice** if not already
   filled by step 4.
8. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
