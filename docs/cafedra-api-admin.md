# Cafedra API — Admin Panel Guide

This document covers all endpoints and data structures for the cafedra (department/chair) module. Cafedras belong to faculties and follow the same structure: translatable fields use `az`/`en` language blocks, and profile images are uploaded via dedicated endpoints.

---

## Base URL

```
/api/cafedra
```

All write endpoints require the `Authorization: Bearer <token>` header.

---

## Endpoints

### `GET /admin/all`

List all cafedras. Requires auth.

**Query params:** `start` (default 0), `end` (default 10), `faculty_code` (optional filter), `lang` (default `az`)

**Response item fields:** `id`, `faculty_code`, `cafedra_code`, `title`, `deputy_director_count`, `created_at`

---

### `GET /public/all`

Same as admin but no auth required.

---

### `GET /{cafedra_code}`

Get full cafedra details including all sections, personnel, and director.

**Query params:** `lang` (default `az`)

---

### `POST /create`

Create a new cafedra.

**Content-Type:** `application/json`

```json
{
  "faculty_code": "123456",
  "az": { "title": "Kompüter mühəndisliyi kafedrası", "html_content": "<p>...</p>" },
  "en": { "title": "Computer Engineering Department", "html_content": "<p>...</p>" },

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
      "bio": "<p>...</p>",
      "scientific_research_fields": ["AI", "Robotics"]
    },
    "en": {
      "scientific_degree": "Doctor of Technical Sciences",
      "scientific_title": "Professor",
      "bio": "<p>...</p>",
      "scientific_research_fields": ["AI", "Robotics"]
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

  "bachelor_programs_count": 3,
  "master_programs_count": 2,
  "phd_programs_count": 1,
  "international_collaborations_count": 5,
  "laboratories_count": 4,
  "projects_patents_count": 10,
  "industrial_collaborations_count": 7,
  "sdgs": [4, 9],

  "deputy_directors": [
    {
      "first_name": "Nigar",
      "last_name": "Həsənova",
      "father_name": "Mübariz qızı",
      "email": "nigar@aztu.edu.az",
      "phone": "+994501234568",
      "az": {
        "scientific_name": "Dosent",
        "scientific_degree": "Fəlsəfə doktoru",
        "duty": "Tədris işləri üzrə direktor müavini"
      },
      "en": {
        "scientific_name": "Associate Professor",
        "scientific_degree": "PhD",
        "duty": "Deputy Director for Academic Affairs"
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
  "research_works": [
    {
      "az": { "title": "Tədqiqat işi", "description": "..." },
      "en": { "title": "Research Work", "description": "..." }
    }
  ],
  "partner_companies": [
    {
      "az": { "title": "Şirkət adı", "description": "..." },
      "en": { "title": "Company Name", "description": "..." }
    }
  ],
  "objectives": [
    {
      "az": { "title": "Məqsəd", "description": "..." },
      "en": { "title": "Objective", "description": "..." }
    }
  ],
  "duties": [
    {
      "az": { "title": "Vəzifə", "description": "..." },
      "en": { "title": "Duty", "description": "..." }
    }
  ],
  "projects": [
    {
      "az": { "title": "Layihə", "description": "..." },
      "en": { "title": "Project", "description": "..." }
    }
  ],
  "directions_of_action": [
    {
      "az": { "title": "Fəaliyyət istiqaməti", "description": "..." },
      "en": { "title": "Direction of Action", "description": "..." }
    }
  ]
}
```

> All fields except `faculty_code`, `az`, and `en` are optional on create.

---

### `PUT /{cafedra_code}`

Update a cafedra. Same body structure as `POST /create` — all fields optional. Only provided fields are updated. Sections (`laboratories`, `workers`, etc.) are replaced entirely when provided.

---

### `DELETE /{cafedra_code}`

Delete a cafedra and all related data (cascading).

---

## Image Upload Endpoints

### Director Profile Image

```
PUT /{cafedra_code}/director/image
Content-Type: multipart/form-data

Field: image  (file — JPEG, PNG, WebP, GIF)
```

**Response:**
```json
{
  "status_code": 200,
  "message": "Director profile image uploaded successfully.",
  "data": { "profile_image": "static/cafedra-directors/abc123.jpg" }
}
```

**Workflow:**
1. Create or update the cafedra (director is saved without an image).
2. Call this endpoint to attach the image.

---

### Deputy Director Profile Image

```
PUT /deputy-directors/{deputy_director_id}/image
Content-Type: multipart/form-data

Field: image  (file — JPEG, PNG, WebP, GIF)
```

**Response:**
```json
{
  "status_code": 200,
  "message": "Deputy director profile image uploaded successfully.",
  "data": { "profile_image": "static/cafedra-deputy-directors/abc123.jpg" }
}
```

**Workflow:**
1. Create or update the cafedra (deputy directors are saved without images).
2. Fetch the cafedra (`GET /{cafedra_code}`) to get the `id` of each deputy director.
3. Call this endpoint for each deputy director that needs a photo.

---

### Worker Profile Image

```
PUT /workers/{worker_id}/image
Content-Type: multipart/form-data

Field: image  (file — JPEG, PNG, WebP, GIF)
```

**Response:**
```json
{
  "status_code": 200,
  "message": "Worker profile image uploaded successfully.",
  "data": { "profile_image": "static/cafedra-workers/abc123.jpg" }
}
```

---

## Field Reference

### Section Items (laboratories, research_works, partner_companies, objectives, duties, projects, directions_of_action)

All section types use the same structure:

```json
{
  "az": { "title": "...", "description": "..." },
  "en": { "title": "...", "description": "..." }
}
```

### Personnel (deputy_directors, workers)

```json
{
  "first_name": "...",
  "last_name": "...",
  "father_name": "...",
  "email": "...",
  "phone": "...",
  "profile_image": null,
  "az": { "duty": "...", "scientific_name": "...", "scientific_degree": "..." },
  "en": { "duty": "...", "scientific_name": "...", "scientific_degree": "..." }
}
```

### Scientific Council Members

Same as personnel but without `profile_image`. `duty` is required.

### Statistics

| Field | Type | Description |
|---|---|---|
| `bachelor_programs_count` | int | Number of bachelor programs |
| `master_programs_count` | int | Number of master programs |
| `phd_programs_count` | int | Number of PhD programs |
| `international_collaborations_count` | int | International collaboration count |
| `laboratories_count` | int | Number of laboratories |
| `projects_patents_count` | int | Projects and patents count |
| `industrial_collaborations_count` | int | Industrial collaboration count |
| `sdgs` | list[int] | Sustainable Development Goals (1-17) |

---

## File Upload Constraints

- **Allowed types:** JPEG, PNG, WebP, GIF
- **Max size:** configured via `MAX_UPLOAD_SIZE_BYTES` (default 10 MB)
- **Stored at:** `static/cafedra-directors/`, `static/cafedra-deputy-directors/`, `static/cafedra-workers/`
- Files are served at `/static/{subdirectory}/{filename}`
