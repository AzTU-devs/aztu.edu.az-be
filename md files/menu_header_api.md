# Menu Header API

The Header Menu is a **3-level hierarchy** designed for a mega-menu navigation bar.

| Level | Name | Description |
|---|---|---|
| 1 | `MenuHeader` | Main titles on the top bar (e.g. "Universitet", "Qəbul") |
| 2 | `MenuHeaderItem` | First-level dropdown / column headers |
| 3 | `MenuHeaderSubItem` | Leaf links under a column header |

---

## 🔗 Documentation Links

For detailed integration instructions, please refer to:

- **[Website Frontend Integration Guide (Public)](docs/menu-header-website-integration.md)**  
  *How to fetch and render the menu on the main university website.*

- **[Admin Dashboard Integration Guide (Private)](docs/menu-header-api.md)**  
  *How to perform CRUD operations (Create, Read, Update, Delete) to manage the menu.*

---

## 🚀 Quick Reference (Public API)

**Endpoint:** `GET /api/menu/header/`

**Headers:**
- `Accept-Language: az` (or `en`)

**Response Structure:**
```json
{
  "status_code": 200,
  "data": [
    {
      "id": 1,
      "title": "Universitet",
      "slug": "universitet",
      "image_url": "https://...",
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
        }
      ]
    }
  ]
}
```
