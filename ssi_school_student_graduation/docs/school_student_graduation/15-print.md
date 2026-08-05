# Print Student Graduation

> **Module:** ssi*school_student_graduation\
> **Model:** `school_student_graduation`\
> **Menu:** School > Student Activities > Student Graduations\
> **Actor:** user in group \_School Student Graduation — Viewer*\
> **Requires:** `01-create`

## Pre-Condition

- **Config:** At least one `print_document_type` (with a linked report for
  `school_student_graduation`) is configured, so a report is available to select in
  step 4.
- **Access:** User is in group _School Student Graduation — Viewer_.

## Flow

1. Open the **School > Student Activities > Student Graduations** menu.
2. Open the record to print.
3. Click **Print** in the header.
4. In the **Select Report To Print** wizard, select a **Type** (optional filter) and the
   **Report Template** to generate.
5. Click **Print**.

## Post-Condition

- The selected report is generated and opened/downloaded.
