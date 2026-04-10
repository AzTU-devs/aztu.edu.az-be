# Cafedra Module Integration Handoff

This document provides the necessary information for the frontend admin to integrate the Cafedra Module. The cafedra now has full parity with the faculty module structure.

## API Endpoints

### 1. Create Cafedra
- **Endpoint:** `POST /api/cafedra/create`
- **Payload:** `CreateCafedra` schema
- **Description:** Creates a new cafedra assigned to a faculty.

### 2. Update Cafedra
- **Endpoint:** `PUT /api/cafedra/{cafedra_code}`
- **Payload:** `UpdateCafedra` schema (all fields optional)
- **Description:** Updates existing cafedra information. Sections are replaced entirely when provided.

### 3. Get Cafedra Details
- **Endpoint:** `GET /api/cafedra/{cafedra_code}?lang=az`
- **Response:** Detailed cafedra object including all sections, personnel, and director.

### 4. Get All Cafedras
- **Admin:** `GET /api/cafedra/admin/all?faculty_code=...&start=0&end=10&lang=az`
- **Public:** `GET /api/cafedra/public/all?faculty_code=...&start=0&end=10&lang=az`
- **Description:** List cafedras, optionally filtered by `faculty_code`.

### 5. Delete Cafedra
- **Endpoint:** `DELETE /api/cafedra/{cafedra_code}`
- **Description:** Deletes the cafedra and all associated data (cascading).

### 6. Image Uploads
- **Director Profile:** `PUT /api/cafedra/{cafedra_code}/director/image`
- **Deputy Director Profile:** `PUT /api/cafedra/deputy-directors/{deputy_director_id}/image`
- **Worker Profile:** `PUT /api/cafedra/workers/{worker_id}/image`
- **Format:** `multipart/form-data` with `image` field.

## Data Structure

### Statistics & SDGs
Available in `Create` and `Update` payloads:
- `bachelor_programs_count` (int)
- `master_programs_count` (int)
- `phd_programs_count` (int)
- `international_collaborations_count` (int)
- `laboratories_count` (int)
- `projects_patents_count` (int)
- `industrial_collaborations_count` (int)
- `sdgs`: List of integers (1-17).

### Cafedra Director
- `first_name`, `last_name`, `father_name`, `email`, `phone`, `room_number`.
- `az`, `en` translations:
  - `scientific_degree`, `scientific_title`, `bio` (HTML).
  - `scientific_research_fields`: List of strings.
- `working_hours`: List of items with `az`, `en` (day) and `time_range`.
- `scientific_events`: List of items with `az`, `en` (`event_title`, `event_description`).
- `educations`: List of items with `az`, `en` (degree, university) and `start_year`, `end_year`.

### Deputy Directors
- `first_name`, `last_name`, `father_name`, `email`, `phone`.
- `az`, `en` translations: `duty`, `scientific_name`, `scientific_degree`.
- `profile_image`: Upload via dedicated endpoint after creation.

### Scientific Council
- `first_name`, `last_name`, `father_name`, `email`, `phone`.
- `az`, `en` translations: `duty` (required), `scientific_name`, `scientific_degree`.
- No `profile_image`.

### Workers
- `first_name`, `last_name`, `father_name`, `email`, `phone`.
- `az`, `en` translations: `duty`, `scientific_name`, `scientific_degree`.
- `profile_image`: Upload via dedicated endpoint after creation.

### Section Items (all use same structure)
The following sections each contain a list of items with `az` and `en` translations (`title`, `description`):
- `laboratories`
- `research_works`
- `partner_companies`
- `objectives`
- `duties`
- `projects`
- `directions_of_action`

## Frontend Integration Tips
1. **Faculty Assignment:** Always provide a valid `faculty_code` when creating a Cafedra.
2. **HTML Content:** Use a rich text editor for Cafedra `about_text` (via `html_content`) and Director `bio`.
3. **Sequential Uploads:** Create the Cafedra first, then use the returned `cafedra_code` or entity `id` for profile image uploads.
4. **Section Updates:** When updating sections (e.g., `laboratories`), send the complete list — existing items are deleted and replaced.
5. **Deputy Director Images:** After creating/updating a cafedra, fetch it to get `deputy_director.id`, then upload images individually.
