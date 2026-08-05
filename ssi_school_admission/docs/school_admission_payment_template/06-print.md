# Print Admission Payment Template

> **Module:** ssi_school_admission\
> **Model:** `school_admission_payment_template`\
> **Menu:** School > Configuration > Admission > Payment Templates\
> **Actor:** user in group `Admission Payment Template`\
> **Requires:** `01-create`

## Pre-Condition

- **Config:** At least one `print_document_type` (with a linked report for
  `school_admission_payment_template`) is configured, so a report is available to select
  in step 4.
- **Access:** User is in group `Admission Payment Template`.

## Flow

1. Open the **School > Configuration > Admission > Payment Templates** menu.
2. Open the record to print.
3. Click **Print** in the header.
4. In the **Select Report To Print** wizard, select a **Type** (optional filter) and the
   **Report Template** to generate.
5. Click **Print**.

## Post-Condition

- The selected report is generated and opened/downloaded.
