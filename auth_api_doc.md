# Auth API Documentation

Base path: `/api/v1/auth`

---

## Endpoints

### POST `/api/v1/auth/login`

Authenticates a user and returns an access token. Sets a `refresh_token` httpOnly cookie.

**Rate limit:** 5 requests/minute per IP.

**Request body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response `200`:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

**Set-Cookie (automatic):**
```
refresh_token=<token>; HttpOnly; SameSite=Strict; Path=/api/auth; Max-Age=604800
```

**Errors:**

| Status | Detail |
|--------|--------|
| `401` | `"Invalid username or password"` |
| `403` | `"Account is disabled"` |
| `429` | Too many requests |

---

### POST `/api/v1/auth/refresh`

Issues a new access token using the `refresh_token` cookie. Rotates the refresh token (old one is invalidated).

**Request:** No body required. The `refresh_token` cookie must be present (sent automatically by the browser).

**Response `200`:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

**Set-Cookie (automatic):** New rotated `refresh_token` cookie replaces the old one.

**Errors:**

| Status | Detail |
|--------|--------|
| `401` | `"Refresh token missing"` |
| `401` | `"Invalid or expired refresh token"` |
| `401` | `"Session not found or revoked"` |
| `401` | `"Session invalidated due to token reuse"` |

> **Security note:** If a previously used refresh token is replayed, the session is fully invalidated and the user must log in again.

---

### POST `/api/v1/auth/logout`

Revokes the current session and clears the `refresh_token` cookie.

**Request:** No body required. The `refresh_token` cookie must be present.

**Response `204`:** No content.

> Always returns `204` regardless of whether the token was valid — the cookie is cleared either way.

---

## Token Details

| Token | Storage | Lifetime | Notes |
|-------|---------|----------|-------|
| Access token | Memory (JS variable) | 15 minutes | Sent as `Authorization: Bearer <token>` header |
| Refresh token | httpOnly cookie | 7 days | Managed by browser automatically; not accessible via JS |

---

## Integration Guide

### 1. Login

```js
const res = await fetch('/api/v1/auth/login', {
  method: 'POST',
  credentials: 'include',          // required for the cookie to be set
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, password }),
});
const { access_token } = await res.json();
// Store access_token in memory (not localStorage)
```

### 2. Authenticated requests

```js
await fetch('/api/v1/some-protected-route', {
  headers: { Authorization: `Bearer ${access_token}` },
  credentials: 'include',
});
```

### 3. Refresh access token

Call this when any request returns `401` (access token expired).

```js
const res = await fetch('/api/v1/auth/refresh', {
  method: 'POST',
  credentials: 'include',          // sends the refresh_token cookie
});
if (res.ok) {
  const { access_token } = await res.json();
  // Update stored access_token and retry original request
} else {
  // Refresh failed — redirect to login
}
```

### 4. Logout

```js
await fetch('/api/v1/auth/logout', {
  method: 'POST',
  credentials: 'include',
});
// Clear access_token from memory and redirect to login
```

---

## Notes

- `credentials: 'include'` is required on all requests so the browser sends and receives the `refresh_token` cookie.
- Do **not** store the access token in `localStorage` or `sessionStorage` — keep it in memory to reduce XSS risk.
- The refresh token is `httpOnly` and cannot be read by JavaScript.
- In production the cookie is `Secure` (HTTPS only).
