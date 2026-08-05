# Print School Academic Term

> **Module:** ssi_school\
> **Model:** `school_academic_term`\
> **Menu:** School > Configuration > Period > Academic Terms\
> **Actor:** user in group `Academic Term`\
> **Requires:** `01-create`

## Pre-Condition

- **Config:** At least one `print_document_type` (with a linked report for
  `school_academic_term`) is configured, so a report is available to select in step 4.
- **Access:** User is in group `Academic Term`.

## Flow

1. Open the **School > Configuration > Period > Academic Terms** menu.
2. Open the record to print.
3. Click **Print** in the header.
4. In the **Select Report To Print** wizard, select a **Type** (optional filter) and the
   **Report Template** to generate.
5. Click **Print**.

## Post-Condition

- The selected report is generated and opened/downloaded.
