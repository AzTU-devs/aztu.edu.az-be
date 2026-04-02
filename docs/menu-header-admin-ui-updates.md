# Admin Dashboard: Menu Header UI Updates

The menu header system now supports **auto-generated recursive URLs** based on slugs.

## 1. Top-Level Header Form (MenuHeader)

**Fields:**
- **Title (AZ/EN):** Used to auto-generate the base slug.
- **Has Sub-items (Checkbox):** 
  - If **Checked**: The header is a category. Sub-items (Items) can be added.
  - If **Unchecked**: The header is a direct link.
- **Direct URL (Optional):** Manual override. Use this for **external links** (e.g., `https://google.com`). If left empty and `has_subitems` is off, the backend generates `/{lang}/{header_slug}`.

---

## 2. First-Level Item Form (MenuHeaderItem)

**Fields:**
- **Title (AZ/EN):** Used to auto-generate the item slug.
- **Has Sub-items (Checkbox):**
  - If **Checked**: This is a column header in the mega-menu. Sub-items can be added.
  - If **Unchecked**: This is a direct link.
- **Direct URL (Optional):** Manual override. If left empty and `has_subitems` is off, the backend generates `/{lang}/{header_slug}/{item_slug}`.

---

## 3. Second-Level Sub-item Form (MenuHeaderSubItem)

**Fields:**
- **Title (AZ/EN):** Used to auto-generate the sub-item slug.
- **Direct URL (Optional):** Manual override. If left empty, the backend generates `/{lang}/{header_slug}/{item_slug}/{sub_item_slug}`.

---

## Example of Auto-generation

If you have:
1. Header: `Universitet` (slug: `universitet`)
2. Item: `Haqqımızda` (slug: `haqqimizda`)
3. Sub-item: `Rektor` (slug: `rektor`)

The Sub-item URL will automatically be: `/az/universitet/haqqimizda/rektor`.
