import os
import logging
import secrets
import magic
from fastapi import UploadFile, HTTPException
from app.core.config import settings

logger = logging.getLogger("aztu.upload")

# Absolute path to the static directory — all uploads must resolve inside here
STATIC_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))

ALLOWED_IMAGE_MIMES: dict[str, str] = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
    "image/gif": "gif",
}

ALLOWED_VIDEO_MIMES: dict[str, str] = {
    "video/mp4": "mp4",
    "video/webm": "webm",
}


async def save_upload(
    upload: UploadFile,
    subdirectory: str,
    allowed_mimes: dict[str, str],
    max_size: int | None = None,
) -> str:
    """
    Safely validate and save an uploaded file.

    - Detects MIME type from actual file bytes (not extension).
    - Enforces size limit.
    - Saves with a cryptographically random filename.
    - Prevents path traversal by resolving absolute path.

    Returns the relative path stored in DB: "static/{subdirectory}/{random}.{ext}"
    """
    content = await upload.read()

    # 1. Enforce file size limit
    limit = max_size or settings.MAX_UPLOAD_SIZE_BYTES
    if len(content) > limit:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum allowed size is {limit // (1024 * 1024)} MB.",
        )

    # 2. Detect MIME from actual bytes — never trust the extension or Content-Type header
    try:
        detected_mime = magic.from_buffer(content, mime=True)
    except Exception:
        raise HTTPException(status_code=415, detail="Could not determine file type.")

    if detected_mime not in allowed_mimes:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{detected_mime}'. "
            f"Allowed: {', '.join(allowed_mimes.keys())}",
        )

    ext = allowed_mimes[detected_mime]

    # 3. Generate a cryptographically random filename — never use user-supplied names
    filename = f"{secrets.token_hex(16)}.{ext}"

    # 4. Resolve target directory and assert it is inside STATIC_BASE (path traversal guard)
    target_dir = os.path.abspath(os.path.join(STATIC_BASE, subdirectory))
    if not target_dir.startswith(STATIC_BASE + os.sep) and target_dir != STATIC_BASE:
        logger.error("Path traversal attempt detected: subdirectory=%s", subdirectory)
        raise HTTPException(status_code=400, detail="Invalid upload directory.")

    os.makedirs(target_dir, exist_ok=True)
    file_path = os.path.join(target_dir, filename)

    with open(file_path, "wb") as f:
        f.write(content)

    return f"static/{subdirectory}/{filename}"


def safe_delete_file(relative_path: str) -> None:
    """
    Safely delete a file that was stored relative to app/static.
    Prevents path traversal by verifying the resolved path stays within STATIC_BASE.
    Silently ignores missing files; logs and skips attempted traversals.
    """
    if not relative_path:
        return

    # relative_path is stored as "static/news/abc123.jpg" — resolve inside app/
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    resolved = os.path.abspath(os.path.join(app_dir, relative_path))

    if not resolved.startswith(STATIC_BASE + os.sep) and not resolved.startswith(STATIC_BASE):
        logger.error(
            "Path traversal attempt in safe_delete_file: path=%s resolved=%s",
            relative_path,
            resolved,
        )
        return

    if os.path.isfile(resolved):
        try:
            os.remove(resolved)
        except OSError as exc:
            logger.warning("Could not delete file %s: %s", resolved, exc)
