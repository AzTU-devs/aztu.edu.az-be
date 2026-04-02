# Department Module — Admin Frontend Guide

Base URL: `/api/department`  
All mutating endpoints require `Authorization: Bearer <token>` header.  
Language is passed via `Accept-Language: az` or `Accept-Language: en` header (defaults to `az`).

---

## Pages to Build

### 1. Department List Page

**Route:** `/admin/departments`

**API call:**
```
GET /api/department/admin/all?start=0&end=20
Accept-Language: az
Authorization: Bearer <token>
```

**Response shape:**
```json
{
  "status_code": 200,
  "departments": [
    {
      "id": 1,
      "department_code": "482910",
      "department_name": "İnsan Resursları Şöbəsi",
      "worker_count": 5,
      "created_at": "2026-04-02T10:00:00+00:00",
      "updated_at": "2026-04-02T10:00:00+00:00"
    }
  ],
  "total": 1
}
```

**UI elements:**
- Table with columns: Name, Worker Count, Created At, Actions (Edit / Delete)
- Pagination controls using `start` / `end` query params
- "Add Department" button → navigates to Create page
- Delete button → calls DELETE, shows confirmation dialog first

---

### 2. Create Department Page

**Route:** `/admin/departments/create`

**Form fields:**

| Field | Type | Notes |
|---|---|---|
| Department Name (AZ) | text input | required |
| About HTML (AZ) | rich-text / HTML editor | optional |
| Department Name (EN) | text input | required |
| About HTML (EN) | rich-text / HTML editor | optional |
| Objectives | repeatable rich-text list | each item has AZ + EN html_content |
| Core Functions | repeatable rich-text list | each item has AZ + EN html_content |
| Director section | see below | optional |
| Workers | repeatable person form | see below |

**Director sub-form (optional, collapsible):**
| Field | Type | Notes |
|---|---|---|
| First Name | text | required if director added |
| Last Name | text | required |
| Father Name | text | optional |
| Room Number | text | e.g. `1-202` |
| Scientific Degree (AZ) | text | optional |
| Scientific Title (AZ) | text | optional |
| Bio (AZ) | textarea | optional |
| Scientific Degree (EN) | text | optional |
| Scientific Title (EN) | text | optional |
| Bio (EN) | textarea | optional |
| Working Hours | repeatable: time_range + day(AZ) + day(EN) | |
| Educations | repeatable: start_year, end_year, degree(AZ), university(AZ), degree(EN), university(EN) | |

> **Note:** Director profile image is uploaded separately after the director is created (see Upload Image section).

**Worker sub-form (repeatable):**
| Field | Type | Notes |
|---|---|---|
| First Name | text | required |
| Last Name | text | required |
| Father Name | text | optional |
| Email | email input | optional |
| Phone | text | optional |
| Duty (AZ) | text | required |
| Scientific Degree (AZ) | text | optional |
| Scientific Name (AZ) | text | optional |
| Duty (EN) | text | required |
| Scientific Degree (EN) | text | optional |
| Scientific Name (EN) | text | optional |

> **Note:** Worker profile images are uploaded separately after save (see Upload Image section).

