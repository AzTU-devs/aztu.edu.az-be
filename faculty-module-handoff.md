# Faculty Module Integration Handoff (Finalized Field Names)

This document provides the exact field names and payload structures for the Faculty Module.

## 1. Faculty Main Data & Statistics

When calling `POST /api/v1/faculty/create` or `PUT /api/v1/faculty/{faculty_code}`, use these exact names:

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `az` | Object | Azerbaijani translations (Title/About) |
| `en` | Object | English translations (Title/About) |
| `bachelor_programs_count` | int | Number of Bachelor programs |
| `master_programs_count` | int | Number of Master programs |
| `phd_programs_count` | int | Number of PhD programs |
| `international_collaborations_count` | int | Number of international collaborations |
| `laboratories_count` | int | Number of laboratories |
| `projects_patents_count` | int | Number of projects & patents |
| `industrial_collaborations_count` | int | Number of industrial collaborations |
| `sdgs` | int[] | List of SDG numbers (e.g., [1, 5, 17]) |

### Language Object (`az` / `en`)
```json
{
  "title": "Faculty Name",
  "html_content": "<p>About text...</p>"
}
```

---

## 2. Director (Dean) - `director` field

Nested inside the main payload as `director`:

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `first_name` | string | First name |
| `last_name` | string | Last name |
| `father_name` | string | Father name |
| `email` | string | Email address |
| `phone` | string | Phone number |
| `room_number` | string | Room number (e.g., "6-404") |
| `az` / `en` | Object | Translations (see below) |
| `working_hours` | Array | List of working hour objects |
| `educations` | Array | List of education objects |

### Director Translations (`az` / `en`)
- `scientific_degree`: string
- `scientific_title`: string
- `bio`: string (HTML content)
- `scientific_research_fields`: string[] (Array of strings)

### Working Hours Item
```json
{
  "az": { "day": "1" },
  "en": { "day": "1" },
  "time_range": "13:00-15:00"
}
```

---

## 3. Personnel Fields

### Deputy Deans (Dean Assistants) - `deputy_deans` field
List of objects:
- `first_name`, `last_name`, `father_name`, `email`, `phone`
- `az` / `en` Translations:
  - `scientific_name`: string
  - `scientific_degree`: string
  - `duty`: string

### Scientific Council - `scientific_council` field
List of objects:
- `first_name`, `last_name`, `father_name`, `email`, `phone`
- `az` / `en` Translations:
  - `duty`: string
  - `scientific_name`: string
  - `scientific_degree`: string

### Workers - `workers` field
List of objects:
- `first_name`, `last_name`, `father_name`, `email`, `phone`
- `az` / `en` Translations:
  - `duty`: string
  - `scientific_name`: string
  - `scientific_degree`: string

---

## 4. Other Sections
All these take a list of `{ "az": { "title": "...", "description": "..." }, "en": { "title": "...", "description": "..." } }`:
- `laboratories`
- `research_works`
- `partner_companies`
- `objectives`
- `duties`
- `projects`
- `directions_of_action`

---

## 5. Image Upload Endpoints (Multipart/Form-Data)

| Endpoint | Method | Key |
| :--- | :--- | :--- |
| `/api/v1/faculty/{faculty_code}/director/image` | PUT | `image` |
| `/api/v1/faculty/deputy-deans/{deputy_dean_id}/image` | PUT | `image` |
| `/api/v1/faculty/workers/{worker_id}/image` | PUT | `image` |

*Note: Ensure the IDs (like `worker_id`) are obtained from the `GET` response or the creation response.*
