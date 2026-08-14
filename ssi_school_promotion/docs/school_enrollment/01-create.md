# Create Enrollment

> **Module:** ssi_school_promotion\
> **Extends:** ssi_school — model `school_enrollment`, aksi `01-create`\
> **Inline Actions:** `action_apply_promotion_code` (Apply Promotion Code)

## Modified Flow

- Anchor: on base Flow step 5 (inline buttons on the Payment Term line), an **Apply
  Promotion Code** button (`action_apply_promotion_code`) becomes available once that
  term is **Invoiced**. Click it to open the **Apply Promotion Code** wizard:

  - **Promotion Code** _(required)_: select a promotion code in state Open.
  - **Date** _(required)_: defaults to today's date. Change if needed.
  - **Voucher User**: automatically filled from this term's own partner (the student),
    shown read-only.

  Click **Apply Promotion Code** in the wizard footer to create one **Promotion Code
  Usage** in Draft status referencing this term, with its own **Allocations** filled
  automatically from the term's own invoice receivable journal item.

## Additional Post-Condition

- The **Promotions** column on the Payment Term line (`promotion_usage_count`)
  recomputes to the number of Promotion Code Usage records referencing that term.