**API call:**
```
POST /api/department/create
Authorization: Bearer <token>
Content-Type: application/json

{
  "az": {
    "department_name": "İnsan Resursları Şöbəsi",
    "about_html": "<p>Şöbə haqqında məlumat...</p>"
  },
  "en": {
    "department_name": "Human Resources Department",
    "about_html": "<p>About the department...</p>"
  },
  "objectives": [
    {
      "az": { "html_content": "<p>Məqsəd 1</p>" },
      "en": { "html_content": "<p>Objective 1</p>" }
    }
  ],
  "core_functions": [
    {
      "az": { "html_content": "<p>Əsas funksiya 1</p>" },
      "en": { "html_content": "<p>Core function 1</p>" }
    }
  ],
  "director": {
    "first_name": "Əli",
    "last_name": "Həsənov",
    "father_name": "Vüsal",
    "room_number": "1-202",
    "az": { "scientific_degree": "f.e.d.", "scientific_title": "dosent", "bio": "<p>Bio...</p>" },
    "en": { "scientific_degree": "PhD", "scientific_title": "Associate Professor", "bio": "<p>Bio...</p>" },
    "working_hours": [
      { "time_range": "09:00-13:00", "az": { "day": "Bazar ertəsi" }, "en": { "day": "Monday" } }
    ],
    "educations": [
      {
        "start_year": "2000",
        "end_year": "2005",
        "az": { "degree": "Bakalavr", "university": "AzTU" },
        "en": { "degree": "Bachelor", "university": "AzTU" }
      }
    ]
  },
  "workers": [
    {
      "first_name": "Nigar",
      "last_name": "Quliyeva",
      "father_name": "Tural",
      "email": "nigar@aztu.edu.az",
      "phone": "+994501234567",
      "az": { "duty": "Mütəxəssis", "scientific_degree": null, "scientific_name": null },
      "en": { "duty": "Specialist", "scientific_degree": null, "scientific_name": null }
    }
  ]
}
```

**Success response:** `201 Created`
```json
{
  "status_code": 201,
  "message": "Department created successfully.",
  "data": { "department_code": "482910", "created_at": "..." }
}
```

**After creation** — store `department_code` from the response to use for image uploads.

---

### 3. Edit Department Page

**Route:** `/admin/departments/:department_code/edit`

**Load current data:**
```
GET /api/department/:department_code
Accept-Language: az
Authorization: Bearer <token>
```

Pre-fill the form with the returned data. Send only changed fields in the PATCH body — unset fields are ignored by the backend.

**API call:**
```
PUT /api/department/:department_code
Authorization: Bearer <token>
Content-Type: application/json

{
  "az": { "department_name": "Yeni ad", "about_html": "<p>...</p>" },
  "objectives": [ ... ],
  "workers": [ ... ]
}
```

> **Important:** `objectives`, `core_functions`, and `workers` are **replaced in full** on update. Send the complete list each time (not just the delta).  
> The `director` object uses upsert logic — only the fields you include are updated.  
> If `director` is sent as `null`, the director record is deleted.

---

### 4. Upload Director Profile Image

After creating or editing a department that has a director, provide an image upload button.

**API call:**
```
PUT /api/department/:department_code/director/image
Authorization: Bearer <token>
Content-Type: multipart/form-data

image: <file>
```

**Accepted formats:** JPEG, PNG, WebP, GIF  
**Max size:** configured in backend settings (typically 5 MB)

**Response:**
```json
{
  "status_code": 200,
  "message": "Director image uploaded successfully.",
  "data": { "profile_image": "static/department-directors/abc123.jpg" }
}
```

Prepend the API base URL to `profile_image` to display it: `https://api.aztu.edu.az/static/department-directors/abc123.jpg`

---

### 5. Upload Worker Profile Image

Each worker card in the list should have an upload button.

**API call:**
```
PUT /api/department/workers/:worker_id/image
Authorization: Bearer <token>
Content-Type: multipart/form-data

image: <file>
```

**Response:**
```json
{
  "status_code": 200,
  "message": "Worker image uploaded successfully.",
  "data": { "profile_image": "static/department-workers/xyz789.png" }
}
```

> The `worker_id` is returned in the full department GET response inside each worker object.

---

### 6. Delete Department

Triggered from the list or edit page.

**API call:**
```
DELETE /api/department/:department_code
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{ "status_code": 200, "message": "Department deleted successfully." }
```

---

## Error Handling

| Status | Meaning |
|---|---|
| 401 | Missing or invalid admin token |
| 404 | Department / director / worker not found |
| 413 | Uploaded file too large |
| 415 | Unsupported file type |
| 422 | Validation error (e.g. duplicate department name) |
| 500 | Server error |

**422 shape:**
```json
{
  "status_code": 422,
  "errors": { "department_name": ["Department name 'X' (az) already exists."] }
}
```
