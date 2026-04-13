# Research Institute Admin Integration Guide

## Endpoints

### 1. Fetch All Research Institutes (Admin)
- **URL:** `/api/research-institute/admin/all`
- **Method:** `GET`
- **Query Params:**
  - `start` (int, default: 0)
  - `end` (int, default: 10)
  - `lang` (str, default: "az")
- **Description:** Returns a list of all research institutes for admin management.

### 2. Create Research Institute
- **URL:** `/api/research-institute/create`
- **Method:** `POST`
- **Request Body:** `CreateResearchInstitute` schema
```json
{
  "institute_code": "RI-001",
  "image_url": "string",
  "az": {
    "name": "Kibertehlükəsizlik İnstitutu",
    "about": "İnstitut haqqında...",
    "vision": "Gələcək baxış...",
    "mission": "Missiya..."
  },
  "en": {
    "name": "Cybersecurity Institute",
    "about": "About the institute...",
    "vision": "Vision...",
    "mission": "Mission..."
  },
  "director": {
    "full_name": "John Doe",
    "email": "john.doe@aztu.edu.az",
    "office": "Room 101",
    "image_url": "string",
    "az": {
      "title": "Direktor",
      "biography": "Bioqrafiya..."
    },
    "en": {
      "title": "Director",
      "biography": "Biography..."
    },
    "educations": [
      {
        "az": { "university": "ADNSU", "degree": "Bakalavr" },
        "en": { "university": "ASOIU", "degree": "Bachelor" },
        "start_year": "2010",
        "end_year": "2014",
        "display_order": 0
      },
      {
        "az": { "university": "AzTU", "degree": "Magistr" },
        "en": { "university": "AzTU", "degree": "Master" },
        "start_year": "2014",
        "end_year": null,
        "display_order": 1
      }
    ],
    "research_areas": [
      {
        "az": { "content": "Şəbəkə təhlükəsizliyi" },
        "en": { "content": "Network security" },
        "display_order": 0
      }
    ]
  },
  "objectives": [
    {
      "az": { "content": "Məqsəd 1" },
      "en": { "content": "Objective 1" },
      "display_order": 0
    }
  ],
  "research_directions": [
    {
      "az": { "content": "İstiqamət 1" },
      "en": { "content": "Direction 1" },
      "display_order": 0
    }
  ],
  "staff": [
    {
      "full_name": "Jane Smith",
      "email": "jane.smith@aztu.edu.az",
      "phone": "+994501234567",
      "image_url": "string",
      "display_order": 0,
      "az": { "title": "Baş elmi işçi" },
      "en": { "title": "Senior Researcher" }
    }
  ]
}
```

### 3. Update Research Institute
- **URL:** `/api/research-institute/{institute_code}`
- **Method:** `PATCH`
- **Request Body:** `UpdateResearchInstitute` schema (all fields optional)

### 4. Delete Research Institute
- **URL:** `/api/research-institute/{institute_code}`
- **Method:** `DELETE`

### 5. Upload Institute Image
- **URL:** `/api/research-institute/{institute_code}/image`
- **Method:** `PUT`
- **Body:** `multipart/form-data` with `image` field.

### 6. Upload Director Image
- **URL:** `/api/research-institute/director/{director_id}/image`
- **Method:** `PUT`
- **Body:** `multipart/form-data` with `image` field.

### 7. Upload Staff Image
- **URL:** `/api/research-institute/staff/{staff_id}/image`
- **Method:** `PUT`
- **Body:** `multipart/form-data` with `image` field.

## Field Names
- `institute_code`: Unique identifier (string)
- `name`: Institute name (multilingual)
- `about`: About text (multilingual)
- `vision`: Vision text (multilingual)
- `mission`: Mission text (multilingual)
- `full_name`: Person's full name
- `title`: Professional title (Director, Researcher, etc.)
- `content`: Content for objectives/directions/research areas
