# Faculty Admin Integration

## Endpoints

### Faculty CRUD
- `GET /api/faculty/admin/all` — list all faculties (paginated)
- `GET /api/faculty/{faculty_code}` — get full faculty detail
- `POST /api/faculty/create` — create a faculty
- `PUT /api/faculty/{faculty_code}` — update a faculty
- `DELETE /api/faculty/{faculty_code}` — delete a faculty

### Director profile image upload
- `PUT /api/faculty/{faculty_code}/director/image` — upload director profile photo

### Directions of Action CRUD
- `GET /api/faculty/{faculty_code}/directions-of-action` — list directions (public, accepts `?lang=az|en`)
- `POST /api/faculty/{faculty_code}/directions-of-action` — create a direction
- `PUT /api/faculty/{faculty_code}/directions-of-action/{direction_id}` — update a direction
- `DELETE /api/faculty/{faculty_code}/directions-of-action/{direction_id}` — delete a direction

## Authentication

All write endpoints (`POST`, `PUT`, `DELETE`) require admin authentication.
Include the `Authorization` header with the admin token.

---

## Create / Update Faculty

- **Content-Type:** `application/json`
- The body is fully nested JSON.
- For `PUT`, any section array in the payload replaces all existing items for that section.
- Sending `"director": null` removes the director record.
- `profile_image` in the `director` object is **no longer set via JSON**. Upload it separately using the director image endpoint (see below).

### Create faculty payload example

```json
{
  "az": {
    "title": "Fakultə başlığı",
    "html_content": "<p>Fakultə haqqında mətn</p>"
  },
  "en": {
    "title": "Faculty title",
    "html_content": "<p>Text about faculty</p>"
  },
  "director": {
    "first_name": "Ayaz",
    "last_name": "Məmmədov",
    "father_name": "Əli",
    "scientific_degree": "PhD",
    "scientific_title": "Professor",
    "bio": "<p>Professor Ayaz Məmmədov is the dean of the faculty with expertise in applied research.</p>",
    "email": "dekan@example.com",
    "phone": "+994501234567",
    "room_number": "B-101",
    "working_hours": [
      {"day": "Monday", "time_range": "13:00-15:00"},
      {"day": "Wednesday", "time_range": "14:00-16:00"}
    ],
    "scientific_events": [
      {"event_title": "Conference 2026", "event_description": "National research conference"}
    ],
    "educations": [
      {"degree": "Bachelor", "university": "Baku State University", "start_year": "2000", "end_year": "2004"}
    ]
  },
  "laboratories": [
    {
      "az": {"title": "Laboratoriya 1", "description": "Açıqlama"},
      "en": {"title": "Laboratory 1", "description": "Description"}
    }
  ],
  "research_works": [
    {
      "az": {"title": "Tədqiqat", "description": "Açıqlama"},
      "en": {"title": "Research work", "description": "Description"}
    }
  ],
  "partner_companies": [
    {
      "az": {"title": "Şirkət", "description": "Açıqlama"},
      "en": {"title": "Company", "description": "Description"}
    }
  ],
  "objectives": [
    {
      "az": {"title": "Məqsəd", "description": "Açıqlama"},
      "en": {"title": "Objective", "description": "Description"}
    }
  ],
  "duties": [
    {
      "az": {"title": "Vəzifə", "description": "Açıqlama"},
      "en": {"title": "Duty", "description": "Description"}
    }
  ],
  "projects": [
    {
      "az": {"title": "Layihə", "description": "Açıqlama"},
      "en": {"title": "Project", "description": "Description"}
    }
  ],
  "directions_of_action": [
    {
      "az": {"title": "Fəaliyyət istiqamətləri", "description": "<p>Fakultənin əsas fəaliyyət istiqamətləri.</p>"},
      "en": {"title": "Directions of action", "description": "<p>Main directions of faculty activity.</p>"}
    }
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
      "profile_image": "/static/deputies/aygun.jpg"
    }
  ],
  "scientific_council": [
    {
      "first_name": "Elman",
      "last_name": "Quliyev",
      "father_name": "Kamran",
      "duty": "Member"
    }
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
  ]
}
```

---

## Director profile image upload

Upload an image file for the faculty director. The director record must already exist (create the faculty with a director first, then upload the photo).

- **Method:** `PUT`
- **URL:** `/api/faculty/{faculty_code}/director/image`
- **Content-Type:** `multipart/form-data`
- **Auth:** required

### Form field

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | file | yes | JPEG, PNG, WebP, or GIF. Max size from server config. |

### Success response

```json
{
  "status_code": 200,
  "message": "Director profile image uploaded successfully.",
  "data": {
    "profile_image": "static/directors/abc123def456.jpg"
  }
}
```

The returned `profile_image` path is relative. Prefix with the API base URL or `/` to render it:
```
<img src="/static/directors/abc123def456.jpg" />
```

---

## Directions of Action CRUD

Use these endpoints to manage individual direction-of-action entries independently of the full faculty update.

### Create

**POST** `/api/faculty/{faculty_code}/directions-of-action`

```json
{
  "az": {
    "title": "Elmi tədqiqat istiqaməti",
    "description": "<p>Ətraflı mətn</p>"
  },
  "en": {
    "title": "Scientific research direction",
    "description": "<p>Detailed text</p>"
  }
}
```

Response (`201`):
```json
{
  "status_code": 201,
  "message": "Direction of action created successfully.",
  "data": { "id": 42 }
}
```

### Update

**PUT** `/api/faculty/{faculty_code}/directions-of-action/{direction_id}`

Send only the language blocks you want to update. Both are optional.

```json
{
  "az": { "title": "Yenilənmiş başlıq" },
  "en": { "title": "Updated title", "description": "<p>New text</p>" }
}
```

Response (`200`):
```json
{
  "status_code": 200,
  "message": "Direction of action updated successfully."
}
```

### Delete

**DELETE** `/api/faculty/{faculty_code}/directions-of-action/{direction_id}`

Response (`200`):
```json
{
  "status_code": 200,
  "message": "Direction of action deleted successfully."
}
```

### List (public — no auth required)

**GET** `/api/faculty/{faculty_code}/directions-of-action?lang=az`

Response (`200`):
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

## Notes for admin dashboard

- Use `GET /api/faculty/admin/all` to list faculty entries.
- Use `GET /api/faculty/{faculty_code}` to fetch full detail for editing.
- After creating a faculty with a director, upload the director photo via `PUT /api/faculty/{faculty_code}/director/image`.
- Directions of action can be managed individually via the dedicated CRUD endpoints, or replaced in bulk via the main faculty `PUT` endpoint.
- The `director.bio` field accepts plain text or HTML. Render it as `innerHTML` or use a sanitised HTML renderer.
