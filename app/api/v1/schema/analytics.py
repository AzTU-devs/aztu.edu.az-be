from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator

MAX_PATH_LENGTH = 512


def truncate_path(value: Any) -> str:
    """Clamp the reported path instead of 422-ing on it.

    This endpoint fires on every page view, so it is deliberately total: an
    absurdly long path is truncated and anything that is not a string degrades
    to "/" rather than surfacing a validation error on the public site.
    """
    if isinstance(value, str):
        return value.strip()[:MAX_PATH_LENGTH] or "/"
    return "/"


TrackedPath = Annotated[str, BeforeValidator(truncate_path)]


class VisitTrackRequest(BaseModel):
    path: TrackedPath = "/"
