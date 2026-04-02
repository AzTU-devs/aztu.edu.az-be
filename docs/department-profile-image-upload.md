# Department Module — Profile Image Upload Guide (Admin)

This guide explains how to handle profile image uploads for Department Directors and Workers in the admin dashboard.

## 1. Overview

Profile images for both directors and workers are handled via separate `PUT` endpoints that accept `multipart/form-data`. This allows for efficient file handling and is consistent with other modules like Faculties and Employees.

The `profile_image` field in the main department JSON payload (GET/POST/PUT) contains the relative path to the image (e.g., `static/department-directors/abc123.jpg`).

---

## 2. Director Profile Image

### Endpoint
`PUT /api/department/{department_code}/director/image`

### Request
- **Method:** `PUT`
- **Headers:** `Authorization: Bearer <token>`
- **Content-Type:** `multipart/form-data`
- **Body:** `image` (File)

### Response (`200 OK`)
```json
{
  "status_code": 200,
  "message": "Director image uploaded successfully.",
  "data": {
    "profile_image": "static/department-directors/585966_random_hash.jpg"
  }
}
```

### Usage in Frontend
1. Create or select a department.
2. If the department has a director, show an "Upload Photo" button.
3. Upon file selection, call the endpoint above.
4. The returned `profile_image` path should be stored/displayed by prepending the API base URL.

---

## 3. Worker Profile Image

### Endpoint
`PUT /api/department/workers/{worker_id}/image`

### Request
- **Method:** `PUT`
- **Headers:** `Authorization: Bearer <token>`
- **Content-Type:** `multipart/form-data`
- **Body:** `image` (File)

### Response (`200 OK`)
```json
{
  "status_code": 200,
  "message": "Worker image uploaded successfully.",
  "data": {
    "profile_image": "static/department-workers/646000_random_hash.png"
  }
}
```

### Usage in Frontend
1. The `worker_id` is available in the `workers` list when fetching department details.
2. For each worker card, provide an "Upload Photo" button.
3. Upon file selection, call the endpoint with the specific `worker_id`.

---

## 4. Handling Images in Create/Update Payloads

When calling `POST /api/department/create` or `PUT /api/department/{department_code}`, you can now include the `profile_image` path in the JSON payload. This is important during **updates** to ensure existing images are not lost when worker lists are replaced.

### Example Payload Fragment
```json
{
  "director": {
    "first_name": "Əli",
    "last_name": "Həsənov",
    "profile_image": "static/department-directors/abc.jpg",
    ...
  },
  "workers": [
    {
      "first_name": "Nigar",
      "last_name": "Quliyeva",
      "profile_image": "static/department-workers/xyz.png",
      ...
    }
  ]
}
```

**Recommendation:** 
- When updating a department, always send back the `profile_image` path you received from the `GET` request. 
- If a new image is uploaded via the separate endpoint, update your local state with the new path returned by that endpoint before sending the final `PUT` to update the department.

---

## 5. Technical Details

- **Accepted Formats:** JPEG, PNG, WebP, GIF.
- **Max Size:** 5MB (configured in backend).
- **Storage:** Files are stored in `static/department-directors/` and `static/department-workers/`.
- **Path Resolution:** The backend returns a relative path. The frontend should prepend the API base domain (e.g., `https://api.aztu.edu.az/`) to render the image.
