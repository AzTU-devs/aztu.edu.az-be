# Department Module — Website UI/UX Display Guide

This guide provides recommendations for displaying department details, including the director and staff with their profile images, on the public university website.

## 1. Department Overview Section

Display the department name as the main heading (`H1`), followed by the "About" content.

- **Background:** Use a clean, light background.
- **Typography:** Ensure `about_html` (which contains rich text) is rendered with standard university typography (e.g., standard line-height for paragraphs, bold for strong tags).

---

## 2. Director Profile Card

The director is the most prominent individual in the department. Use a "Hero" style card or a dedicated sidebar section.

### Layout Components:
- **Image:** Large, high-quality portrait (circular or soft-rounded corners).
- **Name:** `last_name + " " + first_name + " " + (father_name or "")`.
- **Titles:** Combine `scientific_degree` and `scientific_title` (e.g., "PhD, Associate Professor").
- **Contact:** Display `room_number` with an icon.
- **Bio:** Use a collapsible "Read More" if the bio is long.

### Handling the Profile Image:
```html
<!-- Example Vue/React Logic -->
<img 
  :src="director.profile_image ? `${API_BASE_URL}/${director.profile_image}` : '/assets/placeholders/avatar-director.png'" 
  alt="Director Photo"
  class="director-photo"
/>
```

---

## 3. Department Staff (Workers) Grid

Display staff members in a responsive grid (1 column on mobile, 3-4 columns on desktop).

### Staff Card UI:
- **Header:** Small profile image (top or left-aligned).
- **Body:**
    - Full Name (Bold)
    - Position (`duty`)
    - Scientific Info (Small text, if available)
- **Footer:** 
    - Email (icon link)
    - Phone (icon link)

### Responsive Grid Example (CSS):
```css
.staff-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}
.staff-card {
  border: 1px solid #eee;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
}
.staff-img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 10px;
}
```

---

## 4. Academic Sections (Objectives & Functions)

Use interactive elements like accordions or tabbed views if the content is long, but for standard university layouts, a simple list with icons is preferred.

- **Objectives:** Use a "Checkmark" or "Target" icon for each list item.
- **Core Functions:** Use a "Gear" or "Function" icon for each list item.

---

## 5. Profile Image Fallback Strategy

Since not all staff members might have a photo immediately:
1. **Director:** Use a professional generic "Director" silhouette.
2. **Staff:** Use a generic "Staff Member" silhouette or just the person's initials in a colored circle (e.g., "NQ" for Nigar Quliyeva).

---

## 6. Data Fetching Example (Public)

```javascript
// Fetch department details in the current language
async function fetchDepartment(code, lang) {
  const response = await fetch(`https://api.aztu.edu.az/api/department/${code}`, {
    headers: {
      'Accept-Language': lang
    }
  });
  const result = await response.json();
  return result.department;
}
```

---

## 7. URL Construction Table

| Field | Source Path | Full URL Construction |
|---|---|---|
| Director Photo | `director.profile_image` | `API_BASE + "/" + director.profile_image` |
| Worker Photo | `worker.profile_image` | `API_BASE + "/" + worker.profile_image` |

*Note: The backend stores paths relative to the `static` directory (e.g. `static/department-workers/xyz.png`).*
