from typing import Annotated, Any, Optional

from pydantic import BeforeValidator, EmailStr


def blank_to_none(value: Any) -> Any:
    """Coerce empty / whitespace-only strings to None.

    Front-end forms commonly submit "" for optional fields that were left blank.
    Without this, a field like ``email: EmailStr | None`` would raise a 422 on "".
    """
    if isinstance(value, str) and value.strip() == "":
        return None
    return value


# EmailStr that tolerates blank submissions (treats "" as None instead of failing validation).
OptionalEmail = Annotated[Optional[EmailStr], BeforeValidator(blank_to_none)]
