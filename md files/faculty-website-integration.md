# Faculty Website Integration Guide

This document defines the data structure and field names for displaying Faculty details on the public-facing website.

## Data Fetching
- **List Endpoint:** `GET /api/v1/faculty/public/all?lang=az`
- **Detail Endpoint:** `GET /api/v1/faculty/{faculty_code}?lang=az`
- **Language Selection:** Query parameter `?lang=az` or `?lang=en`.
- **Base URL for Images:** Prepend the API base domain (e.g., `https://api.aztu.edu.az/`) to the relative image paths.

---

## Response Field Mapping (Detail Endpoint)

### 1. Main Content
| Field Name | Type | Description |
| :--- | :--- | :--- |
| `title` | string | Full name of the Faculty (translated) |
| `html_content` | string | HTML string for the "About" section (translated) |

### 2. Statistics & Counts
| Field Name | Type | Description |
| :--- | :--- | :--- |
| `bachelor_programs_count` | int | Total bachelor programs |
| `master_programs_count` | int | Total master programs |
| `phd_programs_count` | int | Total PhD programs |
| `international_collaborations_count` | int | Total international partnerships |
| `laboratories_count` | int | Number of laboratories |
| `projects_patents_count` | int | Number of projects/patents |
| `industrial_collaborations_count` | int | Total industrial partnerships |
| `sdgs` | int[] | Array of SDG IDs (1 to 17) |
| `cafedra_count` | int | Total number of departments |
| `deputy_dean_count` | int | Number of deputy deans |

---

### 3. Director (Dean) Data - `director` object
| Field Name | Type | Description |
| :--- | :--- | :--- |
| `first_name` | string | |
| `last_name` | string | |
| `father_name` | string | |
| `scientific_degree` | string | Translated |
| `scientific_title` | string | Translated |
| `bio` | string | HTML string (translated) |
| `profile_image` | string | Relative path |
| `email` | string | |
| `phone` | string | |
| `room_number` | string | e.g., "301" |
| `scientific_research_fields`| string[] | Array of research area strings |
| `working_hours` | object[] | `[ { "day": "...", "time_range": "..." } ]` (day is translated) |
| `scientific_events` | object[] | `[ { "event_title": "...", "event_description": "..." } ]` (translated) |
| `educations` | object[] | `[ { "degree": "...", "university": "...", "start_year": "...", "end_year": "..." } ]` (translated) |

---

### 4. Personnel Lists
Arrays: `deputy_deans`, `scientific_council`, `workers`.

**Personnel Item Structure:**
```json
{
  "id": 1,
  "first_name": "string",
  "last_name": "string",
  "father_name": "string",
  "duty": "string", (translated)
  "scientific_name": "string", (translated)
  "scientific_degree": "string", (translated)
  "email": "string",
  "phone": "string", (if available)
  "profile_image": "string" (if available)
}
```

---

### 5. Categorized Content Sections
Arrays: `laboratories`, `research_works`, `partner_companies`, `objectives`, `duties`, `projects`, `directions_of_action`.
Structure: `{ "id": int, "title": "string", "description": "string" }` (all translated).

---

## Technical Notes
- **Language Header:** While `?lang` is preferred, the `Accept-Language` header is also supported.
- **HTML Injection:** Use a safe HTML renderer for `html_content` and `bio`.
- **Image Handling:** handle `null` values for `profile_image` by showing a default avatar.
- **Null Safety:** All fields may be `null` or `[]`.
