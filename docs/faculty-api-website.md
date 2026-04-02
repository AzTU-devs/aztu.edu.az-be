# Faculty API — Website (Public) Guide

This document describes the public faculty endpoints and the shape of the data returned after the translation refactor. All translatable fields are now served in the language requested via the `lang` query parameter (`az` or `en`).

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

    "director": {
      "first_name": "Əli",
      "last_name": "Əliyev",
      "father_name": "Əli oğlu",
      "scientific_degree": "Texnika elmləri doktoru",
      "scientific_title": "Professor",
      "bio": "<p>...</p>",
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
        "first_name": "Rauf",
        "last_name": "Quliyev",
        "father_name": "Tofiq oğlu",
        "duty": "Elmi katib"
      }
    ],

    "workers": [
      {
        "first_name": "Leyla",
        "last_name": "Məmmədova",
        "father_name": "Farid qızı",
        "duty": "Müəllim",
        "scientific_name": "Dosent",
        "scientific_degree": "Fəlsəfə doktoru",
        "email": "leyla@aztu.edu.az"
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

## What Changed From the Previous Version

### Director fields

Previously `scientific_degree`, `scientific_title`, and `bio` were always returned in a single fixed language. Now they reflect the `?lang` parameter.

### Working hours

Previously `day` was a fixed string (e.g., always in Azerbaijani). Now it reflects the `?lang` parameter — pass `?lang=en` to receive `"Monday"`, `?lang=az` to receive `"Bazar ertəsi"`.

### Scientific events

`event_title` and `event_description` are now translated per `?lang`.

### Educations

`degree` and `university` are now translated per `?lang`.

### Deputy deans

`scientific_name`, `scientific_degree`, and `duty` are now translated per `?lang`.

### Scientific council members

`duty` is now translated per `?lang`.

### Workers

`duty`, `scientific_name`, and `scientific_degree` are now translated per `?lang`.

### Profile images

`profile_image` values are relative paths — prepend the API base domain to get the full URL:

```
https://api.aztu.edu.az/static/directors/abc123.jpg
https://api.aztu.edu.az/static/deputy-deans/xyz456.jpg
```

If `profile_image` is `null`, render a placeholder.

---

## Null Safety

All translatable fields (`scientific_degree`, `duty`, `bio`, `day`, etc.) may be `null` if no translation exists for the requested language. Always handle `null` gracefully in the UI.
