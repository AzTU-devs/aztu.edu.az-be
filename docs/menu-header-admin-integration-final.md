# Admin Integration: Hierarchical Menu with Recursive Slugs

This document explains the "Checkbox Logic" and API integration for the 3-level menu system.

## 1. The "has_subitems" Gatekeeper
Every level except the last one (SubItem) has a `has_subitems` boolean.
- **If TRUE:** The item acts as a container. It will NOT be a clickable link in the frontend (it just opens a sub-menu).
- **If FALSE:** The item is a "Leaf". The backend will generate a recursive URL for it (or use a manual override). You CANNOT add children to it.

---

## 2. API Endpoints Reference

### Level 1: Main Header (Top Bar)
**Endpoint:** `POST /api/menu/header/` (Multipart/Form-Data)

| Field | Value for Category | Value for Direct Link |
|---|---|---|
| `has_subitems` | `true` | `false` |
| `direct_url` | (leave empty) | (empty for auto-slug or enter URL) |

### Level 2: Dropdown Item (Column Header)
**Endpoint:** `POST /api/menu/header/item` (JSON)

| Field | Value for Category (has Sub-items) | Value for Direct Link (Leaf) |
|---|---|---|
| `has_subitems` | `true` | `false` |
| `direct_url` | `null` | `null` (auto-slug) or `"https://..."` |

> **IMPORTANT:** If you try to `POST /api/menu/header/sub-item` to an item that has `has_subitems: false`, the backend will return `400 Bad Request`.

---

## 3. Recursive URL Logic (Backend Automatic)

The frontend **never** sends slugs or constructs paths. The backend calculates the `direct_url` field in the `GET` response as follows:

1. **Header (has_subitems: false):** `/{lang}/{header_slug}`
2. **Item (has_subitems: false):** `/{lang}/{header_slug}/{item_slug}`
3. **SubItem (Always a leaf):** `/{lang}/{header_slug}/{item_slug}/{sub_item_slug}`

---

## 4. Frontend Implementation Checklist

1. **The Checkbox:** When the user checks "Has Sub-items", your UI should:
   - Hide the "Direct URL" input field.
   - Send `has_subitems: true` to the API.
2. **Adding Children:**
   - Only allow adding a "Sub-item" if the parent Item has `has_subitems: true`.
3. **External Links:**
   - For links to external sites (e.g., `https://google.com`), set `has_subitems: false` and enter the URL in the `direct_url` field.
4. **Boolean Values in Forms:** 
   - Since Level 1 uses `multipart/form-data`, ensure the `has_subitems` boolean is sent correctly (usually as a string `"true"` or `"false"`).

---

## 5. Swagger Documentation
You can find the interactive API documentation at:
`http://<your-domain>/docs`

Look for the **Menu Header Admin** and **Menu Header** tags.
