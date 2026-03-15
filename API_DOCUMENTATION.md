# AzTU University — API Documentation

> **For Frontend / Admin Dashboard Developers**
> Base URL: `https://aztu.edu.az/api` (production) · `http://localhost:8000/api` (local)

---

## Table of Contents

1. [General](#general)
2. [Language](#language)
3. [News Categories](#news-categories)
4. [News](#news)
5. [Announcements](#announcements)
6. [Hero (Video Banner)](#hero-video-banner)
7. [Projects](#projects)
8. [Faculties](#faculties)
9. [Cafedras (Departments)](#cafedras-departments)
10. [Menu — Header](#menu--header)
11. [Menu — Footer](#menu--footer)
12. [Menu — Quick Menu](#menu--quick-menu)
13. [Menu — Social Links](#menu--social-links)
14. [Menu — Contacts](#menu--contacts)
15. [Static Files](#static-files)
16. [Error Responses](#error-responses)

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

> No authentication is required for any endpoint. Endpoints marked **[Admin]** are intended for the admin dashboard only.

---

## Language

All `GET` endpoints support multilingual responses via:

| Method | Example | Priority |
|--------|---------|----------|
| Query param | `?lang=az` | Highest |
| HTTP header | `Accept-Language: az` | Fallback |
| Default | `en` | Lowest |

**Supported values:** `en` (English), `az` (Azerbaijani)

Unsupported values return `422 Unprocessable Entity`.

---

## News Categories

### Get All Categories

```
GET /news-category/all
```

**Query Parameters**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `lang` | string | No | `en` | Response language |

**Response `200`**
```json
{
  "status_code": 200,
  "message": "News categories fetched successfully.",
  "news_categories": [
    {
      "category_id": 123456,
      "title": "University News"
    }
  ]
}
```

---

### Create Category **[Admin]**

```
POST /news-category/create
Content-Type: multipart/form-data
```

**Form Fields**

| Name | Type | Required |
|------|------|----------|
| `az_title` | string | Yes |
| `en_title` | string | Yes |

**Response `201`**
```json
{
  "status_code": 201,
  "message": "News category created successfully."
}
```

**Response `409`** — category title already exists in that language.

---

## News

### Get Public News

```
GET /news/public/all
```

**Query Parameters**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `category_id` | integer | No | — | Filter by category |
| `start` | integer | No | `0` | Pagination offset |
| `end` | integer | No | `10` | Pagination limit |
| `lang` | string | No | `en` | Response language |

**Response `200`**
```json
{
  "status_code": 200,
  "message": "News fetched successfully.",
  "total": 42,
  "news": [
    {
      "news_id": 123456,
      "category_id": 654321,
      "display_order": 1,
      "is_active": true,
      "title": "University announces new programs",
      "html_content": "<p>...</p>"
    }
  ]
}
```

**Response `204`** — no news found.

---

### Get All News **[Admin]**

```
GET /news/admin/all
```

**Query Parameters**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `category_id` | integer | No | — | Filter by category |
| `start` | integer | No | `0` | Pagination offset |
| `end` | integer | No | `10` | Pagination limit |
| `lang` | string | No | `en` | Response language |

Returns all news including inactive items.

**Response `200`**
```json
{
  "status_code": 200,
  "message": "News fetched successfully.",
  "total": 42,
  "news": [
    {
      "news_id": 123456,
      "category_id": 654321,
      "display_order": 1,
      "is_active": false,
      "title": "Draft article",
      "created_at": "2025-01-15T10:00:00"
    }
  ]
}
```

---

### Get News by ID

```
GET /news/{news_id}
```

**Path Parameters**

| Name | Type | Required |
|------|------|----------|
| `news_id` | integer | Yes |

**Response `200`**
```json
{
  "status_code": 200,
  "message": "News details fetched successfully.",
  "news": {
    "news_id": 123456,
    "az_title": "Universitetdə yeni proqramlar",
    "az_html_content": "<p>...</p>",
    "en_title": "University announces new programs",
    "en_html_content": "<p>...</p>",
    "category_id": "University News",
    "cover_image": "static/news/123456.jpg",
    "gallery_images": [
      { "image_id": 1, "image": "static/news/123456-gallery-1.jpg" }
    ]
  }
}
```

> Note: `category_id` field in the detail response contains the category **title**, not the ID.

**Response `404`** — news not found.

---

### Get News Gallery

```
GET /news/gallery?news_id={news_id}
```

**Query Parameters**

| Name | Type | Required |
|------|------|----------|
| `news_id` | integer | Yes |

**Response `200`**
```json
{
  "status_code": 200,
  "message": "News gallery fetched successfully.",
  "gallery_images": [
    {
      "id": 1,
      "news_id": 123456,
      "image": "static/news/123456-gallery-1.jpg"
    }
  ]
}
```

---

### Create News **[Admin]**

```
POST /news/create
Content-Type: multipart/form-data
```

**Form Fields**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `az_title` | string | Yes | Azerbaijani title |
| `en_title` | string | Yes | English title |
| `az_html_content` | string | Yes | Azerbaijani body (HTML string) |
| `en_html_content` | string | Yes | English body (HTML string) |
| `cover_image` | file | Yes | Cover image (JPEG / PNG / WEBP) |
| `gallery_images` | file[] | No | Additional gallery images |
| `category_id` | integer | Yes | ID from `/news-category/all` |

**Response `201`**
```json
{
  "status_code": 201,
  "message": "News created successfully."
}
```

**Response `409`** — a news item with that title already exists.
**Response `404`** — category not found.

---

### Activate News **[Admin]**

```
POST /news/activate?news_id={news_id}
```

**Response `200`**
```json
{ "status_code": 200, "message": "News activated successfully." }
```

---

### Deactivate News **[Admin]**

```
POST /news/deactivate?news_id={news_id}
```

**Response `200`**
```json
{ "status_code": 200, "message": "News deactivated successfully." }
```

---

### Reorder News **[Admin]**

```
POST /news/reorder
Content-Type: application/json
```

**Request Body**
```json
{
  "news_id": 123456,
  "new_order": 3
}
```

**Response `200`**
```json
{ "status_code": 200, "message": "News reordered successfully" }
```

---

### Delete News **[Admin]**

```
DELETE /news/{news_id}/delete
```

Deletes the news item, all translations, all gallery records, and all gallery image files from disk.

**Response `200`**
```json
{ "status_code": 200, "message": "News deleted successfully." }
```

**Response `404`** — news not found.

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

**Response `200`**
```json
{
  "status_code": 200,
  "message": "Announcements fetched successfully.",
  "announcements": [
    {
      "id": 168384,
      "display_order": 1,
      "title": "Admission period open",
      "html_content": "<p>...</p>",
      "is_active": true,
      "created_at": "2025-01-10T08:00:00"
    }
  ]
}
```

---

### Get All Announcements **[Admin]**

```
GET /announcement/admin/all
```

Same parameters as public endpoint. Returns all announcements including inactive items.

**Response `200`**
```json
{
  "status_code": 200,
  "message": "Announcements fetched successfully.",
  "total": 12,
  "announcements": [
    {
      "announcement_id": 168384,
      "display_order": 1,
      "title": "Admission period open",
      "html_content": "<p>...</p>",
      "is_active": false,
      "created_at": "2025-01-10T08:00:00"
    }
  ]
}
```

> Note: public response uses key `"id"`, admin response uses key `"announcement_id"`.

---

### Get Announcement by ID

```
GET /announcement/{announcement_id}
```

**Path Parameters**

| Name | Type |
|------|------|
| `announcement_id` | integer |

**Query Parameters**

| Name | Type | Required |
|------|------|----------|
| `lang` | string | No |

**Response `200`**
```json
{
  "status_code": 200,
  "message": "Announcement details fetched successfully.",
  "announcement": {
    "announcement_id": 168384,
    "title": "Admission period open",
    "html_content": "<p>...</p>",
    "image": "static/announcements/168384.webp",
    "display_order": 1,
    "is_active": true
  }
}
```

---

### Create Announcement **[Admin]**

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

**Response `201`**
```json
{ "status_code": 201, "message": "Announcement created successfully." }
```

---

### Activate Announcement **[Admin]**

```
POST /announcement/activate?announcement_id={id}
```

**Response `200`**
```json
{ "status_code": 200, "message": "Announcement activated successfully." }
```

---

### Deactivate Announcement **[Admin]**

```
POST /announcement/deactivate?announcement_id={id}
```

**Response `200`**
```json
{ "status_code": 200, "message": "Announcement deactivated successfully." }
```

---

### Reorder Announcements **[Admin]**

```
POST /announcement/reorder
Content-Type: application/json
```

**Request Body**
```json
{
  "announcement_id": 168384,
  "new_order": 2
}
```

**Response `200`**
```json
{ "status_code": 200, "message": "Announcement reordered successfully" }
```

---

## Hero (Video Banner)

The hero is the full-screen video banner shown on the homepage. Only one hero can be active at a time.

### Get Active Hero (Public)

```
GET /hero/public
```

**Response `200`**
```json
{
  "status_code": 200,
  "message": "Hero fetched successfully.",
  "hero": {
    "hero_id": 512345,
    "video": "static/hero/512345.mp4",
    "is_active": true
  }
}
```

**Response `204`** — no active hero.

---

### Get All Heroes **[Admin]**

```
GET /hero/admin/all
```

**Response `200`**
```json
{
  "status_code": 200,
  "message": "Heroes fetched successfully.",
  "total": 3,
  "heroes": [
    {
      "hero_id": 512345,
      "video": "static/hero/512345.mp4",
      "is_active": true,
      "created_at": "2025-01-01T00:00:00",
      "updated_at": null
    }
  ]
}
```

---

### Upload Hero **[Admin]**

```
POST /hero/create
Content-Type: multipart/form-data
```

**Form Fields**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `video` | file | Yes | Video file (MP4 recommended). Large files — ensure nginx `client_max_body_size` is set to at least `100M`. |

**Response `201`**
```json
{
  "status_code": 201,
  "message": "Hero created successfully.",
  "hero_id": 512345
}
```

---

### Replace Hero Video **[Admin]**

```
PUT /hero/{hero_id}/update
Content-Type: multipart/form-data
```

**Form Fields**

| Name | Type | Required |
|------|------|----------|
| `video` | file | Yes |

**Response `200`**
```json
{ "status_code": 200, "message": "Hero updated successfully." }
```

**Response `404`** — hero not found.

---

### Activate Hero **[Admin]**

```
POST /hero/activate?hero_id={hero_id}
```

**Response `200`**
```json
{ "status_code": 200, "message": "Hero activated successfully." }
```

---

### Deactivate Hero **[Admin]**

```
POST /hero/deactivate?hero_id={hero_id}
```

**Response `200`**
```json
{ "status_code": 200, "message": "Hero deactivated successfully." }
```

---

### Delete Hero **[Admin]**

```
DELETE /hero/{hero_id}/delete
```

**Response `200`**
```json
{ "status_code": 200, "message": "Hero deleted successfully." }
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

**Response `200`**
```json
{
  "status_code": 200,
  "message": "Projects fetched successfully.",
  "total": 8,
  "projects": [
    {
      "id": 1,
      "project_id": "100001",
      "display_order": 1,
      "title": "Smart Campus Initiative",
      "description": "Short description...",
      "html_content": "<p>Full content...</p>",
      "created_at": "2025-01-01T00:00:00"
    }
  ]
}
```

---

### Get Project by ID

```
GET /project/{project_id}
```

**Path Parameters**

| Name | Type |
|------|------|
| `project_id` | string |

**Query Parameters**

| Name | Type | Required |
|------|------|----------|
| `lang` | string | No |

**Response `200`**
```json
{
  "status_code": 200,
  "message": "Project details fetched successfully.",
  "project": {
    "id": 1,
    "bg_image": "static/projects/100001.jpg",
    "title": "Smart Campus Initiative",
    "description": "Short description...",
    "html_content": "<p>...</p>",
    "display_order": 1,
    "created_at": "2025-01-01T00:00:00",
    "updated_at": null
  }
}
```

---

### Create Project **[Admin]**

```
POST /project/create
Content-Type: multipart/form-data
```

**Form Fields**

| Name | Type | Required |
|------|------|----------|
| `bg_image` | file | Yes |
| `az_title` | string | Yes |
| `az_description` | string | Yes |
| `az_content_html` | string | Yes |
| `en_title` | string | Yes |
| `en_description` | string | Yes |
| `en_content_html` | string | Yes |

**Response `201`**
```json
{ "status_code": 201, "message": "Project created successfully." }
```

---

### Reorder Projects **[Admin]**

```
POST /project/reorder
Content-Type: application/json
```

**Request Body**
```json
{
  "project_id": "100001",
  "new_order": 2
}
```

**Response `200`**
```json
{ "status_code": 200, "message": "Project reordered successfully" }
```

---

### Delete Project **[Admin]**

```
DELETE /project/{project_id}/delete
```

**Response `200`**
```json
{ "status_code": 200, "message": "Project deleted successfully." }
```

**Response `404`** — project not found.

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

**Response `200`**
```json
{
  "status_code": 200,
  "message": "Faculties fetched successfully.",
  "total": 5,
  "faculties": [
    {
      "id": 1,
      "faculty_code": "100001",
      "faculty_name": "Faculty of Engineering",
      "created_at": "2025-01-01T00:00:00"
    }
  ]
}
```

---

### Get All Faculties **[Admin]**

```
GET /faculty/admin/all
```

Same parameters and response as public endpoint.

---

### Get Faculty by Code

```
GET /faculty/{faculty_code}
```

**Path Parameters**

| Name | Type |
|------|------|
| `faculty_code` | string |

**Query Parameters**

| Name | Type | Required |
|------|------|----------|
| `lang` | string | No |

**Response `200`**
```json
{
  "status_code": 200,
  "message": "Faculty details fetched successfully.",
  "faculty": {
    "id": 1,
    "faculty_code": "100001",
    "faculty_name": "Faculty of Engineering",
    "created_at": "2025-01-01T00:00:00"
  }
}
```

---

### Create Faculty **[Admin]**

```
POST /faculty/create
Content-Type: multipart/form-data
```

**Form Fields**

| Name | Type | Required |
|------|------|----------|
| `az_name` | string | Yes |
| `en_name` | string | Yes |

**Response `201`**
```json
{
  "status_code": 201,
  "message": "Faculty created successfully.",
  "data": {
    "faculty_code": "100001",
    "created_at": "2025-01-01T00:00:00"
  }
}
```

---

### Update Faculty **[Admin]**

```
PUT /faculty/{faculty_code}
Content-Type: multipart/form-data
```

At least one field must be provided.

**Form Fields**

| Name | Type | Required |
|------|------|----------|
| `az_name` | string | No |
| `en_name` | string | No |

**Response `200`**
```json
{
  "status_code": 200,
  "message": "Faculty updated successfully.",
  "data": {
    "faculty_code": "100001",
    "faculty_name_az": "Mühəndislik Fakültəsi",
    "faculty_name_en": "Faculty of Engineering",
    "updated_at": "2025-06-01T12:00:00"
  }
}
```

**Response `400`** — no fields provided to update.
**Response `404`** — faculty not found.

---

### Delete Faculty **[Admin]**

```
DELETE /faculty/{faculty_code}
```

Deletes the faculty and all its translations.

**Response `200`**
```json
{ "status_code": 200, "message": "Faculty deleted successfully." }
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
| `lang` | string | No | `en` | Response language |

**Response `200`**
```json
{
  "status_code": 200,
  "message": "Cafedras fetched successfully.",
  "total": 20,
  "cafedras": [
    {
      "id": 1,
      "faculty_code": "100001",
      "cafedra_code": "200001",
      "cafedra_name": "Computer Science Department",
      "created_at": "2025-01-01T00:00:00"
    }
  ]
}
```

---

### Get All Cafedras **[Admin]**

```
GET /cafedra/admin/all
```

Same parameters and response as public endpoint.

---

### Get Cafedra by Code

```
GET /cafedra/{cafedra_code}
```

**Path Parameters**

| Name | Type |
|------|------|
| `cafedra_code` | string |

**Query Parameters**

| Name | Type | Required |
|------|------|----------|
| `lang` | string | No |

**Response `200`**
```json
{
  "status_code": 200,
  "message": "Cafedra details fetched successfully.",
  "cafedra": {
    "id": 1,
    "faculty_code": "100001",
    "cafedra_code": "200001",
    "cafedra_name": "Computer Science Department",
    "created_at": "2025-01-01T00:00:00"
  }
}
```

---

### Create Cafedra **[Admin]**

```
POST /cafedra/create
Content-Type: multipart/form-data
```

**Form Fields**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `faculty_code` | string | Yes | Parent faculty code |
| `az_name` | string | Yes | Azerbaijani name |
| `en_name` | string | Yes | English name |

**Response `201`**
```json
{
  "status_code": 201,
  "message": "Cafedra created successfully.",
  "data": {
    "cafedra_code": "200001",
    "faculty_code": "100001",
    "cafedra_name_az": "Kompüter Elmləri Kafedrası",
    "cafedra_name_en": "Computer Science Department",
    "created_at": "2025-01-01T00:00:00"
  }
}
```

**Response `404`** — faculty not found.

---

### Update Cafedra **[Admin]**

```
PUT /cafedra/{cafedra_code}
Content-Type: multipart/form-data
```

At least one field must be provided.

**Form Fields**

| Name | Type | Required |
|------|------|----------|
| `az_name` | string | No |
| `en_name` | string | No |

**Response `200`**
```json
{
  "status_code": 200,
  "message": "Cafedra updated successfully.",
  "data": {
    "cafedra_code": "200001",
    "faculty_code": "100001",
    "cafedra_name_az": "Kompüter Elmləri Kafedrası",
    "cafedra_name_en": "Computer Science Department",
    "updated_at": "2025-06-01T12:00:00"
  }
}
```

**Response `400`** — no fields provided.
**Response `404`** — cafedra not found.

---

### Delete Cafedra **[Admin]**

```
DELETE /cafedra/{cafedra_code}
```

**Response `200`**
```json
{ "status_code": 200, "message": "Cafedra deleted successfully." }
```

---

## Menu — Header

The header menu has a 3-level hierarchy: **Section → Item → Sub-Item**.

```
Section (e.g. "About")
  └── Item (e.g. "History")
        └── Sub-Item (e.g. "Founding Year")
```

### Get Full Header Menu

```
GET /menu/header
```

**Query Parameters**

| Name | Type | Required |
|------|------|----------|
| `lang` | string | No |

Returns the full nested header menu structure.

---

### Create Header Section **[Admin]**

```
POST /menu/header/section
Content-Type: application/json
```

**Request Body**
```json
{
  "section_key": "about",
  "image_url": "static/menu/about.svg",
  "display_order": 1,
  "label": { "az": "Haqqımızda", "en": "About" },
  "base_path": { "az": "/az/haqqimizda", "en": "/en/about" }
}
```

---

### Update Header Section **[Admin]**

```
PUT /menu/header/section/{section_id}
Content-Type: application/json
```

All fields optional:
```json
{
  "image_url": "static/menu/about-v2.svg",
  "display_order": 2,
  "label": { "az": "Haqqımızda", "en": "About Us" },
  "base_path": { "az": "/az/haqqimizda", "en": "/en/about-us" }
}
```

---

### Delete Header Section **[Admin]**

```
DELETE /menu/header/section/{section_id}
```

---

### Create Header Item **[Admin]**

```
POST /menu/header/item
Content-Type: application/json
```

**Request Body**
```json
{
  "section_id": 1,
  "slug": "history",
  "display_order": 1,
  "title": { "az": "Tarix", "en": "History" }
}
```

> `slug` is optional — omit it for items that only group sub-items.

---

### Update Header Item **[Admin]**

```
PUT /menu/header/item/{item_id}
Content-Type: application/json
```

All fields optional:
```json
{
  "slug": "history-updated",
  "display_order": 2,
  "title": { "az": "Tarix", "en": "History" }
}
```

---

### Delete Header Item **[Admin]**

```
DELETE /menu/header/item/{item_id}
```

---

### Create Header Sub-Item **[Admin]**

```
POST /menu/header/sub-item
Content-Type: application/json
```

**Request Body**
```json
{
  "item_id": 5,
  "slug": "founding-year",
  "display_order": 1,
  "title": { "az": "Təsis ili", "en": "Founding Year" }
}
```

---

### Update Header Sub-Item **[Admin]**

```
PUT /menu/header/sub-item/{sub_item_id}
Content-Type: application/json
```

All fields optional:
```json
{
  "slug": "founding-year",
  "display_order": 2,
  "title": { "en": "Founding Year (Updated)" }
}
```

---

### Delete Header Sub-Item **[Admin]**

```
DELETE /menu/header/sub-item/{sub_item_id}
```

---

## Menu — Footer

The footer has **columns → links**, plus independent partner logos and quick icons.

### Get Full Footer Menu

```
GET /menu/footer
```

**Query Parameters**

| Name | Type | Required |
|------|------|----------|
| `lang` | string | No |

Returns the full nested footer structure.

---

### Create Footer Column **[Admin]**

```
POST /menu/footer/column
Content-Type: application/json
```

**Request Body**
```json
{
  "display_order": 1,
  "title": { "az": "Əlaqə", "en": "Contact" }
}
```

---

### Update Footer Column **[Admin]**

```
PUT /menu/footer/column/{column_id}
Content-Type: application/json
```

All fields optional:
```json
{
  "display_order": 2,
  "title": { "en": "Contact Us" }
}
```

---

### Delete Footer Column **[Admin]**

```
DELETE /menu/footer/column/{column_id}
```

---

### Create Footer Link **[Admin]**

```
POST /menu/footer/link
Content-Type: application/json
```

**Request Body**
```json
{
  "column_id": 1,
  "url": "/en/contact",
  "display_order": 1,
  "label": { "az": "Bizimlə əlaqə", "en": "Contact Us" }
}
```

---

### Update Footer Link **[Admin]**

```
PUT /menu/footer/link/{link_id}
Content-Type: application/json
```

All fields optional:
```json
{
  "url": "/en/contact-updated",
  "display_order": 2,
  "label": { "en": "Get In Touch" }
}
```

---

### Delete Footer Link **[Admin]**

```
DELETE /menu/footer/link/{link_id}
```

---

### Create Partner Logo **[Admin]**

```
POST /menu/footer/partner-logo
Content-Type: application/json
```

**Request Body**
```json
{
  "label": "Ministry of Education",
  "image_url": "static/partners/ministry.png",
  "url": "https://edu.gov.az",
  "display_order": 1
}
```

---

### Update Partner Logo **[Admin]**

```
PUT /menu/footer/partner-logo/{logo_id}
Content-Type: application/json
```

All fields optional:
```json
{
  "label": "Ministry of Education AZ",
  "image_url": "static/partners/ministry-v2.png",
  "url": "https://edu.gov.az",
  "display_order": 2
}
```

---

### Delete Partner Logo **[Admin]**

```
DELETE /menu/footer/partner-logo/{logo_id}
```

---

### Create Footer Quick Icon **[Admin]**

```
POST /menu/footer/quick-icon
Content-Type: application/json
```

**Request Body**
```json
{
  "icon": "mdi:phone",
  "url": "tel:+994124445566",
  "display_order": 1,
  "label": { "az": "Zəng edin", "en": "Call Us" }
}
```

---

### Update Footer Quick Icon **[Admin]**

```
PUT /menu/footer/quick-icon/{icon_id}
Content-Type: application/json
```

All fields optional:
```json
{
  "icon": "mdi:email",
  "url": "mailto:info@aztu.edu.az",
  "display_order": 2,
  "label": { "en": "Email Us" }
}
```

---

### Delete Footer Quick Icon **[Admin]**

```
DELETE /menu/footer/quick-icon/{icon_id}
```

---

## Menu — Quick Menu

The quick menu has two parts: **left items** (standalone links) and **sections → section items**.

### Get Full Quick Menu

```
GET /menu/quick
```

**Query Parameters**

| Name | Type | Required |
|------|------|----------|
| `lang` | string | No |

---

### Create Quick Left Item **[Admin]**

```
POST /menu/quick/left-item
Content-Type: application/json
```

**Request Body**
```json
{
  "url": "/en/e-library",
  "display_order": 1,
  "label": { "az": "Elektron kitabxana", "en": "E-Library" }
}
```

---

### Update Quick Left Item **[Admin]**

```
PUT /menu/quick/left-item/{item_id}
Content-Type: application/json
```

All fields optional:
```json
{
  "url": "/en/digital-library",
  "display_order": 2,
  "label": { "en": "Digital Library" }
}
```

---

### Delete Quick Left Item **[Admin]**

```
DELETE /menu/quick/left-item/{item_id}
```

---

### Create Quick Section **[Admin]**

```
POST /menu/quick/section
Content-Type: application/json
```

**Request Body**
```json
{
  "section_key": "student-services",
  "display_order": 1,
  "title": { "az": "Tələbə xidmətləri", "en": "Student Services" }
}
```

---

### Update Quick Section **[Admin]**

```
PUT /menu/quick/section/{section_id}
Content-Type: application/json
```

All fields optional:
```json
{
  "display_order": 2,
  "title": { "en": "Student Portal" }
}
```

---

### Delete Quick Section **[Admin]**

```
DELETE /menu/quick/section/{section_id}
```

---

### Create Quick Section Item **[Admin]**

```
POST /menu/quick/section-item
Content-Type: application/json
```

**Request Body**
```json
{
  "section_id": 3,
  "url": "/en/student-portal",
  "display_order": 1,
  "label": { "az": "Tələbə portalı", "en": "Student Portal" }
}
```

---

### Update Quick Section Item **[Admin]**

```
PUT /menu/quick/section-item/{item_id}
Content-Type: application/json
```

All fields optional:
```json
{
  "url": "/en/portal-v2",
  "display_order": 2,
  "label": { "en": "New Student Portal" }
}
```

---

### Delete Quick Section Item **[Admin]**

```
DELETE /menu/quick/section-item/{item_id}
```

---

## Menu — Social Links

Social links can appear in the footer, the quick menu, or both.

### Create Social Link **[Admin]**

```
POST /menu/social-link
Content-Type: application/json
```

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `platform` | string | Yes | e.g. `"instagram"`, `"youtube"`, `"facebook"` |
| `url` | string | Yes | Full URL |
| `context` | string | Yes | `"footer"` \| `"quick"` \| `"both"` |
| `display_order` | integer | Yes | |

```json
{
  "platform": "instagram",
  "url": "https://instagram.com/aztu.edu.az",
  "context": "both",
  "display_order": 1
}
```

---

### Update Social Link **[Admin]**

```
PUT /menu/social-link/{link_id}
Content-Type: application/json
```

All fields optional:
```json
{
  "url": "https://instagram.com/aztu_official",
  "context": "footer",
  "display_order": 2
}
```

---

### Delete Social Link **[Admin]**

```
DELETE /menu/social-link/{link_id}
```

---

## Menu — Contacts

Contacts can be assigned to `"footer"` or `"quick"` context. Footer contacts include a physical address.

### Create Contact **[Admin]**

```
POST /menu/contact
Content-Type: application/json
```

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `context` | string | Yes | `"footer"` \| `"quick"` |
| `email` | string | Yes | |
| `phones` | string[] | Yes | List of phone numbers |
| `address` | object | No | Footer only — `{ "az": "...", "en": "..." }` |

```json
{
  "context": "footer",
  "email": "info@aztu.edu.az",
  "phones": ["+994 12 444 55 66", "+994 12 444 55 67"],
  "address": {
    "az": "Bakı, H.Cavid pr. 25",
    "en": "25 H.Javid Ave, Baku"
  }
}
```

---

### Update Contact **[Admin]**

```
PUT /menu/contact/{contact_id}
Content-Type: application/json
```

All fields optional:
```json
{
  "email": "contact@aztu.edu.az",
  "phones": ["+994 12 444 55 66"],
  "address": { "en": "25 H.Javid Avenue, Baku, Azerbaijan" }
}
```

---

### Delete Contact **[Admin]**

```
DELETE /menu/contact/{contact_id}
```

---

## Static Files

Uploaded files are served at:

```
GET /static/{entity_type}/{filename}
```

| Entity | Path pattern | Example |
|--------|-------------|---------|
| News cover | `static/news/{news_id}.{ext}` | `static/news/123456.jpg` |
| News gallery | `static/news/{news_id}-gallery-{n}.{ext}` | `static/news/123456-gallery-1.jpeg` |
| Announcement | `static/announcements/{id}.{ext}` | `static/announcements/168384.webp` |
| Hero video | `static/hero/{hero_id}.{ext}` | `static/hero/512345.mp4` |
| Project image | `static/projects/{project_id}.{ext}` | `static/projects/100001.jpg` |

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "status_code": 404,
  "message": "Item not found."
}
```

Or for server errors:
```json
{
  "status_code": 500,
  "error": "error detail string"
}
```

| Status Code | Meaning |
|-------------|---------|
| `200` | OK |
| `201` | Created |
| `204` | No Content (empty result — no body) |
| `400` | Bad Request — e.g. no fields provided for update |
| `404` | Not Found |
| `409` | Conflict — e.g. duplicate title |
| `422` | Unprocessable Entity — validation error (e.g. invalid `lang`) |
| `500` | Internal Server Error |

---

## Notes

- **No authentication** is required for any endpoint currently. Endpoints marked **[Admin]** are intended for the admin panel only.
- All `created_at` / `updated_at` timestamps are in **ISO 8601** format without timezone (`"2025-01-15T10:00:00"`).
- Pagination uses `start` (offset) and `end` (exclusive upper bound), not page numbers. Example: `start=0&end=10` returns the first 10 items.
- `news_id`, `announcement_id`, and `hero_id` are 6-digit randomly generated integers (`100000`–`999999`).
- `faculty_code` and `cafedra_code` are auto-generated 6-digit numeric strings (stored as strings).
- For large file uploads (hero videos, news gallery), the nginx proxy must have `client_max_body_size 100M;` set on the server.
- Menu `label` / `title` / `base_path` fields that take `{ "az": "...", "en": "..." }` are **bilingual objects**, not plain strings.
