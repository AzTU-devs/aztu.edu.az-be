# Research Institute Website Integration Guide

## Endpoints

### 1. Fetch All Research Institutes (Public)
- **URL:** `/api/research-institute/public/all`
- **Method:** `GET`
- **Query Params:**
  - `start` (int, default: 0)
  - `end` (int, default: 10)
  - `lang` (str, default: "az")
- **Description:** Returns a summarized list of all research institutes.

### 2. Fetch Research Institute Details
- **URL:** `/api/research-institute/{institute_code}`
- **Method:** `GET`
- **Query Params:**
  - `lang` (str, default: "az")
- **Description:** Returns full details of a specific research institute.

## Data Structure (Example)
```json
{
  "status_code": 200,
  "message": "Research Institute details fetched successfully.",
  "data": {
    "id": 1,
    "institute_code": "RI-001",
    "image_url": "string",
    "name": "Cybersecurity Institute",
    "about": "About...",
    "vision": "Vision...",
    "mission": "Mission...",
    "director": {
      "id": 1,
      "full_name": "John Doe",
      "email": "john.doe@aztu.edu.az",
      "office": "Room 101",
      "image_url": "string",
      "title": "Director",
      "biography": "Bio...",
      "educations": [
        {
          "id": 1,
          "university": "ASOIU",
          "degree": "Bachelor",
          "start_year": "2010",
          "end_year": "2014"
        },
        {
          "id": 2,
          "university": "AzTU",
          "degree": "Master",
          "start_year": "2014",
          "end_year": null
        }
      ],
      "research_areas": [
        { "id": 1, "content": "Network security" }
      ]
    },
    "objectives": [
      { "id": 1, "content": "Objective 1" }
    ],
    "research_directions": [
      { "id": 1, "content": "Direction 1" }
    ],
    "staff": [
      {
        "id": 1,
        "full_name": "Jane Smith",
        "email": "jane.smith@aztu.edu.az",
        "phone": "+994501234567",
        "image_url": "string",
        "title": "Senior Researcher"
      }
    ],
    "created_at": "2024-03-13T10:00:00Z",
    "updated_at": "2024-03-13T10:00:00Z"
  }
}
```

## Field Names
- `institute_code`: Used in the URL to fetch details.
- `name`: Institute title.
- `about`: Main content.
- `vision`: Vision section content.
- `mission`: Mission section content.
- `director`: Director's profile and details.
- `objectives`: List of institute objectives.
- `research_directions`: List of scientific research areas.
- `staff`: List of team members.
