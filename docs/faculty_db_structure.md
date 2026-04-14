# Faculty Module — Database Structure

## Overview

The faculty module uses a **translation pattern**: locale-agnostic data lives in a base table, and all translatable text lives in a paired `_tr` table keyed by `lang_code`. Most child tables reference `faculties.faculty_code` (natural key) via `CASCADE DELETE`.

---

## Tables

### `faculties`
Root table for a faculty.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | Integer | PK, indexed | |
| `faculty_code` | String(50) | UNIQUE, NOT NULL | Natural key used by all child tables |
| `bachelor_programs_count` | Integer | default 0 | |
| `master_programs_count` | Integer | default 0 | |
| `phd_programs_count` | Integer | default 0 | |
| `international_collaborations_count` | Integer | default 0 | |
| `laboratories_count` | Integer | default 0 | |
| `projects_patents_count` | Integer | default 0 | |
| `industrial_collaborations_count` | Integer | default 0 | |
| `sdgs` | JSON | default `[]` | Sustainable Development Goals |
| `created_at` | DateTime(tz) | NOT NULL | |
| `updated_at` | DateTime(tz) | | |

**Relationships (one-to-many unless noted):**
- `cafedras` → `Cafedra`
- `director` → `FacultyDirector` (one-to-one)
- `laboratories` → `FacultyLaboratory`
- `research_works` → `FacultyResearchWork`
- `partner_companies` → `FacultyPartnerCompany`
- `objectives` → `FacultyObjective`
- `duties` → `FacultyDuty`
- `projects` → `FacultyProject`
- `directions_of_action` → `FacultyDirectionOfAction`
- `deputy_deans` → `FacultyDeputyDean`
- `scientific_council` → `FacultyCouncilMember`
- `workers` → `FacultyWorker`

---

### `faculties_tr`
Translatable content for a faculty.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | Integer | PK, indexed | |
| `faculty_code` | String(50) | NOT NULL | FK → `faculties.faculty_code` (logical, no explicit FK defined) |
| `lang_code` | String(10) | NOT NULL | |
| `faculty_name` | String(255) | NOT NULL | |
| `about_text` | Text | | |
| `created_at` | DateTime(tz) | NOT NULL | |
| `updated_at` | DateTime(tz) | | |

**Unique constraint:** `(faculty_code, lang_code)`

---

## Director

### `faculty_directors`
One director per faculty (one-to-one).

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | Integer | PK, indexed | |
| `faculty_code` | String(50) | NOT NULL, FK → `faculties.faculty_code` CASCADE | UNIQUE |
| `first_name` | String(100) | NOT NULL | |
| `last_name` | String(100) | NOT NULL | |
| `father_name` | String(100) | | |
| `email` | String(255) | | |
| `phone` | String(50) | | |
| `room_number` | String(50) | | |
| `profile_image` | String(1024) | | |
| `created_at` | DateTime(tz) | NOT NULL | |
| `updated_at` | DateTime(tz) | | |

**Unique constraint:** `(faculty_code)`

**Relationships:** `translations`, `working_hours`, `scientific_events`, `educations`

---

### `faculty_director_tr`
Translatable content for the director.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | Integer | PK, indexed | |
| `director_id` | Integer | NOT NULL, FK → `faculty_directors.id` CASCADE | |
| `lang_code` | String(10) | NOT NULL | |
| `scientific_degree` | String(255) | | |
| `scientific_title` | String(255) | | |
| `bio` | Text | | |
| `scientific_research_fields` | JSON | default `[]` | |
| `created_at` | DateTime(tz) | NOT NULL | |
| `updated_at` | DateTime(tz) | | |

**Unique constraint:** `(director_id, lang_code)`

---

### `faculty_director_working_hours`

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | Integer | PK, indexed | |
| `director_id` | Integer | NOT NULL, FK → `faculty_directors.id` CASCADE | |
| `time_range` | String(50) | NOT NULL | e.g. `"09:00-12:00"` |
| `created_at` | DateTime(tz) | NOT NULL | |
| `updated_at` | DateTime(tz) | | |

**Relationships:** `translations`

---

### `faculty_director_working_hour_tr`

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | Integer | PK, indexed | |
| `working_hour_id` | Integer | NOT NULL, FK → `faculty_director_working_hours.id` CASCADE | |
| `lang_code` | String(10) | NOT NULL | |
| `day` | String(50) | NOT NULL | Translated day name |
| `created_at` | DateTime(tz) | NOT NULL | |
| `updated_at` | DateTime(tz) | | |

