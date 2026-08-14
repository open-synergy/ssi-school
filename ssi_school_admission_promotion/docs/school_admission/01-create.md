# Create Admission

> **Module:** ssi_school_admission_promotion\
> **Extends:** ssi_school_admission — model `school_admission`, action `01-create`\
> **Inline Actions:** `action_apply_promotion_code` (Apply Promotion Code)

## Modified Flow

- Anchor: on base Flow step 6 (the payment term row buttons), an **Apply Promotion
  Code** button (`action_apply_promotion_code`) becomes available once that term is
  **Invoiced**. Click it to open the **Apply Promotion Code** wizard:

  - **Promotion Code** _(required)_: select a promotion code in state Open.
  - **Date** _(required)_: defaults to today's date. Change if needed.
  - **Voucher User**: automatically filled from this term's own partner (the student of
    the parent admission), shown read-only.

  Click **Apply Promotion Code** in the wizard footer to create one **Promotion Code
  Usage** in Draft status referencing this term, with its own **Allocations** filled
  automatically from the term's own invoice receivable journal item.

## Additional Post-Condition

- The **Promotions** column on the Payment Term line (`promotion_usage_count`)
  recomputes to the number of Promotion Code Usage records referencing that term.
