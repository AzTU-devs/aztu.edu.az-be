# Menu API Documentation

This document covers all menu-related API endpoints for **AzTU** — both the public read endpoints used by the website and the admin CRUD endpoints used by the dashboard.

---

## Table of Contents

1. [Base URL & Conventions](#1-base-url--conventions)
2. [Language Support](#2-language-support)
3. [Response Envelope](#3-response-envelope)
4. [Website — Public GET Endpoints](#4-website--public-get-endpoints)
   - [GET /api/menu/header](#41-get-apimenuheader)
   - [GET /api/menu/footer](#42-get-apimenufooter)
   - [GET /api/menu/quick](#43-get-apimenquick)
5. [Admin — Header Navigation CRUD](#5-admin--header-navigation-crud)
   - [Sections](#51-sections)
   - [Items](#52-items)
   - [Sub-Items](#53-sub-items)
6. [Admin — Footer CRUD](#6-admin--footer-crud)
   - [Columns](#61-columns)
   - [Links](#62-links)
   - [Partner Logos](#63-partner-logos)
   - [Quick Icons](#64-quick-icons)
7. [Admin — Shared Resources CRUD](#7-admin--shared-resources-crud)
   - [Social Links](#71-social-links)
   - [Contact](#72-contact)
8. [Admin — Quick Menu CRUD](#8-admin--quick-menu-crud)
   - [Left Items](#81-left-items)
   - [Sections](#82-sections)
   - [Section Items](#83-section-items)
9. [Full Endpoint Reference](#9-full-endpoint-reference)
10. [Frontend Integration Guide](#10-frontend-integration-guide)

---

## 1. Base URL & Conventions

```
Base URL: /api/menu
```

- All request bodies are **JSON** (`Content-Type: application/json`)
- All responses are JSON
- CRUD write endpoints (`POST`, `PUT`, `DELETE`) do **not** require the `lang` query parameter
- Read endpoints (`GET`) require `?lang=az` or `?lang=en`

---

## 2. Language Support

All GET endpoints accept a `lang` query parameter:

| Value | Language    |
|-------|-------------|
| `az`  | Azerbaijani |
| `en`  | English     |

Example: `GET /api/menu/header?lang=az`

When creating or updating records, translations are supplied in the request body as an object with `az` and `en` keys:

```json
{
  "title": {
    "az": "Haqqımızda",
    "en": "About"
  }
}
```

---

## 3. Response Envelope

**Success:**
```json
{
  "status_code": 200,
  "data": { ... }
}
```

**Created:**
```json
{
  "status_code": 201,
  "message": "Resource created.",
  "id": 42
}
```

**Not Found:**
```json
{
  "status_code": 404,
  "message": "Section not found."
}
```

**Conflict:**
```json
{
  "status_code": 409,
  "message": "Section key already exists."
}
```

**Server Error:**
```json
{
  "status_code": 500,
  "error": "error details"
}
```

---

## 4. Website — Public GET Endpoints

These three endpoints are called by the website on every page load. They return fully assembled, language-specific data — no post-processing needed on the frontend.

---

### 4.1 GET /api/menu/header

Returns all header navigation sections with their items and sub-items in the requested language.

```
GET /api/menu/header?lang={az|en}
```

**Response:**

```json
{
  "status_code": 200,
  "data": {
    "sections": [
      {
        "key": "about",
        "label": "ABOUT",
        "base_path": "/about",
        "image_url": "https://cdn.aztu.edu.az/images/slide-1.png",
        "items": [
          {
            "title": "History of AzTU",
            "slug": "history",
            "sub_items": []
          },
          {
            "title": "Leadership & Governance",
            "slug": null,
            "sub_items": [
              { "title": "Rector", "slug": "leadership/rector" },
              { "title": "Vice-Rector", "slug": "leadership/vice-rector" }
            ]
          }
        ]
      }
    ]
  }
}
```

**URL construction rules:**

| Case | Formula | Example |
|------|---------|---------|
| Item with slug | `{base_path}/{item.slug}` | `/about/history` |
| Sub-item | `{base_path}/{sub_item.slug}` | `/about/leadership/rector` |
| Item with `slug: null` | not a link — category header only | — |

**TypeScript interface:**

```ts
interface NavSubItem {
  title: string;
  slug: string;
}

interface NavItem {
  title: string;
  slug: string | null;  // null = category header, render sub_items only
  sub_items: NavSubItem[];
}

interface NavSection {
  key: string;
  label: string;
  base_path: string;
  image_url: string;
  items: NavItem[];
}

interface HeaderMenuResponse {
  status_code: number;
  data: { sections: NavSection[] };
}
```

---

### 4.2 GET /api/menu/footer

Returns footer columns with links, contact info, social links, partner logos, and quick icons.

```
GET /api/menu/footer?lang={az|en}
```

**Response:**

```json
{
  "status_code": 200,
  "data": {
    "university_name": "Azerbaijan Technical University",
    "columns": [
      {
        "title": "Haqqımızda",
        "links": [
          { "label": "Universitetin tarixi", "url": "/about/history" },
          { "label": "Kampus", "url": "/about/campus" }
        ]
      }
    ],
    "contact": {
      "email": "aztu@aztu.edu.az",
      "phones": ["(+994 12) 539-13-05", "(+994 12) 538-33-83"],
      "address": "H.Cavid prospekti 25, Bakı, Azərbaycan AZ 1073."
    },
    "social_links": [
      { "platform": "facebook",  "url": "https://facebook.com/aztu" },
      { "platform": "instagram", "url": "https://instagram.com/aztu" },
      { "platform": "linkedin",  "url": "https://linkedin.com/school/aztu" },
      { "platform": "youtube",   "url": "https://youtube.com/aztu" }
    ],
    "partner_logos": [
      {
        "label": "Prezident.az",
        "image_url": "https://cdn.aztu.edu.az/logos/presidentaz.png",
        "url": "https://president.az"
      }
    ],
    "quick_icons": [
      { "label": "E-Library",  "icon": "ImportContacts", "url": "/research/library" },
      { "label": "Rankings",   "icon": "TrendingUp",     "url": "/about/rankings" },
      { "label": "E-Learning", "icon": "School",         "url": "https://lms.aztu.edu.az" }
    ]
  }
}
```

**TypeScript interface:**

```ts
interface FooterLink     { label: string; url: string; }
interface FooterColumn   { title: string; links: FooterLink[]; }
interface SocialLink     { platform: "facebook"|"instagram"|"linkedin"|"youtube"; url: string; }
interface PartnerLogo    { label: string; image_url: string; url: string; }
interface QuickIcon      { label: string; icon: string; url: string; }
interface FooterContact  { email: string; phones: string[]; address: string; }

interface FooterMenuResponse {
  status_code: number;
  data: {
    university_name: string;
    columns: FooterColumn[];
    contact: FooterContact;
    social_links: SocialLink[];
    partner_logos: PartnerLogo[];
    quick_icons: QuickIcon[];
  };
}
```

---

### 4.3 GET /api/menu/quick

Returns quick menu panel content: left shortcut links, contact info, social links, and tabbed right sections.

```
GET /api/menu/quick?lang={az|en}
```

**Response:**

```json
{
  "status_code": 200,
  "data": {
    "title": "AzTU Quick Menu",
    "left_items": [
      { "label": "Ranking",       "url": "/about/rankings" },
      { "label": "Accreditation", "url": "/about/accreditation" },
      { "label": "FAQ",           "url": "/faq" }
    ],
    "contact": {
      "email": "aztu@aztu.edu.az",
      "phones": ["(+994 12) 539-13-05", "(+994 12) 538-33-83"]
    },
    "social_links": [
      { "platform": "facebook",  "url": "https://facebook.com/aztu" },
      { "platform": "instagram", "url": "https://instagram.com/aztu" }
    ],
    "right_sections": [
      {
        "key": "platform",
        "title": "Platform",
        "items": [
          { "label": "LMS",                "url": "https://lms.aztu.edu.az" },
          { "label": "Internal Grant",     "url": "/research/internal-grant" }
        ]
      },
      {
        "key": "alumni",
        "title": "Alumni",
        "items": [
          { "label": "Career",             "url": "/alumni/career" },
          { "label": "Honorary Doctors",   "url": "/about/honorary-doctors" }
        ]
      }
    ]
  }
}
```

**TypeScript interface:**

```ts
interface QuickMenuItem    { label: string; url: string; }
interface QuickMenuSection { key: string; title: string; items: QuickMenuItem[]; }
interface QuickMenuContact { email: string; phones: string[]; }

interface QuickMenuResponse {
  status_code: number;
  data: {
    title: string;
    left_items: QuickMenuItem[];
    contact: QuickMenuContact;
    social_links: SocialLink[];         // same as footer
    right_sections: QuickMenuSection[];
  };
}
```

---

## 5. Admin — Header Navigation CRUD

The header is structured as a 3-level hierarchy:

```
Section  (e.g. "About")
  └── Item  (e.g. "Leadership & Governance")
        └── Sub-Item  (e.g. "Rector")
```

Create in order: **Section → Item → Sub-Item**. Each level requires the parent `id` from the previous create response.

---

### 5.1 Sections

#### Create a section

```
POST /api/menu/header/section
```

**Request body:**

```json
{
  "section_key": "about",
  "image_url": "https://cdn.aztu.edu.az/images/slide-1.png",
  "display_order": 1,
  "label": {
    "az": "HAQQIMIZDA",
    "en": "ABOUT"
  },
  "base_path": {
    "az": "/haqqimizda",
    "en": "/about"
  }
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `section_key` | string | Yes | Unique identifier, lowercase, no spaces (e.g. `about`, `academics`) |
| `image_url` | string | Yes | Full URL to the hero image shown when this section is hovered |
| `display_order` | integer | Yes | Lower number = appears first |
| `label.az` | string | Yes | Navigation label in Azerbaijani |
| `label.en` | string | Yes | Navigation label in English |
| `base_path.az` | string | Yes | URL prefix for Azerbaijani routes |
| `base_path.en` | string | Yes | URL prefix for English routes |

**Response:**
```json
{ "status_code": 201, "message": "Header section created.", "id": 1 }
```

---

#### Update a section

```
PUT /api/menu/header/section/{section_id}
```

All fields are optional — only send what you want to change:

```json
{
  "image_url": "https://cdn.aztu.edu.az/images/new-slide.png",
  "display_order": 2,
  "label": { "en": "ABOUT US" },
  "base_path": { "en": "/about-us" }
}
```

**Response:**
```json
{ "status_code": 200, "message": "Header section updated." }
```

---

#### Delete a section

```
DELETE /api/menu/header/section/{section_id}
```

> **Warning:** Deletes all child items and sub-items automatically (cascade).

**Response:**
```json
{ "status_code": 200, "message": "Header section deleted." }
```

---

### 5.2 Items

Items belong to a section. If `slug` is `null`, the item is rendered as a **category header** (non-clickable) and its `sub_items` are shown beneath it.

#### Create an item

```
POST /api/menu/header/item
```

**Request body:**

```json
{
  "section_id": 1,
  "slug": "history",
  "display_order": 1,
  "title": {
    "az": "AzTU-nun tarixi",
    "en": "History of AzTU"
  }
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `section_id` | integer | Yes | ID returned when creating the parent section |
| `slug` | string\|null | No | Path segment appended to `base_path`. Set to `null` for non-link category headers |
| `display_order` | integer | Yes | Order within the section |
| `title.az` / `title.en` | string | Yes | Displayed label |

**Response:**
```json
{ "status_code": 201, "message": "Header item created.", "id": 10 }
```

---

#### Update an item

```
PUT /api/menu/header/item/{item_id}
```

```json
{
  "slug": "our-history",
  "display_order": 2,
  "title": { "en": "AzTU History" }
}
```

**Response:**
```json
{ "status_code": 200, "message": "Header item updated." }
```

---

#### Delete an item

```
DELETE /api/menu/header/item/{item_id}
```

> **Warning:** Deletes all child sub-items automatically (cascade).

---

### 5.3 Sub-Items

Sub-items always belong to an item. They are always links (no `null` slug).

#### Create a sub-item

```
POST /api/menu/header/sub-item
```

**Request body:**

```json
{
  "item_id": 10,
  "slug": "leadership/rector",
  "display_order": 1,
  "title": {
    "az": "Rektor",
    "en": "Rector"
  }
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `item_id` | integer | Yes | ID returned when creating the parent item |
| `slug` | string | Yes | Full slug appended to `base_path` (e.g. `leadership/rector` → `/about/leadership/rector`) |
| `display_order` | integer | Yes | Order within the item |
| `title.az` / `title.en` | string | Yes | Displayed label |

**Response:**
```json
{ "status_code": 201, "message": "Header sub-item created.", "id": 101 }
```

---

#### Update a sub-item

```
PUT /api/menu/header/sub-item/{sub_item_id}
```

```json
{
  "slug": "rector-office",
  "title": { "az": "Rektor ofisi", "en": "Rector's Office" }
}
```

---

#### Delete a sub-item

```
DELETE /api/menu/header/sub-item/{sub_item_id}
```

---

## 6. Admin — Footer CRUD

The footer has this structure:

```
Columns  (e.g. "About", "Structure", "Research")
  └── Links  (individual nav links per column)

Partner Logos  (independent list)
Quick Icons    (independent list)
```

---

### 6.1 Columns

#### Create a column

```
POST /api/menu/footer/column
```

```json
{
  "display_order": 1,
  "title": {
    "az": "Haqqımızda",
    "en": "About"
  }
}
```

**Response:**
```json
{ "status_code": 201, "message": "Footer column created.", "id": 1 }
```

---

#### Update a column

```
PUT /api/menu/footer/column/{column_id}
```

```json
{
  "display_order": 2,
  "title": { "en": "About Us" }
}
```

---

#### Delete a column

```
DELETE /api/menu/footer/column/{column_id}
```

> **Warning:** Deletes all links within the column (cascade).

---

### 6.2 Links

#### Create a link

```
POST /api/menu/footer/link
```

```json
{
  "column_id": 1,
  "url": "/about/history",
  "display_order": 1,
  "label": {
    "az": "Universitetin tarixi",
    "en": "History of AzTU"
  }
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `column_id` | integer | Yes | ID of the parent footer column |
| `url` | string | Yes | Absolute path or external URL |
| `display_order` | integer | Yes | Order within the column |
| `label.az` / `label.en` | string | Yes | Link label text |

**Response:**
```json
{ "status_code": 201, "message": "Footer link created.", "id": 20 }
```

---

#### Update a link

```
PUT /api/menu/footer/link/{link_id}
```

```json
{
  "url": "/about/our-history",
  "label": { "en": "AzTU History" }
}
```

---

#### Delete a link

```
DELETE /api/menu/footer/link/{link_id}
```

---

### 6.3 Partner Logos

Partner logos are the institution logos displayed at the bottom of the footer. They have no translations (labels are fixed).

#### Create a partner logo

```
POST /api/menu/footer/partner-logo
```

```json
{
  "label": "Prezident.az",
  "image_url": "https://cdn.aztu.edu.az/logos/presidentaz.png",
  "url": "https://president.az",
  "display_order": 1
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `label` | string | Yes | Alt text / accessible name |
| `image_url` | string | Yes | Full URL to the logo image |
| `url` | string | Yes | External link when clicked |
| `display_order` | integer | Yes | Order in the logo row |

**Response:**
```json
{ "status_code": 201, "message": "Partner logo created.", "id": 5 }
```

---

#### Update a partner logo

```
PUT /api/menu/footer/partner-logo/{logo_id}
```

```json
{
  "image_url": "https://cdn.aztu.edu.az/logos/presidentaz-new.png"
}
```

---

#### Delete a partner logo

```
DELETE /api/menu/footer/partner-logo/{logo_id}
```

---

### 6.4 Quick Icons

Quick icons are the 3 shortcut buttons at the top of the footer (E-Library, Rankings, E-Learning). The `icon` field maps to a **Material UI icon name**.

#### Create a quick icon

```
POST /api/menu/footer/quick-icon
```

```json
{
  "icon": "ImportContacts",
  "url": "/research/library",
  "display_order": 1,
  "label": {
    "az": "E-Kitabxana",
    "en": "E-Library"
  }
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `icon` | string | Yes | Material UI icon name (e.g. `ImportContacts`, `TrendingUp`, `School`) |
| `url` | string | Yes | Internal path or external URL |
| `display_order` | integer | Yes | Left-to-right order |
| `label.az` / `label.en` | string | Yes | Icon label shown below the icon |

**Response:**
```json
{ "status_code": 201, "message": "Quick icon created.", "id": 3 }
```

---

#### Update a quick icon

```
PUT /api/menu/footer/quick-icon/{icon_id}
```

```json
{
  "icon": "MenuBook",
  "label": { "en": "Library" }
}
```

---

#### Delete a quick icon

```
DELETE /api/menu/footer/quick-icon/{icon_id}
```

---

## 7. Admin — Shared Resources CRUD

Social links and Contact records are **shared** between the footer and quick menu via the `context` field.

---

### 7.1 Social Links

#### Create a social link

```
POST /api/menu/social-link
```

```json
{
  "platform": "facebook",
  "url": "https://facebook.com/aztu",
  "context": "both",
  "display_order": 1
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `platform` | string | Yes | One of: `facebook`, `instagram`, `linkedin`, `youtube` |
| `url` | string | Yes | Full social media URL |
| `context` | string | Yes | `"footer"` — footer only · `"quick"` — quick menu only · `"both"` — both |
| `display_order` | integer | Yes | Order in the icon row |

**Response:**
```json
{ "status_code": 201, "message": "Social link created.", "id": 1 }
```

---

#### Update a social link

```
PUT /api/menu/social-link/{link_id}
```

```json
{
  "url": "https://facebook.com/aztu.official",
  "context": "both"
}
```

---

#### Delete a social link

```
DELETE /api/menu/social-link/{link_id}
```

---

### 7.2 Contact

There are **two separate contact records** — one for the footer, one for the quick menu. The footer contact includes `address`; the quick menu contact does not.

#### Create a contact

```
POST /api/menu/contact
```

**Footer contact (with address):**

```json
{
  "context": "footer",
  "email": "aztu@aztu.edu.az",
  "phones": [
    "(+994 12) 539-13-05",
    "(+994 12) 538-33-83"
  ],
  "address": {
    "az": "H.Cavid prospekti 25, Bakı, Azərbaycan AZ 1073.",
    "en": "25 H.Javid Avenue, Baku, Azerbaijan AZ 1073."
  }
}
```

**Quick menu contact (no address):**

```json
{
  "context": "quick",
  "email": "aztu@aztu.edu.az",
  "phones": [
    "(+994 12) 539-13-05",
    "(+994 12) 538-33-83"
  ]
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `context` | string | Yes | `"footer"` or `"quick"` |
| `email` | string | Yes | Contact email address |
| `phones` | string[] | Yes | List of phone numbers in display order |
| `address.az` / `address.en` | string | No | Physical address (footer only) |

**Response:**
```json
{ "status_code": 201, "message": "Contact created.", "id": 1 }
```

---

#### Update a contact

```
PUT /api/menu/contact/{contact_id}
```

```json
{
  "email": "info@aztu.edu.az",
  "phones": ["(+994 12) 539-13-05"],
  "address": { "en": "25 H.Javid Ave, Baku, Azerbaijan." }
}
```

> **Note:** When `phones` is included, the **entire phone list is replaced**. To keep existing phones, re-send them all.

---

#### Delete a contact

```
DELETE /api/menu/contact/{contact_id}
```

---

## 8. Admin — Quick Menu CRUD

The quick menu right panel is a list of tabs (sections), each with its own items.

```
Left Items   (shortcut links — independent list)

Right Panel:
  Section  (tab, e.g. "Platform", "Alumni", "Why AzTU?")
    └── Section Item  (link within the tab)
```

---

### 8.1 Left Items

#### Create a left item

```
POST /api/menu/quick/left-item
```

```json
{
  "url": "/about/rankings",
  "display_order": 1,
  "label": {
    "az": "Reytinq",
    "en": "Ranking"
  }
}
```

**Response:**
```json
{ "status_code": 201, "message": "Quick left item created.", "id": 1 }
```

---

#### Update a left item

```
PUT /api/menu/quick/left-item/{item_id}
```

```json
{
  "url": "/rankings",
  "label": { "en": "Rankings" }
}
```

---

#### Delete a left item

```
DELETE /api/menu/quick/left-item/{item_id}
```

---

### 8.2 Sections

Sections are the tabs in the quick menu right panel.

#### Create a section

```
POST /api/menu/quick/section
```

```json
{
  "section_key": "platform",
  "display_order": 1,
  "title": {
    "az": "Platforma",
    "en": "Platform"
  }
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `section_key` | string | Yes | Unique identifier (e.g. `platform`, `alumni`, `why-aztu`) |
| `display_order` | integer | Yes | Tab order (left to right) |
| `title.az` / `title.en` | string | Yes | Tab label |

**Response:**
```json
{ "status_code": 201, "message": "Quick section created.", "id": 1 }
```

---

#### Update a section

```
PUT /api/menu/quick/section/{section_id}
```

```json
{
  "display_order": 2,
  "title": { "en": "Our Platform" }
}
```

---

#### Delete a section

```
DELETE /api/menu/quick/section/{section_id}
```

> **Warning:** Deletes all items inside the section (cascade).

---

### 8.3 Section Items

#### Create a section item

```
POST /api/menu/quick/section-item
```

```json
{
  "section_id": 1,
  "url": "https://lms.aztu.edu.az",
  "display_order": 1,
  "label": {
    "az": "LMS",
    "en": "LMS"
  }
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `section_id` | integer | Yes | ID of the parent quick section |
| `url` | string | Yes | Internal path or external URL |
| `display_order` | integer | Yes | Order within the tab |
| `label.az` / `label.en` | string | Yes | Link label |

**Response:**
```json
{ "status_code": 201, "message": "Quick section item created.", "id": 10 }
```

---

#### Update a section item

```
PUT /api/menu/quick/section-item/{item_id}
```

```json
{
  "url": "https://lms2.aztu.edu.az",
  "label": { "az": "Öyrənmə Sistemi" }
}
```

---

#### Delete a section item

```
DELETE /api/menu/quick/section-item/{item_id}
```

---

## 9. Full Endpoint Reference

### Public (Website)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/menu/header?lang=` | Full header navigation |
| GET | `/api/menu/footer?lang=` | Full footer content |
| GET | `/api/menu/quick?lang=` | Full quick menu content |

### Header Navigation (Admin)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/menu/header/section` | Create section |
| PUT | `/api/menu/header/section/{id}` | Update section |
| DELETE | `/api/menu/header/section/{id}` | Delete section + children |
| POST | `/api/menu/header/item` | Create item |
| PUT | `/api/menu/header/item/{id}` | Update item |
| DELETE | `/api/menu/header/item/{id}` | Delete item + children |
| POST | `/api/menu/header/sub-item` | Create sub-item |
| PUT | `/api/menu/header/sub-item/{id}` | Update sub-item |
| DELETE | `/api/menu/header/sub-item/{id}` | Delete sub-item |

### Footer (Admin)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/menu/footer/column` | Create column |
| PUT | `/api/menu/footer/column/{id}` | Update column |
| DELETE | `/api/menu/footer/column/{id}` | Delete column + links |
| POST | `/api/menu/footer/link` | Create link |
| PUT | `/api/menu/footer/link/{id}` | Update link |
| DELETE | `/api/menu/footer/link/{id}` | Delete link |
| POST | `/api/menu/footer/partner-logo` | Create partner logo |
| PUT | `/api/menu/footer/partner-logo/{id}` | Update partner logo |
| DELETE | `/api/menu/footer/partner-logo/{id}` | Delete partner logo |
| POST | `/api/menu/footer/quick-icon` | Create quick icon |
| PUT | `/api/menu/footer/quick-icon/{id}` | Update quick icon |
| DELETE | `/api/menu/footer/quick-icon/{id}` | Delete quick icon |

### Shared (Admin)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/menu/social-link` | Create social link |
| PUT | `/api/menu/social-link/{id}` | Update social link |
| DELETE | `/api/menu/social-link/{id}` | Delete social link |
| POST | `/api/menu/contact` | Create contact record |
| PUT | `/api/menu/contact/{id}` | Update contact record |
| DELETE | `/api/menu/contact/{id}` | Delete contact record |

### Quick Menu (Admin)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/menu/quick/left-item` | Create left item |
| PUT | `/api/menu/quick/left-item/{id}` | Update left item |
| DELETE | `/api/menu/quick/left-item/{id}` | Delete left item |
| POST | `/api/menu/quick/section` | Create section (tab) |
| PUT | `/api/menu/quick/section/{id}` | Update section |
| DELETE | `/api/menu/quick/section/{id}` | Delete section + items |
| POST | `/api/menu/quick/section-item` | Create section item |
| PUT | `/api/menu/quick/section-item/{id}` | Update section item |
| DELETE | `/api/menu/quick/section-item/{id}` | Delete section item |

---

## 10. Frontend Integration Guide

### Website — fetching menus on page load

Call all three GET endpoints in parallel. Cache the result in state (or a global store like Zustand / Redux) and re-use across pages.

```ts
// services/menuService.ts
const BASE = import.meta.env.VITE_API_URL; // e.g. https://api.aztu.edu.az

export async function fetchHeaderMenu(lang: "az" | "en") {
  const res = await fetch(`${BASE}/api/menu/header?lang=${lang}`);
  const json = await res.json();
  return json.data; // { sections: NavSection[] }
}

export async function fetchFooterMenu(lang: "az" | "en") {
  const res = await fetch(`${BASE}/api/menu/footer?lang=${lang}`);
  const json = await res.json();
  return json.data;
}

export async function fetchQuickMenu(lang: "az" | "en") {
  const res = await fetch(`${BASE}/api/menu/quick?lang=${lang}`);
  const json = await res.json();
  return json.data;
}
```

When the user switches language, re-fetch all three with the new `lang` value.

---

### Admin Dashboard — setup order

When setting up menus from scratch, follow this order to satisfy parent-child relationships:

```
1. POST /api/menu/contact          (context: "footer")
2. POST /api/menu/contact          (context: "quick")
3. POST /api/menu/social-link      (repeat for each platform, context: "both")

4. POST /api/menu/header/section   → save returned id
5. POST /api/menu/header/item      (section_id from step 4) → save returned id
6. POST /api/menu/header/sub-item  (item_id from step 5)

7. POST /api/menu/footer/column    → save returned id
8. POST /api/menu/footer/link      (column_id from step 7)
9. POST /api/menu/footer/partner-logo
10. POST /api/menu/footer/quick-icon

11. POST /api/menu/quick/section   → save returned id
12. POST /api/menu/quick/section-item (section_id from step 11)
13. POST /api/menu/quick/left-item
```

---

### Admin Dashboard — example: adding a new header nav link

Scenario: Add a new page "Campus Map" under the existing "About" section.

**Step 1** — Create the item (no sub-items needed, direct link):
```json
POST /api/menu/header/item
{
  "section_id": 1,
  "slug": "campus-map",
  "display_order": 5,
  "title": { "az": "Kampus xəritəsi", "en": "Campus Map" }
}
```
The frontend will construct the URL as `/about/campus-map`.

---

### Admin Dashboard — example: adding a sub-menu group

Scenario: Add a "Transport" category under "Students" with two sub-links.

**Step 1** — Create the category item (no slug = non-link header):
```json
POST /api/menu/header/item
{
  "section_id": 4,
  "slug": null,
  "display_order": 6,
  "title": { "az": "Nəqliyyat", "en": "Transport" }
}
// Response: { "id": 55 }
```

**Step 2** — Create the first sub-item:
```json
POST /api/menu/header/sub-item
{
  "item_id": 55,
  "slug": "transport/bus",
  "display_order": 1,
  "title": { "az": "Avtobus", "en": "Bus" }
}
```

**Step 3** — Create the second sub-item:
```json
POST /api/menu/header/sub-item
{
  "item_id": 55,
  "slug": "transport/shuttle",
  "display_order": 2,
  "title": { "az": "Şatl", "en": "Shuttle" }
}
```

Result in the nav: clicking "Transport" shows a dropdown with "Bus" (`/students/transport/bus`) and "Shuttle" (`/students/transport/shuttle`).

---

### Admin Dashboard — example: reordering items

`display_order` controls order. To move an item from position 3 to position 1:

```json
PUT /api/menu/header/item/42
{
  "display_order": 1
}
```

Then update all other items that were at positions 1 and 2 to shift them down:

```json
PUT /api/menu/header/item/40   { "display_order": 2 }
PUT /api/menu/header/item/41   { "display_order": 3 }
```

---

### Admin Dashboard — example: updating contact phones

To replace the phone list entirely:

```json
PUT /api/menu/contact/1
{
  "phones": [
    "(+994 12) 539-13-05",
    "(+994 12) 538-33-83",
    "(+994 50) 123-45-67"
  ]
}
```

To remove a phone, send the list without it:

```json
PUT /api/menu/contact/1
{
  "phones": ["(+994 12) 539-13-05"]
}
```

---

### Error handling

All endpoints return a `status_code` in the JSON body. Always check this field in addition to the HTTP status code:

```ts
async function apiCall(url: string, options?: RequestInit) {
  const res = await fetch(url, options);
  const json = await res.json();

  if (json.status_code >= 400) {
    throw new Error(json.message || json.error || "Unknown error");
  }

  return json;
}
```

Common error codes:

| status_code | Meaning | Action |
|-------------|---------|--------|
| 404 | Record not found | Show "not found" message, refresh list |
| 409 | Duplicate key | Prompt user to choose a different `section_key` |
| 422 | Invalid language code | Ensure `lang` is `az` or `en` |
| 500 | Server error | Show generic error, log `error` field |
