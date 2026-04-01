# Header Menu API — Admin Dashboard Integration Guide

## Overview

The header menu is a **3-level tree**:

```
MenuHeader  (main navigation title shown in the top bar)
 └── MenuHeaderItem  (first-level dropdown row)
      └── MenuHeaderSubItem  (second-level leaf row, always has a URL)
```

### Key rules

| Level | Has image? | `direct_url` | Can have children? |
|-------|-----------|-------------|-------------------|
| `MenuHeader` | optional | optional | yes — unless `direct_url` is set |
| `MenuHeaderItem` | no | optional | yes — unless `direct_url` is set |
| `MenuHeaderSubItem` | no | **required** | never (leaf) |

- **Slugs are auto-generated** from the `title_az` / `title_en` fields on every create and update. Never send a slug manually.
- All write endpoints require an `Authorization: Bearer <token>` header (admin only).
- The public GET endpoint requires no auth.

---

## Base URL

```
/api/menu/header
```

---

## 1. GET — Fetch full header tree (public)

```
GET /api/menu/header
```

**Query params**

| Param | Type | Description |
|-------|------|-------------|
| `lang` | `az` \| `en` | Language for titles and slugs (detected from `Accept-Language` header by default) |

**Response `200`**

```json
{
  "status_code": 200,
  "data": [
    {
      "id": 1,
      "image_url": "https://aztu.edu.az/static/uploads/menu/headers/abc.png",
      "title": "Universitet",
      "slug": "universitet",
      "direct_url": null,
      "items": [
        {
          "id": 10,
          "title": "Haqqımızda",
          "slug": "haqqimizda",
          "direct_url": null,
          "sub_items": [
            {
              "id": 100,
              "title": "Rektor",
              "slug": "rektor",
              "direct_url": "/az/universitet/haqqimizda/rektor"
            }
          ]
        },
        {
          "id": 11,
          "title": "Əlaqə",
          "slug": "elaqe",
          "direct_url": "/az/universitet/elaqe",
          "sub_items": []
        }
      ]
    }
  ]
}
```

> When a `MenuHeader` has `direct_url` set, `items` will be `[]`.  
> When a `MenuHeaderItem` has `direct_url` set, `sub_items` will be `[]`.

---

## 2. Create a main header title

```
POST /api/menu/header
Content-Type: multipart/form-data
Authorization: Bearer <token>
```

**Form fields**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `title_az` | string | yes | Azerbaijani title — slug auto-generated |
| `title_en` | string | yes | English title — slug auto-generated |
| `display_order` | integer | yes | Sort position (ascending) |
| `direct_url` | string | no | If set, no items can be added later |
| `image` | file | no | JPEG/PNG/WebP image |

**Response `201`**

```json
{ "status_code": 201, "message": "Header created.", "id": 5 }
```

**Example (fetch)**

```js
const form = new FormData();
form.append("title_az", "Universitet");
form.append("title_en", "University");
form.append("display_order", "1");
form.append("image", imageFile);   // optional

const res = await fetch("/api/menu/header", {
  method: "POST",
  headers: { Authorization: `Bearer ${token}` },
  body: form,
});
```

---

## 3. Update a main header title

```
PUT /api/menu/header/{header_id}
Content-Type: multipart/form-data
Authorization: Bearer <token>
```

**Form fields** — all optional; omit any field you do not want to change

| Field | Type | Notes |
|-------|------|-------|
| `title_az` | string | Updating regenerates `slug_az` |
| `title_en` | string | Updating regenerates `slug_en` |
| `display_order` | integer | |
| `direct_url` | string | Send `""` (empty string) to clear it |
| `is_active` | boolean | `true` / `false` |
| `image` | file | Replaces old image; old file is deleted |

**Response `200`**

```json
{ "status_code": 200, "message": "Header updated." }
```

---

## 4. Delete a main header title

```
DELETE /api/menu/header/{header_id}
Authorization: Bearer <token>
```

Cascades — all items and sub-items under this header are deleted automatically. The image file is also deleted from disk.

**Response `200`**

```json
{ "status_code": 200, "message": "Header deleted." }
```

---

## 5. Add a first-level item

```
POST /api/menu/header/item
Content-Type: application/json
Authorization: Bearer <token>
```

**Body**

