# Faculty API — Admin Panel Guide

This document covers all breaking changes and new patterns introduced in the faculty module refactor. All translatable fields now require `az`/`en` language blocks, and profile images are uploaded via dedicated endpoints instead of URL strings.

---

## Base URL

```
/api/v1/faculty
```

All write endpoints require the `Authorization: Bearer <token>` header.

---

## Breaking Changes Summary

| Entity | Old field | Change |
|---|---|---|
| Director | `scientific_degree`, `scientific_title`, `bio` | Moved to `az`/`en` blocks |
| Director working hours | `day` | Moved to `az`/`en` blocks (per-language day name) |
| Director scientific events | `event_title`, `event_description` | Moved to `az`/`en` blocks |
| Director educations | `degree`, `university` | Moved to `az`/`en` blocks |
| Deputy Dean | `scientific_name`, `scientific_degree`, `duty` | Moved to `az`/`en` blocks |
| Deputy Dean | `profile_image` (URL string) | Removed — use `PUT /deputy-deans/{id}/image` |
| Scientific Council Member | `duty` | Moved to `az`/`en` blocks |
| Worker | `duty`, `scientific_name`, `scientific_degree` | Moved to `az`/`en` blocks |

---

## Endpoints

### `GET /admin/all`

List all faculties. Requires auth.

**Query params:** `start` (default 0), `end` (default 10), `lang` (default `az`)

---

### `POST /create`

Create a new faculty.

**Content-Type:** `application/json`

```json
{
  "az": { "title": "Mühəndislik fakültəsi", "html_content": "<p>...</p>" },
  "en": { "title": "Engineering Faculty", "html_content": "<p>...</p>" },

  "director": {
    "first_name": "Əli",
    "last_name": "Əliyev",
    "father_name": "Əli oğlu",
    "email": "ali@aztu.edu.az",
    "phone": "+994501234567",
    "room_number": "301",
    "az": {
      "scientific_degree": "Texnika elmləri doktoru",
      "scientific_title": "Professor",
      "bio": "<p>...</p>"
    },
    "en": {
      "scientific_degree": "Doctor of Technical Sciences",
      "scientific_title": "Professor",
      "bio": "<p>...</p>"
    },
    "working_hours": [
      {
        "az": { "day": "Bazar ertəsi" },
        "en": { "day": "Monday" },
        "time_range": "09:00-17:00"
      }
    ],
    "scientific_events": [
      {
        "az": { "event_title": "Konfrans", "event_description": "..." },
        "en": { "event_title": "Conference", "event_description": "..." }
      }
    ],
    "educations": [
      {
        "az": { "degree": "Bakalavr", "university": "AZTU" },
        "en": { "degree": "Bachelor", "university": "AZTU" },
        "start_year": "2000",
        "end_year": "2004"
      }
    ]
  },

  "deputy_deans": [
    {
      "first_name": "Nigar",
      "last_name": "Həsənova",
      "father_name": "Mübariz qızı",
      "email": "nigar@aztu.edu.az",
      "phone": "+994501234568",
      "az": {
        "scientific_name": "Dosent",
        "scientific_degree": "Fəlsəfə doktoru",
        "duty": "Tədris işləri üzrə dekan müavini"
      },
      "en": {
        "scientific_name": "Associate Professor",
        "scientific_degree": "PhD",
        "duty": "Vice Dean for Academic Affairs"
      }
    }
  ],

  "scientific_council": [
    {
      "first_name": "Rauf",
      "last_name": "Quliyev",
      "father_name": "Tofiq oğlu",
      "az": { "duty": "Elmi katib" },
      "en": { "duty": "Scientific Secretary" }
    }
  ],

  "workers": [
    {
      "first_name": "Leyla",
      "last_name": "Məmmədova",
      "father_name": "Farid qızı",
      "email": "leyla@aztu.edu.az",
      "az": { "duty": "Müəllim", "scientific_name": "Dosent", "scientific_degree": "Fəlsəfə doktoru" },
      "en": { "duty": "Lecturer", "scientific_name": "Associate Professor", "scientific_degree": "PhD" }
    }
  ],

  "laboratories": [
    {
      "az": { "title": "Kimya laboratoriyası", "description": "..." },
      "en": { "title": "Chemistry Laboratory", "description": "..." }
    }
  ],

  "research_works": [ ... ],
  "partner_companies": [ ... ],
  "objectives": [ ... ],
  "duties": [ ... ],
  "projects": [ ... ],
  "directions_of_action": [ ... ]
}
```

> `title` and `description` fields inside section items (`laboratories`, `research_works`, etc.) remain the same structure as before.

---

### `PUT /{faculty_code}`

Update a faculty. Same body structure as `POST /create` — all fields optional.

---

### `DELETE /{faculty_code}`

Delete a faculty and all related data.

---

## Image Upload Endpoints

### Director Profile Image

```
PUT /{faculty_code}/director/image
Content-Type: multipart/form-data

Field: image  (file — JPEG, PNG, WebP, GIF)
```

**Response:**
```json
{
  "status_code": 200,
  "message": "Director profile image uploaded successfully.",
  "data": { "profile_image": "static/directors/abc123.jpg" }
}
```

**Workflow:**
1. Create or update the faculty (director is saved without an image).
2. Call this endpoint to attach the image.

---

### Deputy Dean Profile Image

```
PUT /deputy-deans/{deputy_dean_id}/image
Content-Type: multipart/form-data

Field: image  (file — JPEG, PNG, WebP, GIF)
```

**Response:**
```json
{
  "status_code": 200,
  "message": "Deputy dean profile image uploaded successfully.",
  "data": { "profile_image": "static/deputy-deans/abc123.jpg" }
}
```

**Workflow:**
1. Create or update the faculty (deputy deans are saved without images).
2. Fetch the faculty (`GET /{faculty_code}`) to get the `id` of each deputy dean.
3. Call this endpoint for each deputy dean that needs a photo.

---

## Directions of Action (standalone CRUD)

These endpoints allow managing directions of action independently of the full faculty update.

| Method | Path | Description |
|---|---|---|
| `GET` | `/{faculty_code}/directions-of-action` | List (lang-filtered) |
| `POST` | `/{faculty_code}/directions-of-action` | Create |
| `PUT` | `/{faculty_code}/directions-of-action/{id}` | Update |
| `DELETE` | `/{faculty_code}/directions-of-action/{id}` | Delete |

**Create/Update body:**
```json
{
  "az": { "title": "...", "description": "..." },
  "en": { "title": "...", "description": "..." }
}
```

---

## File Upload Constraints

- **Allowed types:** JPEG, PNG, WebP, GIF
- **Max size:** configured via `MAX_UPLOAD_SIZE_BYTES` (default 10 MB)
- **Stored at:** `static/directors/` or `static/deputy-deans/`
- Files are served at `/static/{subdirectory}/{filename}`
