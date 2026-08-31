from typing import Optional

from fastapi import Form, UploadFile
from pydantic import BaseModel


def _blank_to_none(value: Optional[str]) -> Optional[str]:
    """Admin forms submit "" for optional fields left blank."""
    if isinstance(value, str) and value.strip() == "":
        return None
    return value


def _parse_flag(value: Optional[str]) -> bool:
    """Multipart booleans arrive as strings ("true" / "false" / "" / missing)."""
    value = _blank_to_none(value)
    if value is None:
        return False
    return value.strip().lower() in ("true", "1", "yes", "on")


class HonoraryDoctorCreate(BaseModel):
    image: Optional[UploadFile] = None
    az_full_name: str
    en_full_name: str
    az_description: Optional[str] = None
    en_description: Optional[str] = None

    model_config = {"arbitrary_types_allowed": True}

    @classmethod
    def as_form(
        cls,
        az_full_name: str = Form(...),
        en_full_name: str = Form(...),
        az_description: Optional[str] = Form(None),
        en_description: Optional[str] = Form(None),
        image: Optional[UploadFile] = None,
    ) -> "HonoraryDoctorCreate":
        return cls(
            image=image,
            az_full_name=az_full_name.strip(),
            en_full_name=en_full_name.strip(),
            az_description=_blank_to_none(az_description),
            en_description=_blank_to_none(en_description),
        )


class HonoraryDoctorUpdate(HonoraryDoctorCreate):
    remove_image: bool = False

    @classmethod
    def as_form(
        cls,
        az_full_name: str = Form(...),
        en_full_name: str = Form(...),
        az_description: Optional[str] = Form(None),
        en_description: Optional[str] = Form(None),
        remove_image: Optional[str] = Form(None),
        image: Optional[UploadFile] = None,
    ) -> "HonoraryDoctorUpdate":
        return cls(
            image=image,
            az_full_name=az_full_name.strip(),
            en_full_name=en_full_name.strip(),
            az_description=_blank_to_none(az_description),
            en_description=_blank_to_none(en_description),
            remove_image=_parse_flag(remove_image),
        )


class ReOrderHonoraryDoctor(BaseModel):
    """Full, ordered list of ids — position in the array is the new order."""

    ids: list[int]
