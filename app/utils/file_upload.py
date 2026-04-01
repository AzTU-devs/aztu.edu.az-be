import os
import logging
import secrets
import filetype
from fastapi import UploadFile, HTTPException
from app.core.config import settings

logger = logging.getLogger("aztu.upload")

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
    content = await upload.read()

    # 1. Size check
    limit = max_size or settings.MAX_UPLOAD_SIZE_BYTES
    if len(content) > limit:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max {limit // (1024 * 1024)} MB",
        )

    # 2. Detect MIME (SAFE, no system dependency)
    kind = filetype.guess(content)

    if kind is None:
        raise HTTPException(status_code=415, detail="Unknown file type")

    detected_mime = kind.mime

    if detected_mime not in allowed_mimes:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{detected_mime}'",
        )

    ext = allowed_mimes[detected_mime]

    # 3. Random filename
    filename = f"{secrets.token_hex(16)}.{ext}"

    # 4. Safe path
    target_dir = os.path.abspath(os.path.join(STATIC_BASE, subdirectory))
    if not target_dir.startswith(STATIC_BASE):
        logger.error("Path traversal attempt: %s", subdirectory)
        raise HTTPException(status_code=400, detail="Invalid directory")

    os.makedirs(target_dir, exist_ok=True)

    file_path = os.path.join(target_dir, filename)

    with open(file_path, "wb") as f:
        f.write(content)

    return f"static/{subdirectory}/{filename}"


def safe_delete_file(relative_path: str) -> None:
    if not relative_path:
        return

    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    resolved = os.path.abspath(os.path.join(app_dir, relative_path))

    if not resolved.startswith(STATIC_BASE):
        logger.error("Path traversal attempt: %s", relative_path)
        return

    if os.path.isfile(resolved):
        try:
            os.remove(resolved)
        except OSError as exc:
            logger.warning("Delete failed %s: %s", resolved, exc)