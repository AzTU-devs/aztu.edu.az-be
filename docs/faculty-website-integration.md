# Faculty Website Integration Guide (Updated)

This document provides the necessary TypeScript interfaces and API usage details to integrate the Faculty module with the frontend. The backend has been updated to return a flattened response structure and ensure all string fields return empty strings (`""`) instead of `null` to prevent "undefined" errors in the UI.

---

## 1. TypeScript Interfaces

Use these interfaces to ensure type safety and correct field mapping.

```typescript
export interface PersonnelItem {
  id: number;
  first_name: string;
  last_name: string;
  father_name: string;
  duty: string;
  scientific_name: string;
  scientific_degree: string;
  email: string;
  phone: string;
  profile_image: string | null;
}

export interface Education {
  degree: string;
  university: string;
  start_year: string;
  end_year: string;
}

export interface WorkingHour {
  day: string;
  time_range: string;
}

export interface ScientificEvent {
  event_title: string;
  event_description: string;
}

export interface Director {
  first_name: string;
  last_name: string;
  father_name: string;
  scientific_degree: string;
  scientific_title: string;
  bio: string;
  profile_image: string | null;
  email: string;
  phone: string;
  room_number: string;
  scientific_research_fields: string[];
  working_hours: WorkingHour[];
  scientific_events: ScientificEvent[];
  educations: Education[];
}

export interface ContentSection {
  id: number;
  title: string;
  description: string;
}

export interface FacultyDetail {
  faculty_code: string;
  title: string;
  html_content: string;
  bachelor_programs_count: number;
  master_programs_count: number;
  phd_programs_count: number;
  international_collaborations_count: number;
  laboratories_count: number;
  projects_patents_count: number;
  industrial_collaborations_count: number;
  sdgs: number[];
  cafedra_count: number;
  deputy_dean_count: number;
  director: Director | null;
  deputy_deans: PersonnelItem[];
  scientific_council: PersonnelItem[];
  workers: PersonnelItem[];
  laboratories: ContentSection[];
  research_works: ContentSection[];
  partner_companies: ContentSection[];
  objectives: ContentSection[];
  duties: ContentSection[];
  projects: ContentSection[];
  directions_of_action: ContentSection[];
}
```

---

## 2. API Endpoints

### Get Faculty Details
**Endpoint:** `GET /api/faculty/{faculty_code}?lang={az|en}`

**Notes:**
- The response is now **flattened**. The `FacultyDetail` object is returned directly as the root of the JSON response.
- If `?lang` is provided, all translatable fields (title, bio, duties, etc.) are returned as strings.
- Missing text values return an empty string `""` instead of `null`.

**Sample Response (`GET /api/faculty/MMF?lang=az`):**
```json
{
  "faculty_code": "MMF",
  "title": "Maşınqayırma və Metallurgiya Fakültəsi",
  "html_content": "<p>Fakültə haqqında məlumat...</p>",
  "bachelor_programs_count": 5,
  "master_programs_count": 3,
  "phd_programs_count": 1,
  "international_collaborations_count": 10,
  "laboratories_count": 4,
  "projects_patents_count": 12,
  "industrial_collaborations_count": 8,
  "sdgs": [4, 9],
  "cafedra_count": 6,
  "deputy_dean_count": 2,
  "director": {
    "first_name": "Məlik",
    "last_name": "Qarayev",
    "father_name": "Fikrət",
    "scientific_degree": "Texnika elmləri namizədi",
    "scientific_title": "Dosent",
    "bio": "<p>Bioqrafiya...</p>",
    "profile_image": "static/directors/malik_qarayev.jpg",
    "email": "m.garayev@aztu.edu.az",
    "phone": "+994 12 539 12 34",
    "room_number": "201",
    "scientific_research_fields": ["Maşınqayırma texnologiyası"],
    "working_hours": [
      { "day": "Bazar ertəsi", "time_range": "09:00 - 18:00" }
    ],
    "scientific_events": [],
    "educations": []
  },
  "deputy_deans": [
    {
      "id": 1,
      "first_name": "Ad",
      "last_name": "Soyad",
      "father_name": "Ata adı",
      "duty": "Dekan müavini",
      "scientific_name": "Dosent",
      "scientific_degree": "Fəlsəfə doktoru",
      "email": "example@aztu.edu.az",
      "phone": "",
      "profile_image": null
    }
  ],
  "scientific_council": [],
  "workers": [],
  "laboratories": [
    { "id": 1, "title": "Laboratoriya 1", "description": "Təsvir..." }
  ],
  "research_works": [],
  "partner_companies": [],
  "objectives": [],
  "duties": [],
  "projects": [],
  "directions_of_action": []
}
```

---

## 3. Integration Tips

1.  **Flattened Access:** When you receive the response from the Axios/Fetch call, the data *is* the `FacultyDetail` object.
    ```javascript
    // Correct
    const faculty = response.data;
    console.log(faculty.title); 

    // Incorrect (no longer needed)
    // const faculty = response.data.faculty;
    ```

2.  **Images:** Prepend the base URL of the API to the `profile_image` path if it is not null.
    ```javascript
    const imageUrl = faculty.director.profile_image 
      ? `${process.env.NEXT_PUBLIC_API_URL}/${faculty.director.profile_image}`
      : '/placeholder-avatar.png';
    ```

3.  **Bilingual Mode:** If you do *not* pass the `?lang` parameter, the fields will return an object with `az` and `en` keys. For the website, it is highly recommended to always pass the `?lang` parameter based on the current active language in your app.

4.  **Empty Arrays:** Lists like `scientific_research_fields`, `deputy_deans`, and content sections like `laboratories` are guaranteed to be arrays. You can safely call `.map()` on them.