**Unique constraint:** `(working_hour_id, lang_code)`

---

### `faculty_director_scientific_events`

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | Integer | PK, indexed | |
| `director_id` | Integer | NOT NULL, FK → `faculty_directors.id` CASCADE | |
| `created_at` | DateTime(tz) | NOT NULL | |
| `updated_at` | DateTime(tz) | | |

**Relationships:** `translations`

---

### `faculty_director_scientific_event_tr`

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | Integer | PK, indexed | |
| `scientific_event_id` | Integer | NOT NULL, FK → `faculty_director_scientific_events.id` CASCADE | |
| `lang_code` | String(10) | NOT NULL | |
| `event_title` | String(255) | NOT NULL | |
| `event_description` | Text | | |
| `created_at` | DateTime(tz) | NOT NULL | |
| `updated_at` | DateTime(tz) | | |

**Unique constraint:** `(scientific_event_id, lang_code)`

---

### `faculty_director_educations`

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | Integer | PK, indexed | |
| `director_id` | Integer | NOT NULL, FK → `faculty_directors.id` CASCADE | |
| `start_year` | String(20) | | |
| `end_year` | String(20) | | |
| `created_at` | DateTime(tz) | NOT NULL | |
| `updated_at` | DateTime(tz) | | |

**Relationships:** `translations`

---

### `faculty_director_education_tr`

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | Integer | PK, indexed | |
| `education_id` | Integer | NOT NULL, FK → `faculty_director_educations.id` CASCADE | |
| `lang_code` | String(10) | NOT NULL | |
| `degree` | String(255) | NOT NULL | |
| `university` | String(255) | NOT NULL | |
| `created_at` | DateTime(tz) | NOT NULL | |
| `updated_at` | DateTime(tz) | | |

**Unique constraint:** `(education_id, lang_code)`

---

## Sections (translatable list items)

All section tables follow the same pattern:
- Base table holds `faculty_code` FK and `display_order`
- `_tr` table holds translatable `title` + `description`
- Unique constraint on `(parent_id, lang_code)`

### `faculty_laboratories` / `faculty_laboratory_tr`

**Base:**

| Column | Type | Constraints |
|---|---|---|
| `id` | Integer | PK |
| `faculty_code` | String(50) | NOT NULL, FK → `faculties.faculty_code` CASCADE |
| `display_order` | Integer | NOT NULL, default 0 |
| `created_at` | DateTime(tz) | NOT NULL |
| `updated_at` | DateTime(tz) | |

**Translation:**

| Column | Type | Constraints |
|---|---|---|
| `id` | Integer | PK |
| `laboratory_id` | Integer | NOT NULL, FK → `faculty_laboratories.id` CASCADE |
| `lang_code` | String(10) | NOT NULL |
| `title` | String(255) | NOT NULL |
| `description` | Text | |
| `created_at` | DateTime(tz) | NOT NULL |
| `updated_at` | DateTime(tz) | |

---

### `faculty_research_works` / `faculty_research_work_tr`

Same structure as laboratories. FK column: `research_work_id`.

---

### `faculty_partner_companies` / `faculty_partner_company_tr`

Same structure as laboratories. FK column: `partner_company_id`.

---

### `faculty_objectives` / `faculty_objective_tr`

Same structure as laboratories. FK column: `objective_id`.

---

### `faculty_duties` / `faculty_duty_tr`

Same structure as laboratories. FK column: `duty_id`.

---

### `faculty_projects` / `faculty_project_tr`

Same structure as laboratories. FK column: `project_id`.

---

### `faculty_directions_of_action` / `faculty_direction_of_action_tr`

Same structure as laboratories. FK column: `direction_of_action_id`.

---

## Personnel

### `faculty_deputy_deans`

| Column | Type | Constraints |
|---|---|---|
| `id` | Integer | PK |
| `faculty_code` | String(50) | NOT NULL, FK → `faculties.faculty_code` CASCADE |
| `first_name` | String(100) | NOT NULL |
| `last_name` | String(100) | NOT NULL |
| `father_name` | String(100) | |
| `email` | String(255) | |
| `phone` | String(50) | |
| `profile_image` | String(1024) | |
| `created_at` | DateTime(tz) | NOT NULL |
| `updated_at` | DateTime(tz) | |

**Relationships:** `translations`

---

### `faculty_deputy_dean_tr`

