# Edit Admission

> **Module:** ssi_school_admission_promotion\
> **Extends:** ssi_school_admission — model `school_admission`, action `02-edit`\
> **Inline Actions:** `action_apply_promotion_code` (Apply Promotion Code)

## Modified Flow

- Anchor: on base Flow step 5 (the payment term row buttons), the **Apply Promotion
  Code** button may be used the same way as described in `01-create`. A payment term
  that is already locked — every term is locked once the admission is opened — can still
  be given a promotion, because applying one writes nothing back to the term.
