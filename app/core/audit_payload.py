"""Sanitising and sizing of audited request/response bodies.

The activity log stores what was sent and what came back. That is genuinely
useful for forensics and genuinely dangerous stored raw, so nothing reaches the
table without passing through here first.

Three rules, in order of importance:

1. **Secrets never land.** ``redact`` walks the whole structure and replaces the
   value of any secret-looking key at any depth. It is keyed on a superset of
   ``SECRET_FIELD_NAMES`` plus a substring check, so ``user_password`` and
   ``X-Api-Key`` are caught as well as exact matches.
2. **Files are never buffered.** A multipart body records field names and each
   file's name and size — never its contents. A 50 MB upload must not become a
   50 MB log row.
3. **Size is bounded.** Anything past ``MAX_BODY_CHARS`` is truncated with a
   marker, so one pathological payload cannot dominate the table.

Also derives the coarse client type ("browser", "curl", …) from a User-Agent.
That is presentation, so it is computed at read time and never stored — the
classification can be improved later with no backfill.
"""

import json
import re
from typing import Any, Optional


# Exact field names that can never be logged. Defined here, with the rest of the
# payload-safety rules, and re-exported by `auth_dependency` for its own use.
SECRET_FIELD_NAMES = frozenset(
    {
        "password", "new_password", "current_password", "confirm_password",
        "hashed_password", "token", "access_token", "refresh_token", "api_key", "secret",
    }
)

# Serialised size cap per body. Comfortably fits a real admin form; a bulk
# import or a base64 blob gets truncated instead of bloating the table.
MAX_BODY_CHARS = 8_000

REDACTED = "[redacted]"
TRUNCATED_KEY = "_truncated"

# Substrings that make a key secret whatever else it is called, so
# `user_password` and `x-api-key` are caught alongside the exact names.
_SECRET_SUBSTRINGS = ("password", "token", "secret", "api_key", "apikey", "authorization")


def _is_secret(key: str) -> bool:
    lowered = key.lower()
    if lowered in SECRET_FIELD_NAMES:
        return True
    normalised = lowered.replace("-", "_")
    return any(needle in normalised for needle in _SECRET_SUBSTRINGS)


def redact(value: Any, depth: int = 0) -> Any:
    """Same shape, with every secret-looking value replaced.

    Depth is bounded so a hostile or cyclic-looking payload cannot spin here.
    """
    if depth > 12:
        return "[too deep]"
    if isinstance(value, dict):
        return {
            key: (REDACTED if _is_secret(str(key)) else redact(item, depth + 1))
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item, depth + 1) for item in value[:200]]
    return value


def _fit(payload: Any) -> Any:
    """Return `payload` if it serialises within the cap, else a truncated stand-in."""
    try:
        encoded = json.dumps(payload, ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        return {TRUNCATED_KEY: True, "reason": "not serialisable"}

    if len(encoded) <= MAX_BODY_CHARS:
        return payload
    return {
        TRUNCATED_KEY: True,
        "reason": f"body exceeded {MAX_BODY_CHARS} characters",
        "size": len(encoded),
        "preview": encoded[:1_000],
    }


def from_json_bytes(raw: bytes) -> Optional[Any]:
    """Sanitised JSON body, or None when there is nothing usable to store."""
    if not raw:
        return None
    try:
        parsed = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Not JSON — record that something was sent without keeping the bytes.
        return _fit({TRUNCATED_KEY: True, "reason": "non-JSON body", "size": len(raw)})
    return _fit(redact(parsed))


def from_form(fields: dict, files: list) -> Optional[Any]:
    """Sanitised summary of a multipart/form body. File contents are never read."""
    if not fields and not files:
        return None
    payload: dict = {}
    if fields:
        payload["fields"] = redact(fields)
    if files:
        payload["files"] = files
    return _fit(payload)


# ── Client classification (read-time only) ─────────────────────────────────────

_CLIENT_PATTERNS: tuple[tuple[str, str], ...] = (
    ("curl", r"^curl/"),
    ("wget", r"^wget/"),
    ("postman", r"postmanruntime"),
    ("insomnia", r"insomnia"),
    ("python", r"^(python-requests|python-urllib|httpx|aiohttp)"),
    ("node", r"^(node-fetch|axios|got|undici)"),
    ("java", r"^(java|okhttp|apache-httpclient)"),
    ("go", r"^go-http-client"),
    ("bot", r"(bot|crawler|spider)"),
    ("browser", r"(mozilla|chrome|safari|firefox|edg/|opera)"),
)


def classify_client(user_agent: Optional[str]) -> str:
    """Coarse client type from a User-Agent.

    Deliberately advisory: a User-Agent is client-supplied and trivial to spoof,
    so this says what the caller *claimed* to be, never what it provably was.
    """
    if not user_agent or not user_agent.strip():
        return "unknown"
    agent = user_agent.strip().lower()
    for name, pattern in _CLIENT_PATTERNS:
        if re.search(pattern, agent):
            return name
    return "other"
