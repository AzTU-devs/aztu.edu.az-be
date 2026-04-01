# Faculty Website Integration

## Public endpoints

- `GET /api/v1/faculty/public/all`
- `GET /api/v1/faculty/{faculty_code}`

## Language selection

- Use query parameter `?lang=az` or `?lang=en`.
- Or use the `Accept-Language` HTTP header.
- Default language is `en`.

## Response structure

### List endpoint

Response contains faculty summary objects with:

- `id`
- `faculty_code`
- `faculty_name`
- `cafedra_count`
- `deputy_dean_count`
- `created_at`
- `updated_at`

### Detail endpoint

The detail response returns a nested `faculty` object with:

- `faculty_code`
- `title`
- `html_content`
- `director`
  - `first_name`
  - `last_name`
  - `father_name`
  - `scientific_degree`
  - `scientific_title`
  - `bio`
  - `email`
  - `phone`
  - `room_number`
  - `profile_image`
  - `working_hours`
  - `scientific_events`
  - `educations`
- `laboratories` (list)
- `research_works` (list)
- `partner_companies` (list)
- `objectives` (list)
- `duties` (list)
- `projects` (list)
- `deputy_deans` (list)
- `scientific_council` (list)
- `workers` (list)

## Example list request

```http
GET /api/v1/faculty/public/all?lang=az
Accept: application/json
```

## Example detail request

```http
GET /api/v1/faculty/123456?lang=en
Accept: application/json
```

## Frontend integration notes

- Use `GET /api/v1/faculty/public/all` to populate faculty cards or list pages.
- Use `GET /api/v1/faculty/{faculty_code}` for faculty detail pages.
- Render `director` data as a profile section with working hours, events, education, email, phone, and image.
- Render `laboratories`, `research_works`, `partner_companies`, `objectives`, `duties`, and `projects` as translated content lists.
- Render `deputy_deans`, `scientific_council`, and `workers` as personnel sections.
- Display only fields that exist in the response to support optional sections.
