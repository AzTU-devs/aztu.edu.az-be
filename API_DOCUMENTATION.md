# AzTU University — API Documentation

> **For Frontend Developers**
> Base URL: `https://aztu.edu.az/api` (production) · `http://localhost:8000/api` (local)

---

## Table of Contents

1. [General](#general)
2. [Language](#language)
3. [News Categories](#news-categories)
4. [News](#news)
5. [Announcements](#announcements)
6. [Sliders](#sliders)
7. [Projects](#projects)
8. [Faculties](#faculties)
9. [Cafedras (Departments)](#cafedras-departments)
10. [Error Responses](#error-responses)

---

## General

### Health Check

```
GET /health
```

**Response**
```json
{ "status": "ok" }
```

---

## Language

All `GET` endpoints support multilingual responses via:

| Method | Example | Priority |
|--------|---------|----------|
| Query param | `?lang=az` | Highest |
| HTTP header | `Accept-Language: az` | Fallback |
| Default | `en` | Lowest |

**Supported values:** `en` (English), `az` (Azerbaijani)

---

## News Categories

### Get All Categories

```
GET /news-category/all
```

**Query Parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `lang_code` | string | No | Language (`en` / `az`) |

**Response**
```json
[
  {
    "category_id": 1,
    "title": "University News"
  }
]
```

---

### Create Category *(Admin)*

```
POST /news-category/create
Content-Type: multipart/form-data
```

**Form Fields**

| Name | Type | Required |
|------|------|----------|
| `az_title` | string | Yes |
| `en_title` | string | Yes |

**Response** — Created category object.

---

## News

### Get Public News

```
GET /news/public/all
```

**Query Parameters**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `category_id` | integer | Yes | — | Filter by category |
| `start` | integer | No | `0` | Pagination offset |
| `end` | integer | No | `10` | Pagination limit |
| `lang` | string | No | `en` | Language |

**Response**
```json
[
  {
    "news_id": 123456,
    "category_id": 1,
    "is_active": true,
    "display_order": 1,
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": null,
    "cover_image": "static/news/123456.jpg",
    "title": "University announces new programs",
    "html_content": "<p>...</p>"
  }
]
```

---

### Get All News *(Admin)*

```
GET /news/admin/all
```

Same query parameters as `GET /news/public/all`. Returns all news including inactive items.

---

### Get News by ID

```
GET /news/{news_id}
```

**Path Parameters**

| Name | Type | Required |
|------|------|----------|
| `news_id` | integer | Yes |

**Response** — Single news object (same structure as list item, includes gallery).

---

### Get News Gallery

```
GET /news/gallery
```

**Query Parameters**

| Name | Type | Required |
|------|------|----------|
| `news_id` | integer | Yes |

**Response**
```json
[
  {
    "id": 1,
    "news_id": 123456,
    "image": "static/news/123456-gallery-1.jpg",
    "is_cover": false
  }
]
```

---

### Create News *(Admin)*

```
POST /news/create
Content-Type: multipart/form-data
```

**Form Fields**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `az_title` | string | Yes | Azerbaijani title |
| `en_title` | string | Yes | English title |
| `az_html_content` | string | Yes | Azerbaijani body (HTML) |
| `en_html_content` | string | Yes | English body (HTML) |
| `cover_image` | file | Yes | Cover image |
| `gallery_images` | file[] | No | Additional images |
| `category_id` | integer | Yes | Category ID |

**Response** — Created news object.

---

### Activate News *(Admin)*

```
POST /news/activate?news_id={news_id}
```

### Deactivate News *(Admin)*

```
POST /news/deactivate?news_id={news_id}
```

### Reorder News *(Admin)*

```
POST /news/reorder
Content-Type: application/json
```

```json
{
  "news_id": 123456,
  "new_order": 3
}
```

### Delete News *(Admin)*

```
DELETE /news/{news_id}/delete
```

---

## Announcements

### Get Public Announcements

```
GET /announcement/public/all
```

**Query Parameters**

| Name | Type | Required | Default |
|------|------|----------|---------|
| `start` | integer | No | `0` |
| `end` | integer | No | `4` |
| `lang` | string | No | `en` |

**Response**
```json
[
  {
    "announcement_id": 168384,
    "is_active": true,
    "display_order": 1,
    "created_at": "2025-01-10T08:00:00Z",
    "updated_at": null,
    "image": "static/announcements/168384.webp",
    "title": "Admission period open",
    "html_content": "<p>...</p>"
  }
]
```

---

### Get All Announcements *(Admin)*

```
GET /announcement/admin/all
```

Same parameters as public endpoint. Returns all announcements including inactive.

---

### Get Announcement by ID

```
GET /announcement/{announcement_id}
```

**Query Parameters**

| Name | Type | Required |
|------|------|----------|
| `lang_code` | string | No |

---

### Create Announcement *(Admin)*

```
POST /announcement/create
Content-Type: multipart/form-data
```

**Form Fields**

| Name | Type | Required |
|------|------|----------|
| `image` | file | Yes |
| `az_title` | string | Yes |
| `az_html_content` | string | Yes |
| `en_title` | string | Yes |
| `en_html_content` | string | Yes |

---

### Activate / Deactivate *(Admin)*

```
POST /announcement/activate?announcement_id={id}
POST /announcement/deactivate?announcement_id={id}
```

### Reorder *(Admin)*

```
POST /announcement/reorder
Content-Type: application/json
```

```json
{
  "announcement_id": 168384,
  "new_order": 2
}
```

---

## Sliders

### Get All Sliders

```
GET /slider/all
```

**Query Parameters**

| Name | Type | Required | Default |
|------|------|----------|---------|
| `start` | integer | No | `0` |
| `end` | integer | No | `4` |
| `lang` | string | No | `en` |

**Response**
```json
[
  {
    "slider_id": 100001,
    "url": "https://aztu.edu.az/programs",
    "image": "static/sliders/100001.jpg",
    "display_order": 1,
    "is_active": true,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": null,
    "desc": "Explore our programs"
  }
]
```

---

### Get Slider by ID

```
GET /slider/{slider_id}
```

| Parameter | Type | Location |
|-----------|------|----------|
| `slider_id` | integer | Path |
| `lang` | string | Query (optional) |

---

### Create Slider *(Admin)*

```
POST /slider/create
Content-Type: multipart/form-data
```

| Name | Type | Required |
|------|------|----------|
| `image` | file | Yes |
| `az_desc` | string | Yes |
| `en_desc` | string | Yes |
| `url` | string | Yes |

---

### Edit Slider *(Admin)*

```
PUT /slider/{slider_id}/edit
Content-Type: multipart/form-data
```

All fields optional:

| Name | Type |
|------|------|
| `url` | string |
| `az_desc` | string |
| `en_desc` | string |
| `image` | file |

---

### Reorder *(Admin)*

```
POST /slider/reorder
Content-Type: application/json
```

```json
{
  "slider_id": 100001,
  "new_order": 1
}
```

### Delete Slider *(Admin)*

```
DELETE /slider/{slider_id}/delete
```

---

## Projects

### Get All Projects

```
GET /project/all
```

**Query Parameters**

| Name | Type | Required | Default |
|------|------|----------|---------|
| `start` | integer | No | `0` |
| `end` | integer | No | `4` |
| `lang` | string | No | `en` |

**Response**
```json
[
  {
    "project_id": "100001",
    "bg_image": "static/projects/100001.jpg",
    "display_order": 1,
    "is_active": true,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": null,
    "title": "Smart Campus Initiative",
    "desc": "Short description...",
    "html_content": "<p>Full content...</p>"
  }
]
```

---

### Get Project by ID

```
GET /project/{project_id}
```

| Parameter | Type | Location |
|-----------|------|----------|
| `project_id` | string | Path |
| `lang` | string | Query (optional) |

---

### Create Project *(Admin)*

```
POST /project/create
Content-Type: multipart/form-data
```

| Name | Type | Required |
|------|------|----------|
| `bg_image` | file | Yes |
| `az_title` | string | Yes |
| `az_desc` | string | Yes |
| `az_content_html` | string | Yes |
| `en_title` | string | Yes |
| `en_desc` | string | Yes |
| `en_content_html` | string | Yes |

---

### Reorder *(Admin)*

```
POST /project/reorder
Content-Type: application/json
```

```json
{
  "project_id": "100001",
  "new_order": 2
}
```

### Delete Project *(Admin)*

```
DELETE /project/{project_id}/delete
```

---

## Faculties

### Get Public Faculties

```
GET /faculty/public/all
```

**Query Parameters**

| Name | Type | Required | Default |
|------|------|----------|---------|
| `start` | integer | No | `0` |
| `end` | integer | No | `10` |
| `lang` | string | No | `en` |

**Response**
```json
[
  {
    "faculty_code": "FAC-ENG",
    "faculty_name": "Faculty of Engineering"
  }
]
```

---

### Get All Faculties *(Admin)*

```
GET /faculty/admin/all
```

Same parameters as public endpoint.

---

### Get Faculty by Code

```
GET /faculty/{faculty_code}
```

| Parameter | Type | Location |
|-----------|------|----------|
| `faculty_code` | string | Path |
| `lang_code` | string | Query (optional) |

---

### Create Faculty *(Admin)*

```
POST /faculty/create
Content-Type: multipart/form-data
```

| Name | Type | Required |
|------|------|----------|
| `az_name` | string | Yes |
| `en_name` | string | Yes |

---

### Update Faculty *(Admin)*

```
PUT /faculty/{faculty_code}
Content-Type: multipart/form-data
```

| Name | Type | Required |
|------|------|----------|
| `az_name` | string | No |
| `en_name` | string | No |

### Delete Faculty *(Admin)*

```
DELETE /faculty/{faculty_code}
```

---

## Cafedras (Departments)

### Get Public Cafedras

```
GET /cafedra/public/all
```

**Query Parameters**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `start` | integer | No | `0` | Pagination offset |
| `end` | integer | No | `10` | Pagination limit |
| `faculty_code` | string | No | — | Filter by faculty |
| `lang` | string | No | `en` | Language |

**Response**
```json
[
  {
    "cafedra_code": "CAF-CS-01",
    "faculty_code": "FAC-ENG",
    "cafedra_name": "Computer Science Department"
  }
]
```

---

### Get All Cafedras *(Admin)*

```
GET /cafedra/admin/all
```

Same parameters as public endpoint.

---

### Get Cafedra by Code

```
GET /cafedra/{cafedra_code}
```

| Parameter | Type | Location |
|-----------|------|----------|
| `cafedra_code` | string | Path |
| `lang_code` | string | Query (optional) |

---

### Create Cafedra *(Admin)*

```
POST /cafedra/create
Content-Type: multipart/form-data
```

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `faculty_code` | string | Yes | Parent faculty |
| `az_name` | string | Yes | Azerbaijani name |
| `en_name` | string | Yes | English name |

---

### Update Cafedra *(Admin)*

```
PUT /cafedra/{cafedra_code}
Content-Type: multipart/form-data
```

| Name | Type | Required |
|------|------|----------|
| `az_name` | string | No |
| `en_name` | string | No |

### Delete Cafedra *(Admin)*

```
DELETE /cafedra/{cafedra_code}
```

---

## Error Responses

All errors return JSON in this format:

```json
{
  "status_code": 404,
  "message": "Item not found"
}
```

| Status Code | Meaning |
|-------------|---------|
| `400` | Bad Request — invalid input |
| `404` | Not Found |
| `422` | Unprocessable Entity — validation error (e.g. invalid `lang`) |
| `500` | Internal Server Error |

---

## Static Files

Uploaded files are served at:

```
GET /static/{entity_type}/{filename}
```

**Examples:**
- `static/news/123456.png` — news cover image
- `static/news/123456-gallery-1.jpeg` — news gallery image
- `static/announcements/168384.webp` — announcement image
- `static/sliders/100001.jpg` — slider image
- `static/projects/100001.jpg` — project background image

---

## Notes

- **No authentication** is required for any endpoint currently.
- Endpoints marked *(Admin)* are intended for the admin panel only.
- All `created_at` / `updated_at` timestamps are in **ISO 8601 UTC** format.
- Pagination uses `start` (offset) and `end` (limit), not page numbers.
- `news_id`, `announcement_id`, and `slider_id` are 6-digit randomly generated integers (100000–999999).
- `faculty_code` and `cafedra_code` are human-readable string slugs (e.g. `FAC-ENG`, `CAF-CS-01`).
