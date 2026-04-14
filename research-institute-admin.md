# Research Institute — Admin API & Integration

Base URL: `/api/research-institute`  
All mutating endpoints (`POST`, `PUT`, `DELETE`) require `Authorization: Bearer <token>`.

---

## API Endpoints

### 1. List Institutes (Admin)
- **Method:** `GET`
- **Path:** `/api/research-institute/admin/all`
- **Query Params:** `start` (default 0), `end` (default 10)
- **Header:** `Accept-Language: az|en`

### 2. Get Institute Detail
- **Method:** `GET`
- **Path:** `/api/research-institute/{institute_code}`
- **Header:** `Accept-Language: az|en`

### 3. Create Institute
- **Method:** `POST`
- **Path:** `/api/research-institute/create`
- **Payload:**
```json
{
  "image": "path/to/image.jpg",
  "az": {
    "name": "Tədqiqat İnstitutu",
    "about_html": "<p>...</p>",
    "vision_html": "<p>...</p>",
    "mission_html": "<p>...</p>",
    "goals_html": "<p>...</p>",
    "direction_html": "<p>...</p>"
  },
  "en": {
    "name": "Research Institute",
    "about_html": "<p>...</p>",
    "vision_html": "<p>...</p>",
    "mission_html": "<p>...</p>",
    "goals_html": "<p>...</p>",
    "direction_html": "<p>...</p>"
  },
  "director": {
    "first_name": "...",
    "last_name": "...",
    "father_name": "...",
    "email": "director@example.com",
    "room_number": "1-102",
    "az": {
      "scientific_name": "...",
      "scientific_degree": "...",
      "bio": "<p>...</p>",
      "researcher_areas": "Süni intellekt, Maşın öyrənməsi"
    },
    "en": {
      "scientific_name": "...",
      "scientific_degree": "...",
      "bio": "<p>...</p>",
      "researcher_areas": "AI, Machine Learning"
    },
    "educations": [
      {
        "university_name": "AzTU",
        "start_year": "2000",
        "end_year": "2004",
        "az": { "degree": "Bakalavr" },
        "en": { "degree": "Bachelor" }
      }
    ]
  },
  "staff": [
    {
      "first_name": "...",
      "last_name": "...",
      "father_name": "...",
      "email": "...",
      "phone_number": "...",
      "az": { "scientific_name": "...", "scientific_degree": "..." },
      "en": { "scientific_name": "...", "scientific_degree": "..." }
    }
  ]
}
```

### 4. Update Institute
- **Method:** `PUT`
- **Path:** `/api/research-institute/{institute_code}`
- **Payload:** Same as create, all fields optional.

### 5. Image Uploads
- **Institute Image:** `PUT /api/research-institute/{institute_code}/image`
- **Director Image:** `PUT /api/research-institute/{institute_code}/director/image`
- **Staff Image:** `PUT /api/research-institute/staff/{staff_id}/image`

---

## UI Components to Build

1. **Institute List Table:** Name, Staff Count, Actions.
2. **Institute Form:** 
    - Translatable Name and HTML editors for About, Vision, Mission, Goals, Directions.
    - Director section (Nested form).
    - Staff Members section (Repeatable nested form).
3. **Image Upload Buttons:** For institute, director, and each staff member.
