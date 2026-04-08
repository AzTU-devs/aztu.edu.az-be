# Cafedra Module Integration Handoff

This document provides the necessary information for the frontend admin to integrate the updated Cafedra Module.

## API Endpoints

### 1. Create Cafedra
- **Endpoint:** `POST /api/v1/cafedra/create`
- **Payload:** `CreateCafedra` schema
- **Description:** Creates a new cafedra assigned to a faculty.

### 2. Update Cafedra
- **Endpoint:** `PUT /api/v1/cafedra/{cafedra_code}`
- **Payload:** `UpdateCafedra` schema (all fields optional)
- **Description:** Updates existing cafedra information.

### 3. Get Cafedra Details
- **Endpoint:** `GET /api/v1/cafedra/{cafedra_code}`
- **Response:** Detailed cafedra object including statistics, director, and workers.

### 4. Get All Cafedras
- **Admin:** `GET /api/v1/cafedra/admin/all?faculty_code=...`
- **Public:** `GET /api/v1/cafedra/public/all?faculty_code=...`
- **Description:** List cafedras, optionally filtered by `faculty_code`.

### 5. Delete Cafedra
- **Endpoint:** `DELETE /api/v1/cafedra/{cafedra_code}`
- **Description:** Deletes the cafedra and all associated data.

### 6. Image Uploads
- **Director Profile:** `PUT /api/v1/cafedra/{cafedra_code}/director/image`
- **Worker Profile:** `PUT /api/v1/cafedra/workers/{worker_id}/image`
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
- `educations`: List of items with `az`, `en` (degree, university) and `start_year`, `end_year`.

### Workers
- `first_name`, `last_name`, `father_name`, `email`, `phone`.
- `az`, `en` translations: `duty`, `scientific_name`, `scientific_degree`.

### Directions of Action
- `directions_of_action`: List of items with `az`, `en` translations (title, description).

## Frontend Integration Tips
1. **Faculty Assignment:** Always provide a valid `faculty_code` when creating a Cafedra.
2. **HTML Content:** Use a rich text editor for Cafedra `about_text` and Director `bio`.
3. **Sequential Uploads:** Create the Cafedra first, then use the returned `cafedra_code` or `worker_id` for profile image uploads.
