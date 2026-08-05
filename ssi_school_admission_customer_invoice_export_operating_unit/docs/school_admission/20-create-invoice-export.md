# Create Invoice Export — Admission

> **Module:** ssi_school_admission_customer_invoice_export_operating_unit\
> **Extends:** ssi_school_admission_customer_invoice_export — model `school_admission`, action
> `20-create-invoice-export`

## Modified Flow

- Anchor: on the base Flow's step 5 (fill in the **Create Invoice Export** wizard), one
  field is added before **Type**:
  - **Operating Unit** _(required)_: Automatically filled with the acting user's default
    operating unit. Change if needed. Restricts which of the collected invoice moves are
    actually exported to this operating unit, and is copied onto the resulting Customer
    Invoice Export document.

## Modified Validation

- Clicking **Create Invoice Export** in the wizard footer fails if none of the collected
  invoice moves belong to the selected **Operating Unit** — even when the base "no
  exportable move" check already passed.

## Additional Post-Condition

- The created **Customer Invoice Export** document's **Invoices**/**Invoice Lines** are
  further restricted to moves of the wizard's **Operating Unit**, and the document's own
  **Operating Unit** is set to that value.
