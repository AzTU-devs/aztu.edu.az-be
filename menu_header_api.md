# Menu Header API

**Base URL:** `/api/v1/menu`

---

## GET `/header`

Returns the full header menu structure.

**Auth:** Public

**Query Params:**

| Param | Type | Description |
|---|---|---|
| `lang` | `string` | `az` or `en` (default: `az`) |

**Response `200`:**

```json
{
  "status_code": 200,
  "data": {
    "sections": [
      {
        "id": 1,
        "key": "about",
        "label": "Haqqımızda",
        "base_path": "/about",
        "image_url": "https://aztu.edu.az/static/menu/headers/abc123.png",
        "direct_url": null,
        "items": [
          {
            "id": 10,
            "title": "Rektorat",
            "item_type": "subheader",
            "slug": null,
            "sub_items": [
              {
                "id": 101,
                "title": "Rektor",
                "slug": "/about/rector"
              }
            ]
          },
          {
            "id": 11,
            "title": "Tarix",
            "item_type": "link",
            "slug": "/about/history",
            "sub_items": []
          }
        ]
      },
      {
        "id": 2,
        "key": "admissions",
        "label": "Qəbul",
        "base_path": "/admissions",
        "image_url": "https://aztu.edu.az/static/menu/headers/def456.png",
        "direct_url": "https://tqdk.gov.az",
        "items": []
      }
    ]
  }
}
```

**Notes:**
- If `direct_url` is set, `items` will always be empty — the section links directly to that URL
- `item_type: "subheader"` — acts as a group heading, has `sub_items`, `slug` is `null`
- `item_type: "link"` — a direct link, `slug` is the endpoint, `sub_items` is always `[]`

---

## POST `/header/section`

Creates a new header section (top-level menu title).

**Auth:** Admin required

**Content-Type:** `multipart/form-data`

**Form Fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `section_key` | `string` | Yes | Unique key (e.g. `"about"`) |
| `display_order` | `integer` | Yes | Sort order |
| `label_az` | `string` | Yes | Azerbaijani label |
| `label_en` | `string` | Yes | English label |
| `base_path_az` | `string` | Yes | Base path (AZ) |
| `base_path_en` | `string` | Yes | Base path (EN) |
| `image` | `file` | Yes | Image file (jpg/png/webp/gif) |
| `direct_url` | `string` | No | If set, section links here — no items can be added |

**Response `201`:**
```json
{
  "status_code": 201,
  "message": "Header section created.",
  "id": 1
}
```

**Response `409`** — section_key already exists

---

## PUT `/header/section/{section_id}`

Updates an existing header section.

**Auth:** Admin required

**Content-Type:** `multipart/form-data`

All fields are optional — only send what you want to change.

| Field | Type | Description |
|---|---|---|
| `display_order` | `integer` | New sort order |
| `label_az` | `string` | Updated AZ label |
| `label_en` | `string` | Updated EN label |
| `base_path_az` | `string` | Updated AZ base path |
| `base_path_en` | `string` | Updated EN base path |
| `image` | `file` | New image — replaces old file |
| `direct_url` | `string` | Set URL to add/change; send `""` (empty string) to clear it |

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "Header section updated."
}
```

**Response `404`** — section not found

---

## DELETE `/header/section/{section_id}`

Deletes a section and all its items/sub-items (cascade).

**Auth:** Admin required

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "Header section deleted."
}
```

---

## POST `/header/item`

Adds an item under a section.

**Auth:** Admin required

**Content-Type:** `application/json`

```json
{
  "section_id": 1,
  "item_type": "link",
  "slug": "/about/history",
  "display_order": 1,
  "title": {
    "az": "Tarix",
    "en": "History"
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `section_id` | `integer` | Yes | Parent section ID |
| `item_type` | `string` | No | `"link"` (default) or `"subheader"` |
| `slug` | `string` | Required if `item_type` is `"link"` | Endpoint URL |
| `display_order` | `integer` | Yes | Sort order |
| `title` | `object` | Yes | `{ "az": "...", "en": "..." }` |

**Response `201`:**
```json
{
  "status_code": 201,
  "message": "Header item created.",
  "id": 10
}
```

**Response `400`** — section has a `direct_url` set, or `link` type missing `slug`

**Response `404`** — section not found

---

## PUT `/header/item/{item_id}`

Updates an item.

**Auth:** Admin required

**Content-Type:** `application/json`

All fields optional:

```json
{
  "item_type": "subheader",
  "slug": null,
  "display_order": 2,
  "title": {
    "az": "Rektorat",
    "en": "Rectorate"
  }
}
```

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "Header item updated."
}
```

**Response `404`** — item not found

---

## DELETE `/header/item/{item_id}`

Deletes an item and all its sub-items (cascade).

**Auth:** Admin required

**Response `200`:**
```json
{ "status_code": 200, "message": "Header item deleted." }
```

---

## POST `/header/sub-item`

Adds a sub-item under a `subheader`-type item. Sub-items are leaf nodes and always require a `slug` (endpoint).

**Auth:** Admin required

**Content-Type:** `application/json`

```json
{
  "item_id": 10,
  "slug": "/about/rector",
  "display_order": 1,
  "title": {
    "az": "Rektor",
    "en": "Rector"
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `item_id` | `integer` | Yes | Parent item ID (must be `subheader` type) |
| `slug` | `string` | Yes | Endpoint URL |
| `display_order` | `integer` | Yes | Sort order |
| `title` | `object` | Yes | `{ "az": "...", "en": "..." }` |

**Response `201`:**
```json
{
  "status_code": 201,
  "message": "Header sub-item created.",
  "id": 101
}
```

**Response `400`** — parent item has `item_type: "link"` (link items cannot have sub-items)

**Response `404`** — item not found

---

## PUT `/header/sub-item/{sub_item_id}`

Updates a sub-item.

**Auth:** Admin required

**Content-Type:** `application/json`

All fields optional:

```json
{
  "slug": "/about/rector-new",
  "display_order": 2,
  "title": {
    "az": "Rektor",
    "en": "Rector"
  }
}
```

**Response `200`:**
```json
{ "status_code": 200, "message": "Header sub-item updated." }
```

**Response `404`** — sub-item not found

---

## DELETE `/header/sub-item/{sub_item_id}`

**Auth:** Admin required

**Response `200`:**
```json
{ "status_code": 200, "message": "Header sub-item deleted." }
```

---

## Section / Item structure rules

```
MenuHeaderSection
├── direct_url is set  →  no items allowed, section is a direct link
└── direct_url is null →  items allowed
    ├── item_type: "link"      →  has slug (endpoint), no sub-items allowed
    └── item_type: "subheader" →  no slug, has sub-items
        └── MenuHeaderSubItem  →  always has slug (endpoint, required)
```
