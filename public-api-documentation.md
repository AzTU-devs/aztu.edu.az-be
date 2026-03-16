# AzTU Public API Documentation

This document covers all public-facing API endpoints for the AzTU website frontend. None of these endpoints require authentication.

---

## Base URL

```
https://<your-domain>
```

Static files (images, videos) are served at:

```
https://<your-domain>/static/<path>
```

Image/video paths returned by the API are relative (e.g., `static/news/123.jpg`). Prepend the base URL to get the full URL.

---

## Internationalization (i18n)

All content endpoints support two languages: **Azerbaijani (`az`)** and **English (`en`)**.

Set the language using either:

- Query parameter: `?lang=az` or `?lang=en`
- HTTP header: `Accept-Language: az` or `Accept-Language: en`

Default language is `en` if not specified.

---

## Common Response Format

All responses include a `status_code` field in the body matching the HTTP status code:

```json
{
  "status_code": 200,
  "message": "...",
  "data": ...
}
```

**Error responses:**

| Status | Meaning |
|--------|---------|
| 204 | No content found |
| 404 | Resource not found |
| 500 | Internal server error |

---

## Endpoints

### System

#### Health Check

```
GET /health
```

**Response `200`:**
```json
{ "status": "ok" }
```

---

### News

#### Get Public News List

```
GET /api/news/public/all
```

Returns only active (published) news articles.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lang` | string | No | `en` | Language code: `az` or `en` |
| `start` | integer | No | `0` | Pagination start index |
| `end` | integer | No | `10` | Pagination end index |
| `category_id` | integer | No | — | Filter by news category ID |

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "News fetched successfully.",
  "total": 42,
  "news": [
    {
      "news_id": 123456,
      "category_id": 789012,
      "display_order": 1,
      "is_active": true,
      "title": "News title in requested language",
      "html_content": "<p>Full HTML content...</p>"
    }
  ]
}
```

> `total` is the total count of all news records (regardless of pagination). Use `start`/`end` for paging.

**Response `204`:** No news found.

---

#### Get News Details

```
GET /api/news/{news_id}
```

Returns full details for a single news article including **both languages** (az and en).

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `news_id` | integer | Yes | News ID |

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "News details fetched successfully.",
  "news": {
    "news_id": 123456,
    "az_title": "Xəbər başlığı",
    "az_html_content": "<p>Azərbaycan dilində məzmun...</p>",
    "en_title": "News title",
    "en_html_content": "<p>English content...</p>",
    "category_id": "Category name (az)",
    "cover_image": "static/news/123456.jpg",
    "gallery_images": [
      {
        "image_id": 1,
        "image": "static/news/123456-gallery-1.jpg"
      }
    ]
  }
}
```

> Note: `category_id` field in the detail response actually contains the **category name in Azerbaijani** (not the numeric ID). This is a known API behavior.

**Response `404`:** News not found.

---

#### Get News Gallery

```
GET /api/news/gallery
```

Returns all gallery images (including cover) for a specific news article.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `news_id` | integer | Yes | News ID |

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "News gallery fetched successfully.",
  "gallery_images": [
    {
      "id": 1,
      "news_id": 123456,
      "image": "static/news/123456.jpg"
    }
  ]
}
```

**Response `204`:** No gallery images found.
**Response `404`:** News not found.

---

### News Categories

#### Get All News Categories

```
GET /api/news-category/all
```

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lang` | string | No | `en` | Language code: `az` or `en` |

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "News categories fetched successfully.",
  "news_categories": [
    {
      "category_id": 789012,
      "title": "Category name in requested language"
    }
  ]
}
```

**Response `204`:** No categories found.

---

### Hero / Banner

#### Get Active Hero Video

```
GET /api/hero/public
```

