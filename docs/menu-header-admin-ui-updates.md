# Admin Dashboard: Menu Header UI & API Integration

This guide provides the technical details for integrating the 3-level hierarchical menu system into the Admin Dashboard.

## 1. Top-Level Headers (MenuHeader)

**UI Component:** A form with a "Has Sub-items" checkbox and an optional "Direct URL" for external links.

### **POST** `/api/menu/header/`
**Content-Type:** `multipart/form-data`

| Field | Type | Required | Description |
|---|---|---|---|
| `title_az` | string | Yes | Azerbaijani title |
| `title_en` | string | Yes | English title |
| `display_order` | integer | Yes | Sort order (ascending) |
| `has_subitems` | boolean | No | Default `true`. If `false`, this is a leaf node. |
| `direct_url` | string | No | Manual override (e.g. `https://google.com`). |
| `image` | file | No | Image for the mega-menu dropdown. |

### **PUT** `/api/menu/header/{header_id}`
**Content-Type:** `multipart/form-data`
*All fields are optional.*

---

## 2. First-Level Dropdown Items (MenuHeaderItem)

**UI Component:** A nested form under a Header. Includes a "Has Sub-items" checkbox.

### **POST** `/api/menu/header/item`
**Content-Type:** `application/json`

```json
{
  "header_id": 1,
  "title_az": "Haqqımızda",
  "title_en": "About Us",
  "display_order": 1,
  "has_subitems": true,
  "direct_url": null
}
```

### **PUT** `/api/menu/header/item/{item_id}`
**Content-Type:** `application/json`
*Fields are optional.*

---

## 3. Second-Level Leaf Items (MenuHeaderSubItem)

**UI Component:** A nested list under a MenuHeaderItem.

### **POST** `/api/menu/header/sub-item`
**Content-Type:** `application/json`

```json
{
  "item_id": 10,
  "title_az": "Rektor",
  "title_en": "Rector",
  "display_order": 1,
  "direct_url": null
}
```

### **PUT** `/api/menu/header/sub-item/{sub_item_id}`
**Content-Type:** `application/json`

---

## 4. Deletion Endpoints

- **Delete Header:** `DELETE /api/menu/header/{header_id}` (Cascades to all children)
- **Delete Item:** `DELETE /api/menu/header/item/{item_id}` (Cascades to all sub-items)
- **Delete Sub-item:** `DELETE /api/menu/header/sub-item/{sub_item_id}`

---

## Recursive URL Logic Summary

The backend automatically calculates the `direct_url` based on the hierarchy of **slugs** (URL-safe titles):

1. **Header (Leaf):** `/{lang}/{header_slug}`
2. **Item (Leaf):** `/{lang}/{header_slug}/{item_slug}`
3. **SubItem:** `/{lang}/{header_slug}/{item_slug}/{sub_item_slug}`

**External Links:** If a user enters a value in the `direct_url` field (e.g., `https://example.com`), that value is returned exactly as entered, bypassing the auto-generation logic.
