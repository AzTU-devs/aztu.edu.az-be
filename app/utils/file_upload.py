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
    # Robust path traversal check
    if os.path.commonpath([STATIC_BASE, target_dir]) != STATIC_BASE:
        logger.error("Path traversal attempt: subdirectory='%s', resolved='%s'", subdirectory, target_dir)
        raise HTTPException(status_code=400, detail="Invalid directory")

    try:
        os.makedirs(target_dir, exist_ok=True)
    except OSError as e:
        logger.error("Failed to create directory %s: %s", target_dir, e)
        raise HTTPException(
            status_code=500,
            detail="Could not create upload directory. Please check permissions."
        )

    file_path = os.path.join(target_dir, filename)

    try:
        with open(file_path, "wb") as f:
            f.write(content)
    except OSError as e:
        logger.error("Failed to write file %s: %s", file_path, e)
        raise HTTPException(
            status_code=500,
            detail="Could not save file. Please check permissions."
        )

    return f"static/{subdirectory}/{filename}"


# Startup check
if not os.path.exists(STATIC_BASE):
    try:
        os.makedirs(STATIC_BASE, exist_ok=True)
        logger.info("Created static base directory at %s", STATIC_BASE)
    except OSError as e:
        logger.error("CRITICAL: Could not create static base directory %s: %s", STATIC_BASE, e)
elif not os.access(STATIC_BASE, os.W_OK):
    logger.warning("WARNING: Static base directory %s is not writable!", STATIC_BASE)
else:
    logger.info("Static base directory %s is ready and writable.", STATIC_BASE)


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