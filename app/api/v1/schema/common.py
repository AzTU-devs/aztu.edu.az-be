from typing import Annotated, Any, Optional

from pydantic import BeforeValidator, EmailStr, Field


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

# Plain optional text that tolerates blank submissions.
OptionalStr = Annotated[Optional[str], BeforeValidator(blank_to_none)]

# Optional integer that tolerates blank submissions (admin <select> submits "" for "no choice").
OptionalInt = Annotated[Optional[int], BeforeValidator(blank_to_none)]

# Optional link stored verbatim as text — HttpUrl rejects bare domains the admin forms allow.
# max_length is constrained on the inner str: applied to the Optional it raises a TypeError on None.
OptionalUrl = Annotated[
    Optional[Annotated[str, Field(max_length=2048)]], BeforeValidator(blank_to_none)
]
