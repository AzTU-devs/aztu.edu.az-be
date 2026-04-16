# Research Institute — Website UI Guide

Base URL: `/api/research-institute`

---

## Website Endpoints

### 1. Public Institute List
- **Method:** `GET`
- **Path:** `/api/research-institute/public/all`
- **Params:** `lang=az|en`, `start=0`, `end=10`
- **Response Shape:**
```json
{
  "status_code": 200,
  "institutes": [
    {
      "id": 1,
      "institute_code": "123456",
      "name": "Research Institute",
      "staff_count": 5
    }
  ]
}
```

### 2. Institute Detail Page
- **Method:** `GET`
- **Path:** `/api/research-institute/{institute_code}`
- **Params:** `lang=az|en`
- **Main Sections:** 
    - `image`, `name`, `about_html`, `vision_html`, `mission_html`, `goals_html`, `direction_html`.
- **Director Profile:**
    - Photo, Full Name, Degrees, BIO (HTML), Research Areas, Education history.
- **Staff List:**
    - Cards for each staff member with photo, name, degrees, email, phone.

---

## Front-side Prompt for Development

Build a **Research Institute Management Module** using React and Tailwind CSS.
1. **Admin Page:**
    - A paginated list of Research Institutes.
    - A "Create/Edit" form with:
        - Translatable Name and about/vision/mission/goals/direction (use a rich-text editor).
        - A "Director" section for details and separate profile photo upload.
        - A "Staff" section that is a dynamic list of members, each with photo, name, degrees, and contact info.
2. **Public Page:**
    - A clean, modern UI for listing institutes.
    - A detailed view for a single institute featuring a sidebar for the director's profile and a grid for the staff members.
3. **Data Handling:**
    - Use the provided REST API endpoints with the `institute_code` as the primary identifier.
    - Handle multi-language fields by switching between `az` and `en` in the UI.
    - Perform separate image uploads for Institute, Director, and Staff members using the dedicated `PUT` endpoints.
