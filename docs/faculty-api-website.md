# Faculty API — Website (Public) Guide

This document describes the public faculty endpoints and the shape of the data returned. All translatable fields are served in the language requested via the `lang` query parameter (`az` or `en`).

---

## Base URL

```
/api/v1/faculty
```

No authentication required for public endpoints.

---

## Language Selection

Pass `?lang=az` or `?lang=en` on every request. Defaults to `az` if omitted.

---

## Endpoints

### `GET /public/all`

List faculties with pagination.

**Query params:** `start`, `end`, `lang`

**Response:**
```json
{
  "status_code": 200,
  "message": "Faculties fetched successfully.",
  "total": 5,
  "faculties": [
    {
      "id": 1,
      "faculty_code": "123456",
      "title": "Mühəndislik fakültəsi",
      "cafedra_count": 4,
      "deputy_dean_count": 2,
      "created_at": "2025-01-01T00:00:00+00:00",
      "updated_at": "2025-06-01T00:00:00+00:00"
    }
  ]
}
```

---

### `GET /{faculty_code}?lang=az`

Get full faculty details. All translatable fields are returned in the requested language.

**Response:**
```json
{
  "status_code": 200,
  "message": "Faculty details fetched successfully.",
  "faculty": {
    "id": 1,
    "faculty_code": "123456",
    "title": "Mühəndislik fakültəsi",
    "html_content": "<p>...</p>",

    "bachelor_programs_count": 10,
    "master_programs_count": 5,
    "phd_programs_count": 2,
    "international_collaborations_count": 15,
    "laboratories_count": 8,
    "projects_patents_count": 20,
    "industrial_collaborations_count": 12,
    "sdgs": [4, 7, 9, 13],
    "cafedra_count": 4,
    "deputy_dean_count": 2,

    "director": {
      "first_name": "Əli",
      "last_name": "Əliyev",
      "father_name": "Əli oğlu",
      "scientific_degree": "Texnika elmləri doktoru",
      "scientific_title": "Professor",
      "bio": "<p>...</p>",
      "scientific_research_fields": ["Cybersecurity", "AI"],
      "email": "ali@aztu.edu.az",
      "phone": "+994501234567",
      "room_number": "301",
      "profile_image": "static/directors/abc123.jpg",
      "working_hours": [
        { "day": "Bazar ertəsi", "time_range": "09:00-17:00" }
      ],
      "scientific_events": [
        { "event_title": "Konfrans", "event_description": "..." }
      ],
      "educations": [
        {
          "degree": "Bakalavr",
          "university": "AZTU",
          "start_year": "2000",
          "end_year": "2004"
        }
      ]
    },

    "deputy_deans": [
      {
        "id": 1,
        "first_name": "Nigar",
        "last_name": "Həsənova",
        "father_name": "Mübariz qızı",
        "scientific_name": "Dosent",
        "scientific_degree": "Fəlsəfə doktoru",
        "duty": "Tədris işləri üzrə dekan müavini",
        "email": "nigar@aztu.edu.az",
        "phone": "+994501234568",
        "profile_image": "static/deputy-deans/xyz456.jpg"
      }
    ],

    "scientific_council": [
      {
        "id": 1,
        "first_name": "Rauf",
        "last_name": "Quliyev",
        "father_name": "Tofiq oğlu",
        "duty": "Elmi katib",
        "scientific_name": "Dosent",
        "scientific_degree": "Fəlsəfə doktoru",
        "email": "rauf@aztu.edu.az",
        "phone": "+994501234569"
      }
    ],

    "workers": [
      {
        "id": 1,
        "first_name": "Leyla",
        "last_name": "Məmmədova",
        "father_name": "Farid qızı",
        "duty": "Müəllim",
        "scientific_name": "Dosent",
        "scientific_degree": "Fəlsəfə doktoru",
        "email": "leyla@aztu.edu.az",
        "profile_image": "static/faculty-workers/lmn789.jpg"
      }
    ],

    "laboratories": [
      { "id": 1, "title": "Kimya laboratoriyası", "description": "..." }
    ],
    "research_works": [ { "id": 1, "title": "...", "description": "..." } ],
    "partner_companies": [ { "id": 1, "title": "...", "description": "..." } ],
    "objectives": [ { "id": 1, "title": "...", "description": "..." } ],
    "duties": [ { "id": 1, "title": "...", "description": "..." } ],
    "projects": [ { "id": 1, "title": "...", "description": "..." } ],
    "directions_of_action": [ { "id": 1, "title": "...", "description": "..." } ],

    "created_at": "2025-01-01T00:00:00+00:00",
    "updated_at": "2025-06-01T00:00:00+00:00"
  }
}
```

---

### `GET /{faculty_code}/directions-of-action?lang=az`

Get only the directions of action for a faculty.

**Response:**
```json
{
  "status_code": 200,
  "message": "Directions of action fetched successfully.",
  "directions_of_action": [
    { "id": 1, "title": "...", "description": "..." }
  ]
}
```

---

## Field Details

### Statistics
- `bachelor_programs_count`, `master_programs_count`, `phd_programs_count`: Integer counts of academic programs.
- `international_collaborations_count`, `industrial_collaborations_count`: Counts of partnerships.
- `laboratories_count`: Total count of laboratories.
- `projects_patents_count`: Count of projects and patents.
- `sdgs`: Array of Sustainable Development Goal (SDG) numbers (1-17).
- `cafedra_count`: Total number of departments (cafedras) under this faculty.
- `deputy_dean_count`: Number of deputy deans.

### Director
- `scientific_research_fields`: Array of strings representing research areas.
- `working_hours`: List of `{ day, time_range }`. `day` is translated.
- `scientific_events`: List of `{ event_title, event_description }`. Both are translated.
- `educations`: List of `{ degree, university, start_year, end_year }`. `degree` and `university` are translated.

### Personnel (Deputy Deans, Council, Workers)
- `scientific_name`, `scientific_degree`, `duty`: All translated based on `?lang`.
- `profile_image`: Relative path. Prefix with API base domain (e.g., `https://api.aztu.edu.az/`).

---

## Static Assets

Prepend the API base domain to all image paths:
```
https://api.aztu.edu.az/static/directors/abc123.jpg
https://api.aztu.edu.az/static/deputy-deans/xyz456.jpg
https://api.aztu.edu.az/static/faculty-workers/lmn789.jpg
```

---

## Null Safety

All translatable fields and optional sections may return `null` or `[]`. Always handle these cases in the UI.
