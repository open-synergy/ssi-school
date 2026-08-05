# Print School Incident Weekly Review

> **Module:** ssi_school_incident\
> **Model:** `school_incident_weekly_review`\
> **Menu:** School > Incident > Weekly Case Reviews\
> **Actor:** any authenticated user\
> **Requires:** `01-create`

## Pre-Condition

- **Config:** At least one `print_document_type` (with a linked report for
  `school_incident_weekly_review`) is configured, so a report is available to select in
  step 4.
- **Access:** User has read access to School Incident Weekly Review (granted to every
  authenticated user by the model's global access rule).

## Flow

1. Open the **School > Incident > Weekly Case Reviews** menu.
2. Open the record to print.
3. Click **Print** in the header.
4. In the **Select Report To Print** wizard, select a **Type** (optional filter) and the
   **Report Template** to generate.
5. Click **Print**.

## Post-Condition

- The selected report is generated and opened/downloaded.
