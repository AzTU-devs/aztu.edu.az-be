# AzTU Public API Documentation

This document covers all public-facing API endpoints for the AzTU website frontend. None of these endpoints require authentication.


## Base URL

```
https://<your-domain>
```

Static files (images, videos) are served at:

```
https://<your-domain>/static/<path>
```

Image/video paths returned by the API are relative (e.g., `static/news/123.jpg`). Prepend the base URL to get the full URL.


## Internationalization (i18n)

All content endpoints support two languages: **Azerbaijani (`az`)** and **English (`en`)**.

Set the language using either:

- Query parameter: `?lang=az` or `?lang=en`
- HTTP header: `Accept-Language: az` or `Accept-Language: en`

Default language is `en` if not specified.


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
{BASE_URL}/{relative_path}w

Example:
  Base URL:      https://api.aztu.edu.az
  Returned path: static/news/123456.jpg
  Full URL:      https://api.aztu.edu.az/static/news/123456.jpg
```











INSERT INTO menu_header_sections (id, section_key, image_url, display_order, is_active) VALUES
(1, 'about',          '', 1, TRUE),
(2, 'academics',      '', 2, TRUE),
(3, 'administration', '', 3, TRUE),
(4, 'students',       '', 4, TRUE),
(5, 'research',       '', 5, TRUE),
(6, 'community',      '', 6, TRUE),
(7, 'sustainability', '', 7, TRUE),
(8, 'contact',        '', 8, TRUE);

INSERT INTO menu_header_section_translations (section_id, lang_code, label, base_path) VALUES
(1, 'en', 'About',          '/about'),
(1, 'az', 'Haqqımızda',     '/about'),
(2, 'en', 'Academics',      '/academics'),
(2, 'az', 'Akademik',       '/academics'),
(3, 'en', 'Administration', '/administration'),
(3, 'az', 'İdarəetmə',      '/administration'),
(4, 'en', 'Students',       '/students'),
(4, 'az', 'Tələbələr',      '/students'),
(5, 'en', 'Research',       '/research'),
(5, 'az', 'Tədqiqat',       '/research'),
(6, 'en', 'Community',      '/community'),
(6, 'az', 'İcma',           '/community'),
(7, 'en', 'Sustainability',  '/sustainability'),
(7, 'az', 'Dayanıqlılıq',   '/sustainability'),
(8, 'en', 'Contact',        '/contact'),
(8, 'az', 'Əlaqə',          '/contact');

INSERT INTO menu_header_items (id, section_id, slug, display_order, is_active) VALUES
(1,  1, 'vision-mission',                          1, TRUE),
(2,  1, 'leadership-governance',                   2, TRUE),
(3,  1, 'partner-university-affiliated-institutes', 3, TRUE),
(4,  1, 'normativ-senedler',                       4, TRUE),
(5,  2, 'faculties',                  1, TRUE),
(6,  2, 'higher-education-institutes', 2, TRUE),
(7,  3, 'departments',         1, TRUE),
(8,  3, 'offices-and-centers', 2, TRUE),
(9,  4, 'academic-calendar-and-guidelines', 1, TRUE),
(10, 4, 'undergraduate',                    2, TRUE),
(11, 4, 'postgraduates',                    3, TRUE),
(12, 5, 'research-activities',          1, TRUE),
(13, 5, 'conferences-and-events',       2, TRUE),
(14, 5, 'research-labs',                3, TRUE),
(15, 5, 'scientific-journals',          4, TRUE),
(16, 5, 'publications-and-dissemination', 5, TRUE),
(17, 5, 'performance-and-evaluation',   6, TRUE),
(18, 6, 'campus-life',            1, TRUE),
(19, 6, 'union-and-organizations', 2, TRUE);

INSERT INTO menu_header_item_translations (item_id, lang_code, title) VALUES
(1,  'en', 'Vision & Mission'),
(1,  'az', 'Vizyon & Missiya'),
(2,  'en', 'Leadership & Governance'),
(2,  'az', 'Rəhbərlik & İdarəetmə'),
(3,  'en', 'Partner University & Affiliated Institutes'),
(3,  'az', 'Tərəfdaş Universitet & Bağlı Qurumlar'),
(4,  'en', 'Legal Documents'),
(4,  'az', 'Normativ Sənədlər'),
(5,  'en', 'Faculties'),
(5,  'az', 'Fakültələr'),
(6,  'en', 'Higher Education Institutes'),
(6,  'az', 'Ali Təhsil İnstitutları'),
(7,  'en', 'Departments'),
(7,  'az', 'Struktur Bölmələr'),
(8,  'en', 'Offices & Centers'),
(8,  'az', 'Ofis və Mərkəzlər'),
(9,  'en', 'Academic Calendar & Guidelines'),
(9,  'az', 'Akademik Təqvim və Qaydalar'),
(10, 'en', 'Undergraduate'),
(10, 'az', 'Bakalavr'),
(11, 'en', 'Postgraduates'),
(11, 'az', 'Magistratura'),
(12, 'en', 'Research Activities'),
(12, 'az', 'Tədqiqat Fəaliyyətləri'),
(13, 'en', 'Conferences & Events'),
(13, 'az', 'Konfranslar & Tədbirlər'),
(14, 'en', 'Research Labs'),
(14, 'az', 'Tədqiqat Laboratoriyaları'),
(15, 'en', 'Scientific Journals'),
(15, 'az', 'Elmi Jurnallar'),
(16, 'en', 'Publications & Dissemination'),
(16, 'az', 'Nəşrlər & Yayım'),
(17, 'en', 'Performance & Evaluation'),
(17, 'az', 'Performans & Qiymətləndirmə'),
(18, 'en', 'Campus Life'),
(18, 'az', 'Kampus Həyatı'),
(19, 'en', 'Union and Organizations'),
(19, 'az', 'Birlik və Təşkilatlar');

INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(1,  1, 'about/vision-mission/vision',              1, TRUE),
(2,  1, 'about/vision-mission/mission',             2, TRUE),
(3,  1, 'about/vision-mission/history-of-aztu',     3, TRUE),
(4,  1, 'about/vision-mission/75th-anniversary-film', 4, TRUE),
(5,  1, 'about/vision-mission/strategic-plan',      5, TRUE),
-- Leadership & Governance (item 2)
(6,  2, 'about/leadership-governance/rector',         1, TRUE),
(7,  2, 'about/leadership-governance/vice-rector',    2, TRUE),
(8,  2, 'about/leadership-governance/scientific-board', 3, TRUE),
(9,  3, 'about/partners/turkish-azerbaijan-university',              1, TRUE),
(10, 3, 'about/partners/institute-of-information-technology',        2, TRUE),
(11, 3, 'about/partners/institute-of-control-systems',               3, TRUE),
(12, 3, 'about/partners/baku-technical-colleges',                    4, TRUE),
(13, 3, 'about/partners/baku-state-colleges-communication-transport', 5, TRUE),
(14, 4, 'about/legal-documents/general-policies',        1, TRUE),
(15, 4, 'about/legal-documents/academic-policies',       2, TRUE),
(16, 4, 'about/legal-documents/sustainability-policies', 3, TRUE),
(17, 4, 'about/legal-documents/procedure-and-guidelines', 4, TRUE),
(18, 5, 'academics/faculties/faculty-1', 1, TRUE),
(19, 5, 'academics/faculties/faculty-2', 2, TRUE),
(20, 5, 'academics/faculties/faculty-3', 3, TRUE),
(21, 5, 'academics/faculties/faculty-4', 4, TRUE),
(22, 5, 'academics/faculties/faculty-5', 5, TRUE),
(23, 5, 'academics/faculties/faculty-6', 6, TRUE),
(24, 6, 'academics/higher-education/mba',  1, TRUE),
(25, 6, 'academics/higher-education/cdio', 2, TRUE),
(26, 7, 'administration/departments/education-affairs',             1, TRUE),
(27, 7, 'administration/departments/research-development-reputation', 2, TRUE),
(28, 7, 'administration/departments/international-affairs',          3, TRUE),
(29, 7, 'administration/departments/quality-assurance',              4, TRUE),
(30, 7, 'administration/departments/documents-and-applications',     5, TRUE),
(31, 7, 'administration/departments/human-resources',                6, TRUE),
(32, 7, 'administration/departments/finance-and-accountant',         7, TRUE),
(33, 7, 'administration/departments/information-technologies',       8, TRUE),
(34, 7, 'administration/departments/communication',                  9, TRUE),
(35, 7, 'administration/departments/mass-media',                    10, TRUE),
(36, 7, 'administration/departments/analytical-analysis',           11, TRUE),
(37, 7, 'administration/departments/procurement',                   12, TRUE),
(38, 8, 'administration/centers/career-and-employability',   1, TRUE),
(39, 8, 'administration/centers/lifelong-learning',          2, TRUE),
(40, 8, 'administration/centers/technology-transfer-office', 3, TRUE),
(41, 8, 'administration/centers/nabran-resort-centre',       4, TRUE),
(42, 8, 'administration/centers/sabah-centre',               5, TRUE),
(43, 8, 'administration/centers/library-information-centre', 6, TRUE),
(44, 9, 'students/calendar/academic-calendar-2026-2027',      1, TRUE),
(45, 9, 'students/calendar/academic-calendar-2025-2026',      2, TRUE),
(46, 9, 'students/calendar/organization-of-examinations',     3, TRUE),
(47, 9, 'students/calendar/credit-system',                    4, TRUE),
(48, 9, 'students/calendar/lms-guidelines',                   5, TRUE),
(49, 10, 'students/undergraduate/specialties',      1, TRUE),
(50, 10, 'students/undergraduate/curriculum',       2, TRUE),
(51, 10, 'students/undergraduate/learning-outcomes', 3, TRUE),
(52, 10, 'students/undergraduate/exchange-programs', 4, TRUE),
(53, 10, 'students/undergraduate/tuition-fees',     5, TRUE),
(54, 11, 'students/postgraduates/specialties',             1, TRUE),
(55, 11, 'students/postgraduates/curriculum',              2, TRUE),
(56, 11, 'students/postgraduates/cdio',                    3, TRUE),
(57, 11, 'students/postgraduates/international-students-unit', 4, TRUE),
(58, 11, 'students/postgraduates/exchange-programs',       5, TRUE),
(59, 12, 'research/activities/research-priorities',          1, TRUE),
(60, 12, 'research/activities/research-institutes',          2, TRUE),
(61, 12, 'research/activities/interdisciplinary-research',   3, TRUE),
(62, 12, 'research/activities/intellectual-property-patents', 4, TRUE),
(63, 12, 'research/activities/research-projects',            5, TRUE),
(64, 13, 'research/conferences/local-conferences',        1, TRUE),
(65, 13, 'research/conferences/international-conferences', 2, TRUE),
(66, 13, 'research/conferences/seminars-and-trainings',   3, TRUE),
(67, 14, 'research/labs/lab-1', 1, TRUE),
-- Scientific Journals (item 15)
(68, 15, 'research/journals/machine-science',                              1, TRUE),
(69, 15, 'research/journals/energy-sustainability-risks-and-decisions',    2, TRUE),
(70, 15, 'research/journals/scientific-works',                             3, TRUE),
(71, 15, 'research/journals/journal-advance-material-processing',          4, TRUE),
(72, 16, 'research/publications/open-access-policy',         1, TRUE),
(73, 16, 'research/publications/plagiarism-and-ethics',      2, TRUE),
(74, 16, 'research/publications/ethics-and-compliance',      3, TRUE),
(75, 16, 'research/publications/annual-research-reports',    4, TRUE),
(76, 17, 'research/performance/incentive-mechanism',    1, TRUE),
(77, 17, 'research/performance/researcher-platforms',   2, TRUE),
(78, 17, 'research/performance/internal-grant-programs', 3, TRUE),
(79, 18, 'community/campus-life/student-life',    1, TRUE),
(80, 18, 'community/campus-life/clubs',           2, TRUE),
(81, 18, 'community/campus-life/sport',           3, TRUE),
(82, 18, 'community/campus-life/cultural-events', 4, TRUE),
(83, 18, 'community/campus-life/aztu-polyclinic', 5, TRUE),
(84, 19, 'community/organizations/trade-union',             1, TRUE),
(85, 19, 'community/organizations/student-trade-union',     2, TRUE),
(86, 19, 'community/organizations/student-youth-organization', 3, TRUE);

INSERT INTO menu_header_sub_item_translations (sub_item_id, lang_code, title) VALUES
(1,  'en', 'Vision'),               (1,  'az', 'Vizyon'),
(2,  'en', 'Mission'),              (2,  'az', 'Missiya'),
(3,  'en', 'History of AzTU'),      (3,  'az', 'AzTU Tarixi'),
(4,  'en', '75th Anniversary Film'),(4,  'az', '75-ci İllik Filmi'),
(5,  'en', 'Strategic Plan'),       (5,  'az', 'Strateji Plan'),
(6,  'en', 'Rector'),               (6,  'az', 'Rektor'),
(7,  'en', 'Vice-Rector'),          (7,  'az', 'Prorektor'),
(8,  'en', 'Scientific Board'),     (8,  'az', 'Elmi Şura'),
(9,  'en', 'Turkish-Azerbaijan University (TAU)'),               (9,  'az', 'Türk-Azərbaycan Universiteti (TAU)'),
(10, 'en', 'Institute of Information Technology'),               (10, 'az', 'İnformasiya Texnologiyaları İnstitutu'),
(11, 'en', 'Institute of Control Systems'),                      (11, 'az', 'İdarəetmə Sistemləri İnstitutu'),
(12, 'en', 'Baku Technical Colleges'),                           (12, 'az', 'Bakı Texniki Kollecləri'),
(13, 'en', 'Baku State Colleges of Communication and Transport'),(13, 'az', 'Bakı Dövlət Rabitə və Nəqliyyat Kollecləri'),
(14, 'en', 'General Policies'),          (14, 'az', 'Ümumi Siyasətlər'),
(15, 'en', 'Academic Policies'),         (15, 'az', 'Akademik Siyasətlər'),
(16, 'en', 'Sustainability Policies'),   (16, 'az', 'Dayanıqlılıq Siyasətləri'),
(17, 'en', 'Procedure and Guidelines'),  (17, 'az', 'Prosedur və Qaydalar'),
(18, 'en', 'Faculty 1'), (18, 'az', 'Fakültə 1'),
(19, 'en', 'Faculty 2'), (19, 'az', 'Fakültə 2'),
(20, 'en', 'Faculty 3'), (20, 'az', 'Fakültə 3'),
(21, 'en', 'Faculty 4'), (21, 'az', 'Fakültə 4'),
(22, 'en', 'Faculty 5'), (22, 'az', 'Fakültə 5'),
(23, 'en', 'Faculty 6'), (23, 'az', 'Fakültə 6'),
(24, 'en', 'MBA'),  (24, 'az', 'MBA'),
(25, 'en', 'CDIO'), (25, 'az', 'CDIO'),
(26, 'en', 'Education Affairs'),                   (26, 'az', 'Tədris İşləri'),
(27, 'en', 'Research, Development and Reputation'),(27, 'az', 'Tədqiqat, İnkişaf və Reputasiya'),
(28, 'en', 'International Affairs'),               (28, 'az', 'Beynəlxalq Əlaqələr'),
(29, 'en', 'Quality Assurance'),                   (29, 'az', 'Keyfiyyətin Təminatı'),
(30, 'en', 'Documents and Applications'),          (30, 'az', 'Sənədlər və Müraciətlərlə İş'),
(31, 'en', 'Human Resources'),                     (31, 'az', 'İnsan Resursları'),
(32, 'en', 'Finance and Accountant'),              (32, 'az', 'Maliyyə və Mühasibat'),
(33, 'en', 'Information Technologies'),            (33, 'az', 'İnformasiya Texnologiyaları'),
(34, 'en', 'Communication'),                       (34, 'az', 'Kommunikasiya'),
(35, 'en', 'Mass Media'),                          (35, 'az', 'Mətbuat Xidməti'),
(36, 'en', 'Analytical Analysis'),                 (36, 'az', 'Analitik Təhlil'),
(37, 'en', 'Procurement'),                         (37, 'az', 'Satınalma Təchizat'),
(38, 'en', 'Career and Employability Centre'),     (38, 'az', 'Karyera və Məşğulluq Mərkəzi'),
(39, 'en', 'LifeLong Learning'),                   (39, 'az', 'Ömürboyu Təhsil'),
(40, 'en', 'Technology Transfer Office (TTO)'),    (40, 'az', 'Texnoloji Transfer Ofisi (TTO)'),
(41, 'en', 'Nabran Resort Centre'),                (41, 'az', 'Nabran İstirahət Mərkəzi'),
(42, 'en', 'Sabah Centre'),                        (42, 'az', 'Sabah Mərkəzi'),
(43, 'en', 'Library Information Centre'),          (43, 'az', 'Kitabxana İnformasiya Mərkəzi'),
(44, 'en', '2026-2027 Academic Calendar'),          (44, 'az', '2026-2027 Akademik Təqvim'),
(45, 'en', '2025-2026 Academic Calendar'),          (45, 'az', '2025-2026 Akademik Təqvim'),
(46, 'en', 'Organization of Examinations at AzTU'), (46, 'az', 'Qiymətləndirmə və İmtahanın Təşkili Qaydaları'),
(47, 'en', 'Credit System at Bachelor''s and Master''s Levels'), (47, 'az', 'Kredit Sistemi ilə Tədrisin Təşkili Qaydaları'),
(48, 'en', 'LMS Guidelines'),                       (48, 'az', 'LMS Qaydaları'),
(49, 'en', 'Specialties'),      (49, 'az', 'İxtisaslar'),
(50, 'en', 'Curriculum'),       (50, 'az', 'Tədris Planı'),
(51, 'en', 'Learning Outcomes'),(51, 'az', 'Təhsil Nəticələri'),
(52, 'en', 'Exchange Programs'),(52, 'az', 'Mübadilə Proqramları'),
(53, 'en', 'Tuition Fees'),     (53, 'az', 'Təhsil Haqqı'),
(54, 'en', 'Specialties'),               (54, 'az', 'İxtisaslar'),
(55, 'en', 'Curriculum'),                (55, 'az', 'Tədris Planı'),
(56, 'en', 'CDIO'),                      (56, 'az', 'CDIO'),
(57, 'en', 'International Students Unit'),(57, 'az', 'Beynəlxalq Tələbələr Bölməsi'),
(58, 'en', 'Exchange Programs'),         (58, 'az', 'Mübadilə Proqramları'),
(59, 'en', 'Research Priorities'),          (59, 'az', 'Tədqiqat Prioritetləri'),
(60, 'en', 'Research Institutes'),          (60, 'az', 'Tədqiqat İnstitutları'),
(61, 'en', 'Interdisciplinary Research'),   (61, 'az', 'İnterdissiplinar Tədqiqat'),
(62, 'en', 'Intellectual Property & Patents'),(62, 'az', 'Əqli Mülkiyyət & Patentlər'),
(63, 'en', 'Research Projects'),            (63, 'az', 'Tədqiqat Layihələri'),
(64, 'en', 'Local Conferences'),         (64, 'az', 'Yerli Konfranslar'),
(65, 'en', 'International Conferences'), (65, 'az', 'Beynəlxalq Konfranslar'),
(66, 'en', 'Seminars and Trainings'),    (66, 'az', 'Seminarlar və Təlimlər'),
(67, 'en', 'Lab 1'), (67, 'az', 'Lab 1'),
(68, 'en', 'Machine Science'),                                       (68, 'az', 'Maşınşünaslıq'),
(69, 'en', 'Energy Sustainability: Risks and Decision Making'),      (69, 'az', 'Enerji Davamlılığı: Risklər və Qərarların Qəbulu'),
(70, 'en', 'Scientific Works'),                                      (70, 'az', 'Elmi Əsərlər'),
(71, 'en', 'Journal of Advance Material Processing and Applications'),(71, 'az', 'Journal of Advance Material Processing and Applications'),
(72, 'en', 'Open Access Policy'),          (72, 'az', 'Açıq Giriş Siyasəti'),
(73, 'en', 'Plagiarism & Ethics'),         (73, 'az', 'Plagiat & Etika'),
(74, 'en', 'Ethics & Compliance Guidance'),(74, 'az', 'Etika & Uyğunluq Rəhbərliyi'),
(75, 'en', 'Annual Research Reports'),     (75, 'az', 'İllik Tədqiqat Hesabatları'),
(76, 'en', 'Incentive Mechanism'),    (76, 'az', 'Həvəsləndirmə Mexanizmi'),
(77, 'en', 'Researcher Platforms'),   (77, 'az', 'Tədqiqatçı Platformaları'),
(78, 'en', 'Internal Grant Programs'),(78, 'az', 'Daxili Qrant Proqramları'),
(79, 'en', 'Student Life'),    (79, 'az', 'Tələbə Həyatı'),
(80, 'en', 'Clubs'),           (80, 'az', 'Klublar'),
(81, 'en', 'Sport'),           (81, 'az', 'İdman'),
(82, 'en', 'Cultural Events'), (82, 'az', 'Mədəni Tədbirlər'),
(83, 'en', 'AzTU Polyclinic'), (83, 'az', 'AzTU Poliklinikası'),
(84, 'en', 'Trade Union'),               (84, 'az', 'Həmkarlar İttifaqı'),
(85, 'en', 'Student Trade Union'),       (85, 'az', 'Tələbə Həmkarlar İttifaqı'),
(86, 'en', 'Student Youth Organization'),(86, 'az', 'Tələbə Gənclər Təşkilatı');
