# Create Admission from CRM Lead

> **Module:** ssi*school_lead\
> **Model:** `crm.lead`\
> **Menu:** CRM > Leads\
> **Actor:** user with CRM Lead access (e.g. \_Sales / User: Own Documents Only* or higher)\
> **Extends:** crm.lead (Odoo core CRM) — no base Instruksi Kerja exists for this model

## Pre-Condition

- **Record:** **Can Create Admission** is checked, i.e. this lead has no **Admission**
  linked yet. Once an **Admission** is linked, this button opens that record instead of
  creating a new one.
- **Data:** A `crm.lead` record already exists (created via standard CRM Lead creation —
  see the fields this module adds in `docs/crm_lead/01-create.md`).
- **Data:** At least one `school_academic_term` exists with **Is Open Admission**
  checked, so the wizard can pre-fill **Academic Year**/**Academic Term**. An active
  `school_admission_payment_template` for the chosen **School**/**Grade**/**Academic
  Term** is optional — it only pre-fills **Payment Template** on the wizard.
- **Config:** The CRM app's **Leads** feature is enabled (Settings > CRM > Leads), so
  the **Leads** menu is visible.
- **Access:** User is in group _Admission — User_ (required to create the
  `school_admission` document; the wizard itself only needs standard internal user
  access).

## Flow

1. Open the **CRM > Leads** menu.
2. Open the lead record for the prospective student.
3. Click the **Create Admission** button (`action_create_admission`).
4. In the **Create Admission** wizard, fill in:
   - **Lead**: Pre-filled with this lead, read-only.
   - **Date**: Automatically filled with today's date. Change if needed.
   - **Academic Year** _(required)_: Automatically filled with the year of the earliest
     academic term open for admission, if any. Change if needed.
   - **Academic Term** _(required)_: Automatically filled together with **Academic
     Year**, if any. The list is filtered by the selected **Academic Year** and only
     shows terms open for admission. Change if needed. Resets when **Academic Year**
     changes.
   - **School** _(required)_: Automatically filled from the lead's **School**, if set.
     Change if needed. Resets **Grade** when changed.
   - **Grade** _(required)_: Select the grade level. The list is filtered by the
     selected **School**'s **Grade Type**.
   - **Student** _(required)_: Automatically filled from the lead's **Student**, if set.
     Change if needed.
   - **Payment Template**: Automatically filled if an active template matches the
     selected **School**/**Grade**/**Academic Term**. Change if needed — it determines
     the receivable journal/account and customer invoice settings applied below.
5. Click the **Create** button (`action_confirm`).

## Post-Condition

- A new `school_admission` document is created in **Draft** status from the wizard's
  values. If a **Payment Template** was selected, its payment terms are computed
  automatically on the new document.
- The lead's **Admission** field is set to the new `school_admission` document, and the
  lead's **Student** field is updated to the wizard's **Student**.
- The new `school_admission` document's form opens directly.
