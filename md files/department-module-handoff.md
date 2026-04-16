# Department Module Integration Handoff

This document provides the necessary information for the frontend admin to integrate the Department Module. The Department module is designed for administrative and central university departments (e.g., HR, IT, etc.).

## API Endpoints

### 1. Create Department
- **Endpoint:** `POST /api/department/create`
- **Payload:** `CreateDepartment` schema
- **Description:** Creates a new department. A unique `department_code` (6-digit) is generated automatically.

### 2. Update Department
- **Endpoint:** `PUT /api/department/{department_code}`
- **Payload:** `UpdateDepartment` schema (all fields optional)
- **Description:** Updates existing department information. Lists like `objectives`, `core_functions`, and `workers` are replaced entirely when provided. The `director` object uses upsert logic.

### 3. Get Department Details
- **Endpoint:** `GET /api/department/{department_code}?lang=az`
- **Response:** Detailed department object including objectives, core functions, director, and workers.

### 4. Get All Departments
- **Admin:** `GET /api/department/admin/all?start=0&end=10&lang=az`
- **Public:** `GET /api/department/public/all?start=0&end=10&lang=az`
- **Description:** List departments with pagination.

### 5. Delete Department
- **Endpoint:** `DELETE /api/department/{department_code}`
- **Description:** Deletes the department and all associated data (cascading).

### 6. Image Uploads
- **Director Profile:** `PUT /api/department/{department_code}/director/image`
- **Worker Profile:** `PUT /api/department/workers/{worker_id}/image`
- **Format:** `multipart/form-data` with `image` field.

## Data Structure

### Department Translation
- `department_name` (string, required)
- `about_html` (string, optional)

### Sections (Objectives & Core Functions)
Each contains a list of items with `az` and `en` translations:
- `html_content` (string, required)

### Department Director
- `first_name`, `last_name`, `father_name`, `room_number`.
- `az`, `en` translations:
  - `scientific_degree`, `scientific_title`, `bio` (HTML).
- `working_hours`: List of items with `az`, `en` (day) and `time_range`.
- `educations`: List of items with `az`, `en` (degree, university) and `start_year`, `end_year`.
- `profile_image`: Upload via dedicated endpoint.

### Workers
- `first_name`, `last_name`, `father_name`, `email`, `phone`.
- `az`, `en` translations: `duty` (required), `scientific_degree`, `scientific_name`.
- `profile_image`: Upload via dedicated endpoint after creation.

## Frontend Integration Tips
1. **HTML Content:** Use a rich text editor for Department `about_html`, Objectives, Core Functions, and Director `bio`.
2. **Sequential Uploads:** Create the Department first, then use the returned `department_code` for the director image, or `worker.id` for worker images.
3. **List Updates:** When updating `objectives`, `core_functions`, or `workers`, send the complete list — existing items are deleted and replaced.
4. **Director Update:** The `director` object can be updated partially. To remove the director, send `"director": null`.
