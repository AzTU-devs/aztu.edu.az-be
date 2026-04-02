# Department Module — Public Website Frontend Guide

Base URL: `/api/department`  
No authentication required for public endpoints.  
Pass the active locale via `Accept-Language: az` or `Accept-Language: en`.

---

## Pages to Build

### 1. Departments Listing Page

Displays a grid / list of all departments.

**Route (example):** `/departments`

**API call:**
```
GET /api/department/public/all?start=0&end=50
Accept-Language: az
```

**Response:**
```json
{
  "status_code": 200,
  "departments": [
    {
      "id": 1,
      "department_code": "482910",
      "department_name": "İnsan Resursları Şöbəsi",
      "worker_count": 5,
      "created_at": "...",
      "updated_at": "..."
    }
  ],
  "total": 1
}
```

**UI:**
- Each card shows `department_name`.
- Clicking a card navigates to `/departments/:department_code`.

---

### 2. Department Detail Page

**Route (example):** `/departments/:department_code`

**API call:**
```
GET /api/department/:department_code
Accept-Language: az
```

**Full response shape:**
```json
{
  "status_code": 200,
  "department": {
    "id": 1,
    "department_code": "482910",
    "department_name": "İnsan Resursları Şöbəsi",
    "about_html": "<p>Şöbə haqqında...</p>",
    "objectives": [
      { "id": 1, "html_content": "<p>Məqsəd 1</p>" }
    ],
    "core_functions": [
      { "id": 1, "html_content": "<p>Funksiya 1</p>" }
    ],
    "director": {
      "id": 2,
      "first_name": "Əli",
      "last_name": "Həsənov",
      "father_name": "Vüsal",
      "room_number": "1-202",
      "profile_image": "static/department-directors/abc123.jpg",
      "scientific_degree": "f.e.d.",
      "scientific_title": "dosent",
      "bio": "<p>Bio...</p>",
      "working_hours": [
        { "day": "Bazar ertəsi", "time_range": "09:00-13:00" }
      ],
      "educations": [
        { "degree": "Bakalavr", "university": "AzTU", "start_year": "2000", "end_year": "2005" }
      ]
    },
    "workers": [
      {
        "id": 3,
        "first_name": "Nigar",
        "last_name": "Quliyeva",
        "father_name": "Tural",
        "email": "nigar@aztu.edu.az",
        "phone": "+994501234567",
        "profile_image": "static/department-workers/xyz789.png",
        "duty": "Mütəxəssis",
        "scientific_degree": null,
        "scientific_name": null
      }
    ],
    "created_at": "...",
    "updated_at": "..."
  }
}
```

---

## Rendering Guide

### `about_html`

Render directly as HTML inside a container. Apply scoped CSS so the university's typography styles apply to headings, paragraphs, and lists inside this block.

```html
<div class="department-about" v-html="department.about_html" />
```

> Never use `innerHTML` from untrusted sources without sanitization. The backend sanitizes content on the admin side; on the frontend, use a sanitizer like DOMPurify before rendering if extra safety is needed.

---

### Objectives list

Each objective's `html_content` is a standalone HTML fragment (a `<p>`, `<ul>`, or similar). Render them in order as a numbered or bulleted list.

```html
<ol class="objectives-list">
  <li v-for="obj in department.objectives" :key="obj.id" v-html="obj.html_content" />
</ol>
```

---

### Core Functions list

Same pattern as objectives.

```html
<ul class="core-functions-list">
  <li v-for="fn in department.core_functions" :key="fn.id" v-html="fn.html_content" />
</ul>
```

---

### Director section

Only render this section if `department.director` is not `null`.

**Layout suggestion:**

```
┌─────────────────────────────────────────────┐
│  [Photo]   Full Name                        │
│            Scientific Degree · Title        │
│                                             │
│  Bio (rendered as HTML)                     │
│                                             │
│  Working Hours                              │
│  ─────────                                  │
│  Monday   09:00–13:00                       │
│                                             │
│  Education                                  │
│  ─────────                                  │
│  Bachelor — AzTU  (2000–2005)               │
└─────────────────────────────────────────────┘
```

**Profile image URL:**
```js
const imgUrl = `${API_BASE_URL}/${director.profile_image}`
// e.g. https://api.aztu.edu.az/static/department-directors/abc123.jpg
```

If `profile_image` is `null`, show a placeholder avatar.

**Scientific fields:** `scientific_degree` and `scientific_title` may both be `null` (optional on admin side). Only render them when present.

**Room number:** Display as e.g. `Otaq: 1-202`.

---

### Workers list

Render as a card grid. Each card:

| Element | Field |
|---|---|
| Photo | `profile_image` → prepend API base URL; fallback to placeholder |
| Full name | `last_name + " " + first_name + " " + father_name` |
| Position / duty | `duty` |
| Scientific info | `scientific_degree` + `scientific_name` (only if not null) |
| Email | `email` (only if not null) — render as `mailto:` link |
| Phone | `phone` (only if not null) — render as `tel:` link |

---

## Locale Switching

When the user switches language, re-fetch the detail page with the new `Accept-Language` header. All translatable fields (`department_name`, `about_html`, `objectives[*].html_content`, `core_functions[*].html_content`, director bio / scientific fields / working_hours day / education fields, worker duty / scientific fields) will be returned in the new language.

Non-translated fields (names, emails, phones, room numbers, time ranges, years) remain the same regardless of language.

---

## SEO Recommendations

- Set `<title>` to `department_name`.
- Set `<meta name="description">` to the first 160 characters of `about_html` stripped of HTML tags.
- Use `<h1>` for the department name, `<h2>` for section headings (About, Objectives, Core Functions, Director, Staff).

---

## Error States

| Condition | UI |
|---|---|
| `status_code: 204` on list | Show "No departments found." message |
| `status_code: 404` on detail | Show 404 page |
| `status_code: 500` | Show generic error message with retry button |
| `director: null` | Hide the director section entirely |
| `objectives: []` | Hide the objectives section |
| `core_functions: []` | Hide the core functions section |
| `workers: []` | Hide the staff section |