```json
{
  "header_id": 5,
  "title_az": "Haqqımızda",
  "title_en": "About Us",
  "display_order": 1,
  "direct_url": null
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `header_id` | integer | yes | ID of the parent `MenuHeader` |
| `title_az` | string | yes | |
| `title_en` | string | yes | |
| `display_order` | integer | yes | |
| `direct_url` | string | no | Set this **only** if this item is a leaf (no sub-items). Once set, sub-items cannot be added. |

> **Error `400`** — if the parent `MenuHeader` already has a `direct_url`, you cannot add items to it.

**Response `201`**

```json
{ "status_code": 201, "message": "Header item created.", "id": 42 }
```

---

## 6. Update a first-level item

```
PUT /api/menu/header/item/{item_id}
Content-Type: application/json
Authorization: Bearer <token>
```

**Body** — all fields optional

```json
{
  "title_az": "Haqqımızda",
  "title_en": "About Us",
  "display_order": 2,
  "direct_url": "",
  "is_active": true
}
```

| Field | Type | Notes |
|-------|------|-------|
| `title_az` | string | Regenerates `slug_az` |
| `title_en` | string | Regenerates `slug_en` |
| `display_order` | integer | |
| `direct_url` | string | `""` to clear, non-empty to set |
| `is_active` | boolean | |

**Response `200`**

```json
{ "status_code": 200, "message": "Header item updated." }
```

---

## 7. Delete a first-level item

```
DELETE /api/menu/header/item/{item_id}
Authorization: Bearer <token>
```

Cascades — all sub-items under this item are deleted automatically.

**Response `200`**

```json
{ "status_code": 200, "message": "Header item deleted." }
```

---

## 8. Add a second-level sub-item (leaf)

```
POST /api/menu/header/sub-item
Content-Type: application/json
Authorization: Bearer <token>
```

**Body**

```json
{
  "item_id": 42,
  "title_az": "Rektor",
  "title_en": "Rector",
  "direct_url": "/az/universitet/haqqimizda/rektor",
  "display_order": 1
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `item_id` | integer | yes | ID of the parent `MenuHeaderItem` |
| `title_az` | string | yes | |
| `title_en` | string | yes | |
| `direct_url` | string | yes | Leaf nodes always require a URL |
| `display_order` | integer | yes | |

> **Error `400`** — if the parent `MenuHeaderItem` already has a `direct_url`, you cannot add sub-items to it.

**Response `201`**

```json
{ "status_code": 201, "message": "Header sub-item created.", "id": 201 }
```

---

## 9. Update a second-level sub-item

```
PUT /api/menu/header/sub-item/{sub_item_id}
Content-Type: application/json
Authorization: Bearer <token>
```

**Body** — all fields optional

```json
{
  "title_az": "Rektor",
  "title_en": "Rector",
  "direct_url": "/az/universitet/haqqimizda/rektor",
  "display_order": 1,
  "is_active": true
}
```

**Response `200`**

```json
{ "status_code": 200, "message": "Header sub-item updated." }
```

---

## 10. Delete a second-level sub-item

```
DELETE /api/menu/header/sub-item/{sub_item_id}
Authorization: Bearer <token>
```

**Response `200`**

```json
{ "status_code": 200, "message": "Header sub-item deleted." }
```

---

## Error responses

| `status_code` | Meaning |
|-------------|---------|
| `400` | Bad request — e.g. adding items to a node that already has `direct_url` |
| `401` | Missing or invalid token |
| `404` | Resource not found |
| `500` | Internal server error |

---

## Admin dashboard workflow

### Creating a new top-level navigation entry

```
1. POST /api/menu/header          → gets back { id: N }
2. POST /api/menu/header/item     { header_id: N, ... }   × as many items as needed
3. POST /api/menu/header/sub-item { item_id: M, ... }     × as many sub-items as needed
```

### Typical form layout

```
┌─ Create / Edit Header ───────────────────────────────────────┐
│  Title AZ  [___________________________]  (slug shown below) │
│  Title EN  [___________________________]  (slug shown below) │
│  Image     [Browse...]                                        │
│  Direct URL [___________________________] (leave empty if    │
│                                            this has a menu)  │
│  Display order [__]                                          │
└──────────────────────────────────────────────────────────────┘

┌─ Items (added after the header is saved) ────────────────────┐
│  + Add item                                                  │
│  ┌─ Item ─────────────────────────────────────────────────┐  │
│  │ Title AZ [__________]  Title EN [__________]           │  │
│  │ Direct URL [__________] (leave empty for sub-items)    │  │
│  │ Order [__]                                             │  │
│  │ + Add sub-item                                         │  │
│  │  ┌─ Sub-item ───────────────────────────────────────┐  │  │
│  │  │ Title AZ [__________]  Title EN [__________]     │  │  │
│  │  │ Direct URL [__________] (required)               │  │  │
│  │  │ Order [__]                                       │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Slug preview

Since slugs are auto-generated from the title you can show a live preview in the form by replicating the server logic on the client:

```js
function makeSlug(title) {
  const az = { ə:'e',Ə:'E',ü:'u',Ü:'U',ö:'o',Ö:'O',ğ:'g',Ğ:'G',ı:'i',İ:'I',ç:'c',Ç:'C',ş:'s',Ş:'S' };
  return title
    .replace(/[əƏüÜöÖğĞıİçÇşŞ]/g, ch => az[ch] ?? ch)
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/[\s_]+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');
}
```

---

## Migration note

The previous API used a `MenuHeaderSection` (section_key, base_path, label) as the root level with a separate concept of `item_type: "link" | "subheader"`. **All of that is replaced.** The new model:

- No more `section_key` or `base_path` fields
- No more `item_type` flag — a node is a leaf if and only if `direct_url` is set
- Slugs are stored per-language in the translation table and are always derived from the title
- The 4-level old hierarchy (`Section → Item → SubItem → SubSubItem`) is now a clean 3-level tree (`Header → Item → SubItem`)
