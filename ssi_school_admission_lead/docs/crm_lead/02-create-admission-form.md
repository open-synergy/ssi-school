# Create Admission Form from CRM Lead

> **Module:** ssi*school_admission_lead\
> **Model:** `crm.lead`\
> **Menu:** CRM > Leads\
> **Actor:** user with CRM Lead access (e.g. \_Sales / User: Own Documents Only* or higher)\
> **Extends:** crm.lead (Odoo core CRM) — no base Instruksi Kerja exists for this model

## Pre-Condition

- **Record:** **Can Create Admission Form** is checked, i.e. this lead has no
  **Admission Form** linked yet. Once an **Admission Form** is linked, this button opens
  that record instead of creating a new one.
- **Data:** A `crm.lead` record already exists (created via standard CRM Lead creation —
  see the fields this module and `ssi_school_lead` add in `docs/crm_lead/01-create.md`).
- **Data:** At least one `school_academic_term` exists with **Is Open Admission**
  checked, so the wizard can pre-fill **Academic Year**/**Academic Term**. An active
  `school_admission_fee_template` for the chosen **School**/**Grade** is optional — it
  only pre-fills **Fee Template** on the wizard.
- **Config:** The CRM app's **Leads** feature is enabled (Settings > CRM > Leads), so
  the **Leads** menu is visible.
- **Access:** User is in group _Admission Form — User_ (required to create the
  `school_admission_form` document; the wizard itself only needs standard internal user
  access).

## Flow

1. Open the **CRM > Leads** menu.
2. Open the lead record for the prospective student.
3. Click the **Create Admission Form** button (`action_create_admission_form`).
4. In the **Create Admission Form** wizard, fill in:
   - **Lead**: Pre-filled with this lead, read-only.
   - **Date**: Automatically filled with today's date. Change if needed.
   - **Academic Year** _(required)_: Automatically filled with the year of the earliest
     academic term open for admission, if any. Change if needed.
   - **Academic Term** _(required)_: Automatically filled together with **Academic
     Year**, if any. The list is filtered by the selected **Academic Year** and only
     shows terms open for admission. Change if needed.
   - **Pricelist** _(required)_: Select the pricelist applied to the admission fees.
   - **School** _(required)_: Automatically filled from the lead's **School**, if set.
     Change if needed. Resets **Grade** and **Fee Template** when changed.
   - **Grade** _(required)_: Select the grade level. The list is filtered by the
     selected **School**'s **Grade Type**. Resets **Fee Template** when changed. Not
     pre-filled from the lead's own **Grade** field, even when set.
   - **Student** _(required)_: Automatically filled from the lead's **Student**, if set.
     Change if needed.
   - **Parent** _(required)_: Select the parent/guardian contact.
   - **Fee Template**: Automatically cleared when **School** or **Grade** changes.
     Optional — selecting one (filtered by **School**/**Grade**) pre-fills the admission
     form's **Journal** and **Account**.
5. Click the **Create** button (`action_confirm`).

## Post-Condition

- A new `school_admission_form` document is created in **Draft** status from the
  wizard's values. If a **Fee Template** was selected, its **Journal** and **Account**
  are copied onto the new document.
- The lead's **Admission Form** field is set to the new `school_admission_form`
  document.
- The new `school_admission_form` document's form opens directly.
