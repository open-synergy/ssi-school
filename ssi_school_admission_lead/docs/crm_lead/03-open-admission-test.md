# Open Admission Test from CRM Lead

> **Module:** ssi_school_admission_lead\
> **Model:** `crm.lead`\
> **Menu:** CRM > Leads\
> **Actor:** user with CRM Lead access and read access to `school_admission_test`\
> **Extends:** crm.lead (Odoo core CRM) — no base Instruksi Kerja exists for this model

## Pre-Condition

- **Record:** **Admission Test** is set on this lead. The button is hidden otherwise.
  This field is populated from the **Admission Test** linked to the lead's **Admission
  Form**, once that form's own workflow reaches that point.
- **Access:** User is in group _Admission Test — User_ (or otherwise has read access to
  `school_admission_test`).

## Flow

1. Open the **CRM > Leads** menu.
2. Open the lead record whose **Admission Test** field is set.
3. Click the **Admission Test** button (`action_open_admission_test`).

## Post-Condition

- The linked `school_admission_test` document's form opens, replacing the lead's own
  form view.
