# Header Menu API — Admin Dashboard Integration Guide

## Overview

The header menu is a **3-level tree**:

```
MenuHeader  (main navigation title shown in the top bar)
 └── MenuHeaderItem  (first-level dropdown row)
      └── MenuHeaderSubItem  (second-level leaf row)
```

### Key rules

| Level | `has_subitems` | `direct_url` | `base_path` |
|-------|----------------|-------------|-------------|
| `MenuHeader` | boolean | manual override | prefix for auto-url |
| `MenuHeaderItem` | boolean | manual override | n/a |
| `MenuHeaderSubItem` | always leaf | manual override | n/a |

- **Auto-generated URLs:** If `has_subitems` is `false` (or it's a `SubItem`) and no `direct_url` is provided, the backend generates a URL:
  - Header: `/{lang}/{base_path}/{header_slug}`
  - Item: `/{lang}/{base_path}/{header_slug}/{item_slug}`
  - SubItem: `/{lang}/{base_path}/{header_slug}/{item_slug}/{sub_item_slug}`
- **Manual override:** If `direct_url` is provided, it takes precedence over the auto-generated URL.
- **Slugs are auto-generated** from the `title_az` / `title_en` fields. Never send a slug manually.

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
| `lang` | `az` \| `en` | Language for titles and slugs |

**Response `200`**

The `direct_url` in the response will already be populated (either manual override or auto-generated).

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
| `title_az` | string | yes | Azerbaijani title |
| `title_en` | string | yes | English title |
| `display_order` | integer | yes | Sort position |
| `has_subitems` | boolean | no | Default: `true`. If `false`, this is a leaf node. |
| `base_path_az` | string | no | e.g. `"about"` → URL becomes `/az/about/rector` |
| `base_path_en` | string | no | e.g. `"about-us"` → URL becomes `/en/about-us/rector` |
| `direct_url` | string | no | Manual override URL |
| `image` | file | no | Optional image for mega-menu |

---

## 3. Update a main header title

```
PUT /api/menu/header/{header_id}
Content-Type: multipart/form-data
Authorization: Bearer <token>
```

**Form fields** — all optional

| Field | Type | Notes |
|-------|------|-------|
| `title_az` / `title_en` | string | Updates title and slug |
| `base_path_az` / `base_path_en` | string | Updates URL prefix |
| `has_subitems` | boolean | |
| `direct_url` | string | `""` to clear (revert to auto-url) |
| `is_active` | boolean | |
| `image` | file | |

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
  "has_subitems": true,
  "direct_url": null
}
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
  "display_order": 1,
  "direct_url": null
}
```

> Leaf nodes (SubItems) do not need a URL if you want them to be auto-generated as `/{lang}/{base_path}/{header_slug}/{item_slug}/{sub_item_slug}`.
