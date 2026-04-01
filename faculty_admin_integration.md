# Faculty Admin Integration

## Endpoints

- `POST /api/v1/faculty/create`
- `PUT /api/v1/faculty/{faculty_code}`
- `DELETE /api/v1/faculty/{faculty_code}`
- `GET /api/v1/faculty/admin/all`
- `GET /api/v1/faculty/{faculty_code}`

## Authentication

- All admin endpoints require admin authentication.
- Use the existing admin auth flow and include the valid auth token with each request.

## Request format

- Content-Type: `application/json`
- Request body is fully nested JSON.

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
    "profile_image": "/uploads/directors/ayaz.jpg",
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
      "profile_image": "/uploads/deputies/aygun.jpg"
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

## Update faculty

- Use `PUT /api/v1/faculty/{faculty_code}` with the same body shape.
- Any provided section array replaces existing items for that section.
- Providing `director: null` removes the director record.

## Notes for admin dashboard

- Use `GET /api/v1/faculty/admin/all` to list faculty entries.
- Use `GET /api/v1/faculty/{faculty_code}` to fetch detail for editing.
- Use nested arrays for labs, research works, partner companies, objectives, duties, projects, deputy deans, council, and workers.
- The admin UI should let editors fill both `az` and `en` translations for section titles/descriptions.