| Column | Type | Constraints |
|---|---|---|
| `id` | Integer | PK |
| `deputy_dean_id` | Integer | NOT NULL, FK → `faculty_deputy_deans.id` CASCADE |
| `lang_code` | String(10) | NOT NULL |
| `scientific_name` | String(255) | |
| `scientific_degree` | String(255) | |
| `duty` | String(255) | |
| `created_at` | DateTime(tz) | NOT NULL |
| `updated_at` | DateTime(tz) | |

**Unique constraint:** `(deputy_dean_id, lang_code)`

---

### `faculty_scientific_council`

| Column | Type | Constraints |
|---|---|---|
| `id` | Integer | PK |
| `faculty_code` | String(50) | NOT NULL, FK → `faculties.faculty_code` CASCADE |
| `first_name` | String(100) | NOT NULL |
| `last_name` | String(100) | NOT NULL |
| `father_name` | String(100) | |
| `email` | String(255) | |
| `phone` | String(50) | |
| `created_at` | DateTime(tz) | NOT NULL |
| `updated_at` | DateTime(tz) | |

**Relationships:** `translations`

---

### `faculty_council_member_tr`

| Column | Type | Constraints |
|---|---|---|
| `id` | Integer | PK |
| `council_member_id` | Integer | NOT NULL, FK → `faculty_scientific_council.id` CASCADE |
| `lang_code` | String(10) | NOT NULL |
| `duty` | String(255) | NOT NULL |
| `scientific_name` | String(255) | |
| `scientific_degree` | String(255) | |
| `created_at` | DateTime(tz) | NOT NULL |
| `updated_at` | DateTime(tz) | |

**Unique constraint:** `(council_member_id, lang_code)`

---

### `faculty_workers`

| Column | Type | Constraints |
|---|---|---|
| `id` | Integer | PK |
| `faculty_code` | String(50) | NOT NULL, FK → `faculties.faculty_code` CASCADE |
| `first_name` | String(100) | NOT NULL |
| `last_name` | String(100) | NOT NULL |
| `father_name` | String(100) | |
| `email` | String(255) | |
| `phone` | String(50) | |
| `profile_image` | String(1024) | |
| `created_at` | DateTime(tz) | NOT NULL |
| `updated_at` | DateTime(tz) | |

**Relationships:** `translations`

---

### `faculty_worker_tr`

| Column | Type | Constraints |
|---|---|---|
| `id` | Integer | PK |
| `worker_id` | Integer | NOT NULL, FK → `faculty_workers.id` CASCADE |
| `lang_code` | String(10) | NOT NULL |
| `duty` | String(255) | NOT NULL |
| `scientific_name` | String(255) | |
| `scientific_degree` | String(255) | |
| `created_at` | DateTime(tz) | NOT NULL |
| `updated_at` | DateTime(tz) | |

**Unique constraint:** `(worker_id, lang_code)`

---

## Entity Relationship Summary

```
faculties (faculty_code PK)
│
├── faculties_tr                        (faculty_code)
│
├── faculty_directors                   (faculty_code) [1:1]
│   ├── faculty_director_tr             (director_id)
│   ├── faculty_director_working_hours  (director_id)
│   │   └── faculty_director_working_hour_tr   (working_hour_id)
│   ├── faculty_director_scientific_events     (director_id)
│   │   └── faculty_director_scientific_event_tr (scientific_event_id)
│   └── faculty_director_educations     (director_id)
│       └── faculty_director_education_tr      (education_id)
│
├── faculty_laboratories                (faculty_code)
│   └── faculty_laboratory_tr          (laboratory_id)
│
├── faculty_research_works              (faculty_code)
│   └── faculty_research_work_tr       (research_work_id)
│
├── faculty_partner_companies           (faculty_code)
│   └── faculty_partner_company_tr     (partner_company_id)
│
├── faculty_objectives                  (faculty_code)
│   └── faculty_objective_tr           (objective_id)
│
├── faculty_duties                      (faculty_code)
│   └── faculty_duty_tr                (duty_id)
│
├── faculty_projects                    (faculty_code)
│   └── faculty_project_tr             (project_id)
│
├── faculty_directions_of_action        (faculty_code)
│   └── faculty_direction_of_action_tr (direction_of_action_id)
│
├── faculty_deputy_deans                (faculty_code)
│   └── faculty_deputy_dean_tr         (deputy_dean_id)
│
├── faculty_scientific_council          (faculty_code)
│   └── faculty_council_member_tr      (council_member_id)
│
└── faculty_workers                     (faculty_code)
    └── faculty_worker_tr              (worker_id)
```
