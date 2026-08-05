# Print Graduation Batch

> **Module:** ssi*school_student_graduation\
> **Model:** `school_student_graduation_batch`\
> **Menu:** School > Student Activities > Graduation Batches\
> **Actor:** user in group \_School Student Graduation Batch — Viewer*\
> **Requires:** `01-create`

## Pre-Condition

- **Config:** At least one `print_document_type` (with a linked report for
  `school_student_graduation_batch`) is configured, so a report is available to select
  in step 4.
- **Access:** User is in group _School Student Graduation Batch — Viewer_.

## Flow

1. Open the **School > Student Activities > Graduation Batches** menu.
2. Open the record to print.
3. Click **Print** in the header.
4. In the **Select Report To Print** wizard, select a **Type** (optional filter) and the
   **Report Template** to generate.
5. Click **Print**.

## Post-Condition

- The selected report is generated and opened/downloaded.
