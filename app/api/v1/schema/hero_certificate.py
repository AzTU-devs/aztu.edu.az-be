from datetime import date
from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile, Form, HTTPException, status


def _blank_to_none(value: Optional[str]) -> Optional[str]:
    """Admin forms submit "" for optional fields that were left blank.

    Without this every blank optional Form(...) field would either be stored as an
    empty string or blow up validation with a 422.
    """
    if isinstance(value, str) and value.strip() == "":
        return None
    return value


def _parse_issued_date(value: Optional[str]) -> Optional[date]:
    """Parse a "YYYY-MM-DD" form string into a date. Blank / missing -> None."""
    value = _blank_to_none(value)
    if value is None:
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid issued_date format. Expected YYYY-MM-DD."
        )


def _parse_flag(value: Optional[str]) -> bool:
    """Multipart booleans arrive as strings ("true" / "false" / "" / missing)."""
    value = _blank_to_none(value)
    if value is None:
        return False
    return value.strip().lower() in ("true", "1", "yes", "on")


class HeroCertificateTranslationForm:
    def __init__(
        self,
        title: str = Form(...),
        kicker: Optional[str] = Form(None),
        signer: Optional[str] = Form(None)
    ):
        self.title = title
        self.kicker = _blank_to_none(kicker)
        self.signer = _blank_to_none(signer)


class HeroCertificateCreate:
    def __init__(
        self,
        rank_label: str,
        family: str,
        issued_date: Optional[date],
        external_url: Optional[str],
        image: Optional[UploadFile],
        document: Optional[UploadFile],
        az: HeroCertificateTranslationForm,
        en: HeroCertificateTranslationForm
    ):
        self.rank_label = rank_label
        self.family = family
        self.issued_date = issued_date
        self.external_url = external_url
        self.image = image
        self.document = document
        self.az = az
        self.en = en

    @classmethod
    def as_form(
        cls,
        rank_label: str = Form(...),
        family: str = Form(...),
        issued_date: Optional[str] = Form(None),
        external_url: Optional[str] = Form(None),
        image: Optional[UploadFile] = Form(None),
        document: Optional[UploadFile] = Form(None),
        az_title: str = Form(...),
        en_title: str = Form(...),
        az_kicker: Optional[str] = Form(None),
        en_kicker: Optional[str] = Form(None),
        az_signer: Optional[str] = Form(None),
        en_signer: Optional[str] = Form(None)
    ):
        az = HeroCertificateTranslationForm(
            title=az_title,
            kicker=az_kicker,
            signer=az_signer
        )
        en = HeroCertificateTranslationForm(
            title=en_title,
            kicker=en_kicker,
            signer=en_signer
        )
        return cls(
            rank_label=rank_label,
            family=family,
            issued_date=_parse_issued_date(issued_date),
            external_url=_blank_to_none(external_url),
            image=image,
            document=document,
            az=az,
            en=en
        )


class HeroCertificateUpdate:
    def __init__(
        self,
        rank_label: str,
        family: str,
        issued_date: Optional[date],
        external_url: Optional[str],
        image: Optional[UploadFile],
        document: Optional[UploadFile],
        remove_image: bool,
        remove_document: bool,
        az: HeroCertificateTranslationForm,
        en: HeroCertificateTranslationForm
    ):
        self.rank_label = rank_label
        self.family = family
        self.issued_date = issued_date
        self.external_url = external_url
        self.image = image
        self.document = document
        self.remove_image = remove_image
        self.remove_document = remove_document
        self.az = az
        self.en = en

    @classmethod
    def as_form(
        cls,
        rank_label: str = Form(...),
        family: str = Form(...),
        issued_date: Optional[str] = Form(None),
        external_url: Optional[str] = Form(None),
        image: Optional[UploadFile] = Form(None),
        document: Optional[UploadFile] = Form(None),
        remove_image: Optional[str] = Form(None),
        remove_document: Optional[str] = Form(None),
        az_title: str = Form(...),
        en_title: str = Form(...),
        az_kicker: Optional[str] = Form(None),
        en_kicker: Optional[str] = Form(None),
        az_signer: Optional[str] = Form(None),
        en_signer: Optional[str] = Form(None)
    ):
        az = HeroCertificateTranslationForm(
            title=az_title,
            kicker=az_kicker,
            signer=az_signer
        )
        en = HeroCertificateTranslationForm(
            title=en_title,
            kicker=en_kicker,
            signer=en_signer
        )
        return cls(
            rank_label=rank_label,
            family=family,
            issued_date=_parse_issued_date(issued_date),
            external_url=_blank_to_none(external_url),
            image=image,
            document=document,
            remove_image=_parse_flag(remove_image),
            remove_document=_parse_flag(remove_document),
            az=az,
            en=en
        )


class ReOrderHeroCertificate(BaseModel):
    certificate_id: int
    new_order: int