Returns the currently active hero section video.

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "Hero fetched successfully.",
  "hero": {
    "hero_id": 456789,
    "video": "static/hero/456789.mp4",
    "is_active": true
  }
}
```

**Response `204`:** No active hero found.

---

### Announcements

#### Get Public Announcements List

```
GET /api/announcement/public/all
```

Returns only active announcements.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lang` | string | No | `en` | Language code: `az` or `en` |
| `start` | integer | No | `0` | Pagination start index |
| `end` | integer | No | `4` | Pagination end index |

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "Announcements fetched successfully.",
  "announcements": [
    {
      "id": 123456,
      "display_order": 1,
      "title": "Announcement title",
      "html_content": "<p>Full HTML content...</p>",
      "is_active": true,
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

> Note: The public list does **not** return the `total` count. Use pagination params accordingly.

**Response `204`:** No announcements found.

---

#### Get Announcement Details

```
GET /api/announcement/{announcement_id}
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `announcement_id` | integer | Yes | Announcement ID |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lang` | string | No | `en` | Language code: `az` or `en` |

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "Announcement details fetched successfully.",
  "announcement": {
    "announcement_id": 123456,
    "title": "Announcement title",
    "html_content": "<p>Full HTML content...</p>",
    "image": "static/announcements/123456.jpg",
    "display_order": 1,
    "is_active": true
  }
}
```

**Response `404`:** Announcement not found.

---

### Projects

#### Get Projects List

```
GET /api/project/all
```

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lang` | string | No | `en` | Language code: `az` or `en` |
| `start` | integer | No | `0` | Pagination start index |
| `end` | integer | No | `4` | Pagination end index |

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "Projects fetched successfully.",
  "total": 12,
  "projects": [
    {
      "id": 1,
      "project_id": 567890,
      "display_order": 1,
      "title": "Project title",
      "description": "Short description",
      "html_content": "<p>Full HTML content...</p>",
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

**Response `204`:** No projects found.

---

#### Get Project Details

```
GET /api/project/{project_id}
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | string | Yes | Project ID |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lang` | string | No | `en` | Language code: `az` or `en` |

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "Project details fetched successfully.",
  "project": {
    "id": 1,
    "bg_image": "static/projects/567890.jpg",
    "title": "Project title",
    "description": "Short description",
    "html_content": "<p>Full HTML content...</p>",
    "display_order": 1,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": null
  }
}
```

**Response `404`:** Project not found.

---

### Faculties

#### Get Faculties List

```
GET /api/faculty/public/all
```

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lang` | string | No | `en` | Language code: `az` or `en` |
| `start` | integer | No | `0` | Pagination start index |
| `end` | integer | No | `10` | Pagination end index |

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "Faculties fetched successfully.",
  "total": 8,
  "faculties": [
    {
      "id": 1,
      "faculty_code": "123456",
      "faculty_name": "Faculty name in requested language",
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

**Response `204`:** No faculties found.

---

#### Get Faculty Details

```
GET /api/faculty/{faculty_code}
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `faculty_code` | string | Yes | Faculty code |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lang` | string | No | `en` | Language code: `az` or `en` |

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "Faculty details fetched successfully.",
  "faculty": {
    "id": 1,
    "faculty_code": "123456",
    "faculty_name": "Faculty name in requested language",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

**Response `404`:** Faculty not found.

---

### Cafedras (Departments)

#### Get Cafedras List

```
GET /api/cafedra/public/all
```

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lang` | string | No | `en` | Language code: `az` or `en` |
| `start` | integer | No | `0` | Pagination start index |
| `end` | integer | No | `10` | Pagination end index |
| `faculty_code` | string | No | — | Filter cafedras by faculty code |

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "Cafedras fetched successfully.",
  "total": 25,
  "cafedras": [
    {
      "id": 1,
      "faculty_code": "123456",
      "cafedra_code": "789012",
      "cafedra_name": "Department name in requested language",
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

**Response `204`:** No cafedras found.

---

#### Get Cafedra Details

```
GET /api/cafedra/{cafedra_code}
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `cafedra_code` | string | Yes | Cafedra code |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lang` | string | No | `en` | Language code: `az` or `en` |

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "Cafedra details fetched successfully.",
  "cafedra": {
    "id": 1,
    "faculty_code": "123456",
    "cafedra_code": "789012",
    "cafedra_name": "Department name in requested language",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

**Response `404`:** Cafedra not found.

---

### Collaborations

#### Get Collaborations List

```
GET /api/collaboration/all
```

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lang` | string | No | `en` | Language code: `az` or `en` |
| `start` | integer | No | `0` | Pagination start index |
| `end` | integer | No | `10` | Pagination end index |

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "Collaborations fetched successfully.",
  "total": 15,
  "collaborations": [
    {
      "id": 1,
      "collaboration_id": 345678,
      "logo": "static/collaborations/345678.png",
      "website_url": "https://partner.org",
      "display_order": 1,
      "name": "Partner name in requested language",
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

**Response `204`:** No collaborations found.

---

#### Get Collaboration Details

```
GET /api/collaboration/{collaboration_id}
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `collaboration_id` | integer | Yes | Collaboration ID |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lang` | string | No | `en` | Language code: `az` or `en` |

**Response `200`:**
```json
{
  "status_code": 200,
  "message": "Collaboration fetched successfully.",
  "collaboration": {
    "id": 1,
    "collaboration_id": 345678,
    "logo": "static/collaborations/345678.png",
    "website_url": "https://partner.org",
    "display_order": 1,
    "name": "Partner name in requested language",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": null
  }
}
```

**Response `404`:** Collaboration not found.

---

### Menu

#### Get Header Menu

```
GET /api/menu/header
```

Returns the full navigation header structure.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lang` | string | No | `en` | Language code: `az` or `en` |

**Response `200`:**
```json
{
  "status_code": 200,
  "data": {
    "sections": [
      {
        "key": "about",
        "label": "About",
        "base_path": "/about",
        "image_url": "https://example.com/section-image.jpg",
        "items": [
          {
            "title": "History",
            "slug": "history",
            "sub_items": [
              {
                "title": "Early Years",
                "slug": "early-years"
              }
            ]
          }
        ]
      }
    ]
  }
}
```

> `slug` on items can be `null` if the item is a category header with no direct link.

---

#### Get Footer Menu

```
GET /api/menu/footer
```

Returns the full footer structure including navigation columns, contact info, social links, partner logos, and quick icons.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lang` | string | No | `en` | Language code: `az` or `en` |

**Response `200`:**
```json
{
  "status_code": 200,
  "data": {
    "university_name": "Azerbaijan Technical University",
    "columns": [
      {
        "title": "Column title",
        "links": [
          {
            "label": "Link label",
            "url": "/page-path"
          }
        ]
      }
    ],
    "contact": {
      "email": "info@aztu.edu.az",
      "phones": ["+994 12 498 20 26"],
      "address": "Baku, Azerbaijan, H. Cavid Ave. 25"
    },
    "social_links": [
      {
        "platform": "facebook",
        "url": "https://facebook.com/aztu"
      }
    ],
    "partner_logos": [
      {
        "label": "Partner Name",
        "image_url": "https://example.com/logo.png",
        "url": "https://partner.org"
      }
    ],
    "quick_icons": [
      {
        "label": "Icon label",
        "icon": "icon-class-name",
        "url": "/page-path"
      }
    ]
  }
}
```

> `contact` will be an empty object `{}` if no footer contact is configured.

---

#### Get Quick Menu

```
GET /api/menu/quick
```

Returns the quick-access menu structure (typically rendered as a side drawer or quick nav overlay).

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lang` | string | No | `en` | Language code: `az` or `en` |

**Response `200`:**
```json
{
  "status_code": 200,
  "data": {
    "title": "AzTU Quick Menu",
    "left_items": [
      {
        "label": "Item label",
        "url": "/page-path"
      }
    ],
    "contact": {
      "email": "info@aztu.edu.az",
      "phones": ["+994 12 498 20 26"]
    },
    "social_links": [
      {
        "platform": "instagram",
        "url": "https://instagram.com/aztu"
      }
    ],
    "right_sections": [
      {
        "key": "students",
        "title": "Students",
        "items": [
          {
            "label": "Item label",
            "url": "/page-path"
          }
        ]
      }
    ]
  }
}
```

> `contact` will be an empty object `{}` if no quick menu contact is configured.

---

## Pagination Guide

Endpoints that support pagination use `start` and `end` as **index bounds** (not page number and size):

- To get the first 10 items: `?start=0&end=10`
- To get items 11–20: `?start=10&end=20`
- To get items 21–30: `?start=20&end=30`

The `total` field in paginated responses reflects the **total count** in the database, useful for calculating total pages.

---

## Static File URLs

Image and video paths returned by the API are relative paths. To construct the full URL:

```
{BASE_URL}/{relative_path}

Example:
  Base URL:      https://api.aztu.edu.az
  Returned path: static/news/123456.jpg
  Full URL:      https://api.aztu.edu.az/static/news/123456.jpg
```
