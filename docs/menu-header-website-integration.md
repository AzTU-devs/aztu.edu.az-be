# Header Menu Website Integration Guide

This document provides instructions for the website frontend on how to fetch and render the main navigation header menu.

## API Endpoint

**URL:** `GET /api/menu/header/`  
**Auth:** Public (No authentication required)  
**Query Parameters:**
- `lang_code` (optional): `az` or `en`. If not provided, it is detected from the `Accept-Language` header or defaults to `az`.

## Data Structure

The API returns a 3-level hierarchical tree structure.

### 1. Level 1: Main Header (Top Bar)
Each item in the top bar is a `MenuHeader` object.
- `id`: Unique identifier.
- `title`: Localized title (e.g., "Universitet").
- `slug`: Localized slug (e.g., "universitet").
- `image_url`: (Optional) Background image URL for the mega-menu dropdown.
- `direct_url`: (Optional) If this is set, the top bar item is a direct link and has no dropdown.
- `items`: Array of Level 2 items.

### 2. Level 2: Dropdown / Mega-Menu Column
Each item in the first level of the dropdown.
- `id`: Unique identifier.
- `title`: Localized title.
- `slug`: Localized slug.
- `direct_url`: (Optional) If set, this item is a direct link and has no sub-items.
- `sub_items`: Array of Level 3 items.

### 3. Level 3: Leaf Items
The final links within a category.
- `id`: Unique identifier.
- `title`: Localized title.
- `slug`: Localized slug.
- `direct_url`: The actual destination URL (always present for Level 3).

### Relationship between Slug and Direct URL
- **Slug:** This is a URL-safe version of the title. It is useful if your frontend uses hierarchical routing (e.g., `/{lang}/{header_slug}/{item_slug}/{sub_item_slug}`).
- **Direct URL:** This is the **authoritative** link provided by the backend. It can be a relative path (e.g., `/az/universitet/haqqimizda/rektor`) or an absolute URL (e.g., `https://portal.edu.az`). **It is recommended to always use `direct_url` for navigation.**

---

## Example Response

```json
{
  "status_code": 200,
  "data": [
    {
      "id": 1,
      "title": "Universitet",
      "slug": "universitet",
      "image_url": "https://aztu.edu.az/static/menu/headers/abc.jpg",
      "direct_url": null,
      "items": [
        {
          "id": 10,
          "title": "Haqqımızda",
          "slug": "haqqimizda",
          "direct_url": null,
          "sub_items": [
            {
              "id": 100,
              "title": "Rektor",
              "slug": "rektor",
              "direct_url": "/az/universitet/haqqimizda/rektor"
            }
          ]
        },
        {
          "id": 11,
          "title": "Əlaqə",
          "slug": "elaqe",
          "direct_url": "/az/universitet/elaqe",
          "sub_items": []
        }
      ]
    },
    {
      "id": 2,
      "title": "Qəbul",
      "slug": "qebul",
      "image_url": null,
      "direct_url": "https://portal.edu.az",
      "items": []
    }
  ]
}
```

---

## Rendering Logic Guidelines

### 1. Handling Links
Always check the `direct_url` property at every level:
- **Level 1 (Top Bar):** If `direct_url` is not null, render it as an `<a>` tag. If it is null, render it as a button/hover-trigger for the dropdown.
- **Level 2 (Dropdown Titles):** If `direct_url` is not null, render it as a clickable link. If it is null, it acts as a non-clickable header for its `sub_items`.
- **Level 3 (Sub-items):** These are always clickable links using `direct_url`.

### 2. Mega Menu Styling
- When `image_url` is present in a Level 1 item, it is recommended to use it as a visual decoration (background or side image) within that specific mega-menu dropdown.
- If a Level 1 item has many Level 2 items, consider a grid layout (columns).

### 3. Language Switching
When the user changes the site language, re-fetch the menu with the new `lang_code` to get translated titles and updated `direct_url` paths.

### 4. Active State
You can determine the active menu item by comparing the current browser URL with the `direct_url` of the items.

---

## Implementation Example (React)

```tsx
interface SubItem {
  id: number;
  title: string;
  direct_url: string;
}

interface MenuItem {
  id: number;
  title: string;
  direct_url: string | null;
  sub_items: SubItem[];
}

interface MenuHeader {
  id: number;
  title: string;
  image_url: string | null;
  direct_url: string | null;
  items: MenuItem[];
}

// ... in your component
const [menuData, setMenuData] = useState<MenuHeader[]>([]);

useEffect(() => {
  fetch('/api/menu/header/?lang_code=az')
    .then(res => res.json())
    .then(json => setMenuData(json.data));
}, []);
```
