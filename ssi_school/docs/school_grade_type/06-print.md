# Print Grade Type

> **Module:** ssi_school\
> **Model:** `school_grade_type`\
> **Menu:** School > Configuration > Grade > Grade Types\
> **Actor:** user in group `Grade Type`\
> **Requires:** `01-create`

## Pre-Condition

- **Config:** At least one `print_document_type` (with a linked report for
  `school_grade_type`) is configured, so a report is available to select in step 4.
- **Access:** User is in group `Grade Type`.

## Flow

1. Open the **School > Configuration > Grade > Grade Types** menu.
2. Open the record to print.
3. Click **Print** in the header.
4. In the **Select Report To Print** wizard, select a **Type** (optional filter) and the
   **Report Template** to generate.
5. Click **Print**.

## Post-Condition

- The selected report is generated and opened/downloaded.
