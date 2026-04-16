# Cafedra Complete SQL Schema & API Reference

This document contains all SQL table definitions and API field mappings for the Cafedra module. Use this as the single source of truth for building all admin and website pages.

---

## API Endpoints

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/api/cafedra/admin/all?start=0&end=10&faculty_code=...&lang=az` | List cafedras (admin, auth required) |
| `GET` | `/api/cafedra/public/all?start=0&end=10&faculty_code=...&lang=az` | List cafedras (public) |
| `GET` | `/api/cafedra/{cafedra_code}?lang=az` | Get full cafedra details |
| `POST` | `/api/cafedra/create` | Create cafedra |
| `PUT` | `/api/cafedra/{cafedra_code}` | Update cafedra |
| `DELETE` | `/api/cafedra/{cafedra_code}` | Delete cafedra (cascading) |
| `PUT` | `/api/cafedra/{cafedra_code}/director/image` | Upload director profile image |
| `PUT` | `/api/cafedra/deputy-directors/{deputy_director_id}/image` | Upload deputy director profile image |
| `PUT` | `/api/cafedra/workers/{worker_id}/image` | Upload worker profile image |

---

## API Response Fields (GET Detail)

### List Response (`GET /admin/all` or `/public/all`)
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | int | Internal ID |
| `faculty_code` | string | Parent faculty code |
| `cafedra_code` | string | Unique cafedra identifier |
| `title` | string | Translated cafedra name |
| `deputy_director_count` | int | Number of deputy directors |
| `created_at` | string | ISO datetime |

### Detail Response (`GET /{cafedra_code}`)

#### Main Content
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | int | Internal ID |
| `faculty_code` | string | Parent faculty code |
| `cafedra_code` | string | Unique cafedra identifier |
| `title` | string | Translated cafedra name |
| `html_content` | string | HTML "About" text (translated) |

#### Statistics
| Field | Type | Description |
| :--- | :--- | :--- |
| `bachelor_programs_count` | int | Total bachelor programs |
| `master_programs_count` | int | Total master programs |
| `phd_programs_count` | int | Total PhD programs |
| `international_collaborations_count` | int | International partnerships |
| `laboratories_count` | int | Number of laboratories |
| `projects_patents_count` | int | Projects/patents count |
| `industrial_collaborations_count` | int | Industrial partnerships |
| `sdgs` | int[] | SDG IDs (1-17) |
| `deputy_director_count` | int | Number of deputy directors |

#### Director Object (`director`)
| Field | Type | Description |
| :--- | :--- | :--- |
| `first_name` | string | |
| `last_name` | string | |
| `father_name` | string | |
| `scientific_degree` | string | Translated |
| `scientific_title` | string | Translated |
| `bio` | string | HTML (translated) |
| `scientific_research_fields` | string[] | Research areas |
| `email` | string | |
| `phone` | string | |
| `room_number` | string | |
| `profile_image` | string | Relative path (prepend base URL) |
| `working_hours` | object[] | `[{ "day": "...", "time_range": "..." }]` (day is translated) |
| `scientific_events` | object[] | `[{ "event_title": "...", "event_description": "..." }]` (translated) |
| `educations` | object[] | `[{ "degree": "...", "university": "...", "start_year": "...", "end_year": "..." }]` (translated) |

#### Personnel Arrays: `deputy_directors`, `workers`
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | int | Use for image upload endpoint |
| `first_name` | string | |
| `last_name` | string | |
| `father_name` | string | |
| `duty` | string | Translated |
| `scientific_name` | string | Translated |
| `scientific_degree` | string | Translated |
| `email` | string | |
| `phone` | string | |
| `profile_image` | string | Relative path (only deputy_directors & workers) |

#### Personnel Array: `scientific_council`
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | int | |
| `first_name` | string | |
| `last_name` | string | |
| `father_name` | string | |
| `duty` | string | Translated |
| `scientific_name` | string | Translated |
| `scientific_degree` | string | Translated |
| `email` | string | |
| `phone` | string | |

> No `profile_image` for scientific council members.

#### Section Arrays: `laboratories`, `research_works`, `partner_companies`, `objectives`, `duties`, `projects`, `directions_of_action`
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | int | |
| `title` | string | Translated |
| `description` | string | Translated |

---

## API Request Payloads (POST Create / PUT Update)

### Create Payload (`POST /api/cafedra/create`)
```json
{
  "faculty_code": "123456",
  "az": { "title": "...", "html_content": "<p>...</p>" },
  "en": { "title": "...", "html_content": "<p>...</p>" },

  "director": {
    "first_name": "...", "last_name": "...", "father_name": "...",
    "email": "...", "phone": "...", "room_number": "...",
    "az": {
      "scientific_degree": "...", "scientific_title": "...",
      "bio": "<p>...</p>", "scientific_research_fields": ["..."]
    },
    "en": {
      "scientific_degree": "...", "scientific_title": "...",
      "bio": "<p>...</p>", "scientific_research_fields": ["..."]
    },
    "working_hours": [
      { "az": { "day": "..." }, "en": { "day": "..." }, "time_range": "09:00-17:00" }
    ],
    "scientific_events": [
      { "az": { "event_title": "...", "event_description": "..." }, "en": { "event_title": "...", "event_description": "..." } }
    ],
    "educations": [
      { "az": { "degree": "...", "university": "..." }, "en": { "degree": "...", "university": "..." }, "start_year": "2000", "end_year": "2004" }
    ]
  },

  "bachelor_programs_count": 0,
  "master_programs_count": 0,
  "phd_programs_count": 0,
  "international_collaborations_count": 0,
  "laboratories_count": 0,
  "projects_patents_count": 0,
  "industrial_collaborations_count": 0,
  "sdgs": [4, 9],

  "deputy_directors": [
    {
      "first_name": "...", "last_name": "...", "father_name": "...",
      "email": "...", "phone": "...",
      "az": { "scientific_name": "...", "scientific_degree": "...", "duty": "..." },
      "en": { "scientific_name": "...", "scientific_degree": "...", "duty": "..." }
    }
  ],

  "scientific_council": [
    {
      "first_name": "...", "last_name": "...", "father_name": "...",
      "email": "...", "phone": "...",
      "az": { "duty": "...", "scientific_name": "...", "scientific_degree": "..." },
      "en": { "duty": "...", "scientific_name": "...", "scientific_degree": "..." }
    }
  ],

  "workers": [
    {
      "first_name": "...", "last_name": "...", "father_name": "...",
      "email": "...", "phone": "...",
      "az": { "duty": "...", "scientific_name": "...", "scientific_degree": "..." },
      "en": { "duty": "...", "scientific_name": "...", "scientific_degree": "..." }
    }
  ],

  "laboratories":          [{ "az": { "title": "...", "description": "..." }, "en": { "title": "...", "description": "..." } }],
  "research_works":        [{ "az": { "title": "...", "description": "..." }, "en": { "title": "...", "description": "..." } }],
  "partner_companies":     [{ "az": { "title": "...", "description": "..." }, "en": { "title": "...", "description": "..." } }],
  "objectives":            [{ "az": { "title": "...", "description": "..." }, "en": { "title": "...", "description": "..." } }],
  "duties":                [{ "az": { "title": "...", "description": "..." }, "en": { "title": "...", "description": "..." } }],
  "projects":              [{ "az": { "title": "...", "description": "..." }, "en": { "title": "...", "description": "..." } }],
  "directions_of_action":  [{ "az": { "title": "...", "description": "..." }, "en": { "title": "...", "description": "..." } }]
}
```

> **Update (`PUT`):** Same structure, all fields optional. Only provided fields are updated. Section arrays are fully replaced when provided.

### Image Upload (all endpoints)
```
Content-Type: multipart/form-data
Field: image (JPEG, PNG, WebP, GIF — max 10 MB)
```

---

## SQL Table Definitions

### Core Tables

```sql
CREATE TABLE cafedras (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    cafedra_code VARCHAR(50) UNIQUE NOT NULL,

    -- Statistics
    bachelor_programs_count INT DEFAULT 0,
    master_programs_count INT DEFAULT 0,
    phd_programs_count INT DEFAULT 0,
    international_collaborations_count INT DEFAULT 0,
    laboratories_count INT DEFAULT 0,
    projects_patents_count INT DEFAULT 0,
    industrial_collaborations_count INT DEFAULT 0,
    sdgs JSONB DEFAULT '[]',

    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedras_tr (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    cafedra_name VARCHAR(255) NOT NULL,
    about_text TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (cafedra_code, lang_code)
);
```

### Director Tables

```sql
CREATE TABLE cafedra_directors (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) UNIQUE NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    room_number VARCHAR(50),
    profile_image VARCHAR(1024),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_director_tr (
    id SERIAL PRIMARY KEY,
    director_id INT NOT NULL REFERENCES cafedra_directors(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    scientific_degree VARCHAR(255),
    scientific_title VARCHAR(255),
    bio TEXT,
    scientific_research_fields JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (director_id, lang_code)
);

CREATE TABLE cafedra_director_working_hours (
    id SERIAL PRIMARY KEY,
    director_id INT NOT NULL REFERENCES cafedra_directors(id) ON DELETE CASCADE,
    time_range VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_director_working_hour_tr (
    id SERIAL PRIMARY KEY,
    working_hour_id INT NOT NULL REFERENCES cafedra_director_working_hours(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    day VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (working_hour_id, lang_code)
);

CREATE TABLE cafedra_director_scientific_events (
    id SERIAL PRIMARY KEY,
    director_id INT NOT NULL REFERENCES cafedra_directors(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_director_scientific_event_tr (
    id SERIAL PRIMARY KEY,
    scientific_event_id INT NOT NULL REFERENCES cafedra_director_scientific_events(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    event_title VARCHAR(255) NOT NULL,
    event_description TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (scientific_event_id, lang_code)
);

CREATE TABLE cafedra_director_educations (
    id SERIAL PRIMARY KEY,
    director_id INT NOT NULL REFERENCES cafedra_directors(id) ON DELETE CASCADE,
    start_year VARCHAR(20),
    end_year VARCHAR(20),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_director_education_tr (
    id SERIAL PRIMARY KEY,
    education_id INT NOT NULL REFERENCES cafedra_director_educations(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    degree VARCHAR(255) NOT NULL,
    university VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (education_id, lang_code)
);
```

### Personnel Tables

```sql
CREATE TABLE cafedra_deputy_directors (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    profile_image VARCHAR(1024),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_deputy_director_tr (
    id SERIAL PRIMARY KEY,
    deputy_director_id INT NOT NULL REFERENCES cafedra_deputy_directors(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    scientific_name VARCHAR(255),
    scientific_degree VARCHAR(255),
    duty VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (deputy_director_id, lang_code)
);

CREATE TABLE cafedra_scientific_council (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_council_member_tr (
    id SERIAL PRIMARY KEY,
    council_member_id INT NOT NULL REFERENCES cafedra_scientific_council(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    duty VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255),
    scientific_degree VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (council_member_id, lang_code)
);

CREATE TABLE cafedra_workers (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    profile_image VARCHAR(1024),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_worker_tr (
    id SERIAL PRIMARY KEY,
    worker_id INT NOT NULL REFERENCES cafedra_workers(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    duty VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255),
    scientific_degree VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (worker_id, lang_code)
);
```

### Section Tables

```sql
CREATE TABLE cafedra_laboratories (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_laboratory_tr (
    id SERIAL PRIMARY KEY,
    laboratory_id INT NOT NULL REFERENCES cafedra_laboratories(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (laboratory_id, lang_code)
);

CREATE TABLE cafedra_research_works (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_research_work_tr (
    id SERIAL PRIMARY KEY,
    research_work_id INT NOT NULL REFERENCES cafedra_research_works(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (research_work_id, lang_code)
);

CREATE TABLE cafedra_partner_companies (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_partner_company_tr (
    id SERIAL PRIMARY KEY,
    partner_company_id INT NOT NULL REFERENCES cafedra_partner_companies(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (partner_company_id, lang_code)
);

CREATE TABLE cafedra_objectives (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_objective_tr (
    id SERIAL PRIMARY KEY,
    objective_id INT NOT NULL REFERENCES cafedra_objectives(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (objective_id, lang_code)
);

CREATE TABLE cafedra_duties (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_duty_tr (
    id SERIAL PRIMARY KEY,
    duty_id INT NOT NULL REFERENCES cafedra_duties(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (duty_id, lang_code)
);

CREATE TABLE cafedra_projects (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_project_tr (
    id SERIAL PRIMARY KEY,
    project_id INT NOT NULL REFERENCES cafedra_projects(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (project_id, lang_code)
);

CREATE TABLE cafedra_directions_of_action (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_direction_of_action_tr (
    id SERIAL PRIMARY KEY,
    direction_of_action_id INT NOT NULL REFERENCES cafedra_directions_of_action(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (direction_of_action_id, lang_code)
);
```

---

## Table Summary

| # | Table | Type | Parent FK |
| :--- | :--- | :--- | :--- |
| 1 | `cafedras` | Core | `faculties.faculty_code` |
| 2 | `cafedras_tr` | Translation | `cafedras.cafedra_code` |
| 3 | `cafedra_directors` | Director | `cafedras.cafedra_code` |
| 4 | `cafedra_director_tr` | Translation | `cafedra_directors.id` |
| 5 | `cafedra_director_working_hours` | Director relation | `cafedra_directors.id` |
| 6 | `cafedra_director_working_hour_tr` | Translation | `cafedra_director_working_hours.id` |
| 7 | `cafedra_director_scientific_events` | Director relation | `cafedra_directors.id` |
| 8 | `cafedra_director_scientific_event_tr` | Translation | `cafedra_director_scientific_events.id` |
| 9 | `cafedra_director_educations` | Director relation | `cafedra_directors.id` |
| 10 | `cafedra_director_education_tr` | Translation | `cafedra_director_educations.id` |
| 11 | `cafedra_deputy_directors` | Personnel | `cafedras.cafedra_code` |
| 12 | `cafedra_deputy_director_tr` | Translation | `cafedra_deputy_directors.id` |
| 13 | `cafedra_scientific_council` | Personnel | `cafedras.cafedra_code` |
| 14 | `cafedra_council_member_tr` | Translation | `cafedra_scientific_council.id` |
| 15 | `cafedra_workers` | Personnel | `cafedras.cafedra_code` |
| 16 | `cafedra_worker_tr` | Translation | `cafedra_workers.id` |
| 17 | `cafedra_laboratories` | Section | `cafedras.cafedra_code` |
| 18 | `cafedra_laboratory_tr` | Translation | `cafedra_laboratories.id` |
| 19 | `cafedra_research_works` | Section | `cafedras.cafedra_code` |
| 20 | `cafedra_research_work_tr` | Translation | `cafedra_research_works.id` |
| 21 | `cafedra_partner_companies` | Section | `cafedras.cafedra_code` |
| 22 | `cafedra_partner_company_tr` | Translation | `cafedra_partner_companies.id` |
| 23 | `cafedra_objectives` | Section | `cafedras.cafedra_code` |
| 24 | `cafedra_objective_tr` | Translation | `cafedra_objectives.id` |
| 25 | `cafedra_duties` | Section | `cafedras.cafedra_code` |
| 26 | `cafedra_duty_tr` | Translation | `cafedra_duties.id` |
| 27 | `cafedra_projects` | Section | `cafedras.cafedra_code` |
| 28 | `cafedra_project_tr` | Translation | `cafedra_projects.id` |
| 29 | `cafedra_directions_of_action` | Section | `cafedras.cafedra_code` |
| 30 | `cafedra_direction_of_action_tr` | Translation | `cafedra_directions_of_action.id` |

---

## Notes
- All `ON DELETE CASCADE` — deleting a cafedra removes all related data.
- All translatable content uses `lang_code` (`az`, `en`).
- Image fields store relative paths. Prepend API base URL (e.g. `https://api.aztu.edu.az/`) for display.
- `profile_image` is uploaded separately via image endpoints after entity creation.
- `sdgs` accepts integers 1-17 only.
- Section arrays on update are fully replaced (delete all + re-create).
