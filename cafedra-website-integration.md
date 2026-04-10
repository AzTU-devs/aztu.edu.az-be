# Cafedra Website Integration Guide

This document outlines the frontend integration for the **Cafedras (Departments)** module within a Faculty website. Each faculty contains multiple cafedras, each with its own detailed pages, personnel, and research sections.

---

## 1. Cafedra Listing (Within Faculty Page)

**Goal:** Display all cafedras associated with a specific faculty.

- **API Endpoint:** `GET /api/cafedra/public/all?faculty_code={faculty_code}&lang={lang}`
- **Parameters:**
  - `faculty_code`: Unique code of the parent faculty.
  - `lang`: `az` or `en`.
  - `start`, `end`: For pagination (optional).

### Key Response Fields
| Field | Type | Description |
| :--- | :--- | :--- |
| `cafedras` | Array | List of cafedra summary objects. |
| `cafedras[].cafedra_code` | String | Unique identifier used for routing to the detail page. |
| `cafedras[].title` | String | Translated name of the cafedra. |
| `cafedras[].deputy_director_count` | Integer | Number of deputy directors (useful for statistics). |

---

## 2. Cafedra Detail Page (Overview)

**Goal:** Show the main information, statistics, and sections of a single cafedra.

- **API Endpoint:** `GET /api/cafedra/{cafedra_code}?lang={lang}`
- **URL Pattern:** `/faculties/{faculty_code}/cafedras/{cafedra_code}`

### Top Section: Header & Info
- `title`: Cafedra name.
- `html_content`: Rich text "About" section.

### Section: Statistics (Counters)
| Field | Description |
| :--- | :--- |
| `bachelor_programs_count` | Number of Bachelor programs. |
| `master_programs_count` | Number of Master programs. |
| `phd_programs_count` | Number of PhD programs. |
| `international_collaborations_count` | International partnerships. |
| `laboratories_count` | Number of active labs. |
| `projects_patents_count` | Patents and major projects. |
| `industrial_collaborations_count` | Local industry partners. |

### Section: Sustainable Development Goals (SDGs)
- `sdgs`: Array of integers (1-17). Use standard UN SDG icons for these numbers.

---

## 3. Personnel Sections

### Cafedra Director (Head of Department)
Data found in `director` object of the detail response.

| Field | Description |
| :--- | :--- |
| `first_name`, `last_name`, `father_name` | Full name of the director. |
| `profile_image` | Image URL (e.g., `static/cafedra-directors/...`). |
| `scientific_degree` | Translated degree (e.g., "PhD"). |
| `scientific_title` | Translated title (e.g., "Associate Professor"). |
| `bio` | HTML content of the biography. |
| `email`, `phone`, `room_number` | Contact details. |
| `working_hours` | Array of `{day, time_range}`. |
| `educations` | Array of `{degree, university, start_year, end_year}`. |
| `scientific_events` | Array of `{event_title, event_description}`. |

### Deputy Directors & Workers
Arrays: `deputy_directors` and `workers`.

| Field | Description |
| :--- | :--- |
| `first_name`, `last_name`, `father_name` | Personnel name. |
| `profile_image` | Image URL (e.g., `static/cafedra-workers/...`). |
| `duty` | Job title/position. |
| `scientific_name` | Academic name/prefix. |
| `scientific_degree` | Academic degree. |
| `email`, `phone` | Contact info. |

### Scientific Council
Array: `scientific_council`. Same structure as workers but usually lacks `profile_image`.

---

## 4. Academic & Research Sections

The following sections are arrays of `{id, title, description}`. Render them as lists or accordions.

- `laboratories`: Laboratory names and their specific focus.
- `research_works`: Ongoing or completed research topics.
- `partner_companies`: Companies the cafedra collaborates with.
- `objectives`: Strategic goals of the cafedra.
- `duties`: Core responsibilities.
- `projects`: Specific research or development projects.
- `directions_of_action`: Primary operational focus areas.

---

## 5. Implementation Notes

1. **Image Rendering:** All image paths returned by the API (like `profile_image`) start with `static/`. Prefix them with your backend base URL (e.g., `https://api.aztu.edu.az/static/...`).
2. **HTML Content:** Fields like `html_content` and `bio` contain raw HTML. Ensure they are sanitized and rendered safely (e.g., using `dangerouslySetInnerHTML` in React).
3. **Empty States:** Many sections (like `scientific_events` or `projects`) might be empty arrays. Hide the section header if no data is present.
4. **Localization:** Always pass the `lang` header or query parameter (`az` or `en`) to ensure you get the correct translations. The API defaults to `az`.
