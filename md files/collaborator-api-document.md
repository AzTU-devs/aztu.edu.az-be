# Collaboration API Documentation

Base URL: `/api/collaboration`

All logo paths returned by the API are relative to the static file server root.
To get the full URL, prepend the server base URL:
`https://<your-domain>/static/collaborations/<filename>`

---

## Language

All `GET` endpoints are language-aware. Pass the language via query param or header:

| Method | Example |
|--------|---------|
| Query param | `?lang=az` or `?lang=en` |
| Header | `Accept-Language: az` |

Defaults to `en` if not provided.

---

## Endpoints

### 1. Get All Collaborations

```
GET /api/collaboration/all
```

**Query Parameters**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `start` | integer | `0` | Offset (start index) |
| `end` | integer | `10` | End index (returns `end - start` items) |
| `lang` | string | `en` | Language code: `az` or `en` |

**Success Response** `200 OK`

```json
{
  "status_code": 200,
  "message": "Collaborations fetched successfully.",
  "total": 5,
  "collaborations": [
    {
      "id": 1,
      "collaboration_id": 482910,
      "name": "MIT University",
      "logo": "static/collaborations/482910.png",
      "website_url": "https://mit.edu",
      "display_order": 1,
      "created_at": "2026-03-15T10:00:00"
    }
  ]
}
```

**Empty Response** `204 No Content`

```json
{
  "status_code": 204,
  "message": "No content."
}
```

---

### 2. Get Single Collaboration

```
GET /api/collaboration/{collaboration_id}
```

**Path Parameters**

| Param | Type | Description |
|-------|------|-------------|
| `collaboration_id` | integer | The unique collaboration ID |

**Query Parameters**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `lang` | string | `en` | Language code: `az` or `en` |

**Success Response** `200 OK`

```json
{
  "status_code": 200,
  "message": "Collaboration fetched successfully.",
  "collaboration": {
    "id": 1,
    "collaboration_id": 482910,
    "name": "MIT University",
    "logo": "static/collaborations/482910.png",
    "website_url": "https://mit.edu",
    "display_order": 1,
    "created_at": "2026-03-15T10:00:00",
    "updated_at": null
  }
}
```

**Not Found Response** `404 Not Found`

```json
{
  "status_code": 404,
  "message": "Collaboration not found."
}
```

---

### 3. Create Collaboration

```
POST /api/collaboration/create
Content-Type: multipart/form-data
```

**Form Fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `logo` | file | yes | University logo image (png, jpg, svg, etc.) |
| `az_name` | string | yes | University name in Azerbaijani |
| `en_name` | string | yes | University name in English |
| `website_url` | string | no | University website URL |

**Example (fetch)**

```js
const formData = new FormData();
formData.append("logo", logoFile);
formData.append("az_name", "MIT Universiteti");
formData.append("en_name", "MIT University");
formData.append("website_url", "https://mit.edu");

const res = await fetch("/api/collaboration/create", {
  method: "POST",
  body: formData,
});
```

**Success Response** `201 Created`

```json
{
  "status_code": 201,
  "message": "Collaboration created successfully."
}
```

---

### 4. Update Collaboration

```
PUT /api/collaboration/{collaboration_id}/update
Content-Type: multipart/form-data
```

**Path Parameters**

| Param | Type | Description |
|-------|------|-------------|
| `collaboration_id` | integer | The unique collaboration ID |

**Form Fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `az_name` | string | yes | University name in Azerbaijani |
| `en_name` | string | yes | University name in English |
| `logo` | file | no | New logo image — omit to keep existing |
| `website_url` | string | no | New website URL — omit to keep existing |

**Example (fetch)**

```js
const formData = new FormData();
formData.append("az_name", "MIT Universiteti (yenilənmiş)");
formData.append("en_name", "MIT University (updated)");
// logo and website_url are optional — only append if changing

const res = await fetch(`/api/collaboration/${collaborationId}/update`, {
  method: "PUT",
  body: formData,
});
```

**Success Response** `200 OK`

```json
{
  "status_code": 200,
  "message": "Collaboration updated successfully."
}
```

**Not Found Response** `404 Not Found`

```json
{
  "status_code": 404,
  "message": "Collaboration not found."
}
```

---

### 5. Reorder Collaborations

```
POST /api/collaboration/reorder
Content-Type: application/json
```

**Request Body**

| Field | Type | Description |
|-------|------|-------------|
| `collaboration_id` | integer | The unique collaboration ID to move |
| `new_order` | integer | The target display position (1-based) |

**Example (fetch)**

```js
const res = await fetch("/api/collaboration/reorder", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    collaboration_id: 482910,
    new_order: 2,
  }),
});
```

**Success Response** `200 OK`

```json
{
  "status_code": 200,
  "message": "Collaboration reordered successfully"
}
```

**No Change Response** `200 OK`

```json
{
  "status_code": 200,
  "message": "No change"
}
```

---

### 6. Delete Collaboration

```
DELETE /api/collaboration/{collaboration_id}/delete
```

**Path Parameters**

| Param | Type | Description |
|-------|------|-------------|
| `collaboration_id` | integer | The unique collaboration ID |

**Example (fetch)**

```js
const res = await fetch(`/api/collaboration/${collaborationId}/delete`, {
  method: "DELETE",
});
```

**Success Response** `200 OK`

```json
{
  "status_code": 200,
  "message": "Collaboration deleted successfully."
}
```

**Not Found Response** `404 Not Found`

```json
{
  "status_code": 404,
  "message": "Collaboration not found."
}
```

---

## Error Response

All endpoints return this shape on server error:

```json
{
  "status_code": 500,
  "error": "error details"
}
```

---

## Notes

- `display_order` starts at `1`. Newly created entries are always placed first (order `1`); all existing entries shift down.
- `logo` paths are relative — prepend your domain to build the full image URL.
- `website_url` may be `null` if not provided.
- `collaboration_id` is a randomly generated 6-digit integer — use this (not `id`) for all operations.
