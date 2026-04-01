# Faculty Website Integration

## Public endpoints

- `GET /api/faculty/public/all` — list all faculties (paginated)
- `GET /api/faculty/{faculty_code}` — full faculty detail
- `GET /api/faculty/{faculty_code}/directions-of-action` — list directions of action for a faculty

## Language selection

- Use query parameter `?lang=az` or `?lang=en`.
- Or use the `Accept-Language` HTTP header.
- Default language is `en`.

---

## Response structure

### List endpoint

```json
{
  "status_code": 200,
  "message": "Faculties fetched successfully.",
  "total": 5,
  "faculties": [
    {
      "id": 1,
      "faculty_code": "123456",
      "title": "Faculty of Engineering",
      "cafedra_count": 4,
      "deputy_dean_count": 2,
      "created_at": "2025-01-01T00:00:00+00:00",
      "updated_at": "2025-06-01T00:00:00+00:00"
    }
  ]
}
```

### Detail endpoint

```json
{
  "status_code": 200,
  "message": "Faculty details fetched successfully.",
  "faculty": {
    "id": 1,
    "faculty_code": "123456",
    "title": "Faculty of Engineering",
    "html_content": "<p>About the faculty...</p>",
    "director": {
      "first_name": "Ayaz",
      "last_name": "Məmmədov",
      "father_name": "Əli",
      "scientific_degree": "PhD",
      "scientific_title": "Professor",
      "bio": "<p>Professor Ayaz Məmmədov is the dean of the faculty...</p>",
      "email": "dekan@example.com",
      "phone": "+994501234567",
      "room_number": "B-101",
      "profile_image": "static/directors/abc123.jpg",
      "working_hours": [
        {"day": "Monday", "time_range": "13:00-15:00"}
      ],
      "scientific_events": [
        {"event_title": "Conference 2026", "event_description": "National research conference"}
      ],
      "educations": [
        {"degree": "Bachelor", "university": "Baku State University", "start_year": "2000", "end_year": "2004"}
      ]
    },
    "laboratories": [
      {"id": 1, "title": "Laboratory 1", "description": "Description"}
    ],
    "research_works": [...],
    "partner_companies": [...],
    "objectives": [...],
    "duties": [...],
    "projects": [...],
    "directions_of_action": [
      {"id": 42, "title": "Scientific research direction", "description": "<p>Detailed text</p>"}
    ],
    "deputy_deans": [
      {
        "first_name": "Aygün",
        "last_name": "Hüseynova",
        "father_name": "Rəşad",
        "scientific_name": "Associate Professor",
        "scientific_degree": "PhD",
        "email": "aygun@example.com",
        "phone": "+994501112233",
        "duty": "Deputy Dean",
        "profile_image": "static/deputies/aygun.jpg"
      }
    ],
    "scientific_council": [
      {"first_name": "Elman", "last_name": "Quliyev", "father_name": "Kamran", "duty": "Member"}
    ],
    "workers": [
      {
        "first_name": "Nigar",
        "last_name": "İsmayılova",
        "father_name": "Vaqif",
        "duty": "Analyst",
        "scientific_name": "MSc",
        "scientific_degree": "Master",
        "email": "nigar@example.com"
      }
    ],
    "created_at": "2025-01-01T00:00:00+00:00",
    "updated_at": "2025-06-01T00:00:00+00:00"
  }
}
```

### Directions of action standalone endpoint

```http
GET /api/faculty/123456/directions-of-action?lang=az
```

```json
{
  "status_code": 200,
  "message": "Directions of action fetched successfully.",
  "directions_of_action": [
    {
      "id": 42,
      "title": "Elmi tədqiqat istiqaməti",
      "description": "<p>Ətraflı mətn</p>"
    }
  ]
}
```

---

## Example requests

```http
GET /api/faculty/public/all?lang=az
Accept: application/json
```

```http
GET /api/faculty/123456?lang=en
Accept: application/json
```

```http
GET /api/faculty/123456/directions-of-action?lang=az
Accept: application/json
```

---

## Frontend integration notes

### Director section

- Render `director.first_name`, `last_name`, `father_name` as the dean's name.
- `director.scientific_degree` and `director.scientific_title` go in the subtitle line.
- `director.bio` contains rich text (may include HTML). Render with a sanitised HTML renderer or `innerHTML`.
- `director.profile_image` is a relative path — prefix with the API base URL:
  ```
  <img src="https://api.aztu.edu.az/static/directors/abc123.jpg" />
  ```
- Render `director.working_hours` as a table or list of day/time pairs.
- Render `director.scientific_events` and `director.educations` as timeline or list sections.
- All director fields are optional — guard against `null` before rendering.

### Section lists (laboratories, research_works, etc.)

- Each item has `id`, `title`, and `description` (optional).
- Render as cards or bulleted lists depending on section context.

### Directions of action

- Can be fetched inline from the faculty detail response (`faculty.directions_of_action`), or independently from `GET /{faculty_code}/directions-of-action`.
- Use the standalone endpoint if you need to lazy-load or refresh this section independently.

### Personnel sections

- `deputy_deans` — show name, duty, scientific degree, email, phone, and profile image.
- `scientific_council` — show name and duty only.
- `workers` — show name, duty, scientific degree, and email.

### Null safety

Display only fields that exist in the response. All optional sections return an empty array `[]` when not set, not `null`.
