import json
import re
from typing import Optional
from fastapi import Form, UploadFile, File, HTTPException, status


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^\+?[0-9\s\-\(\)]{7,20}$")

CONTACT_REQUIRED_FIELDS = ("email", "phone", "building", "floor", "room")


def _err(field: str, msg: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={"errors": {field: [msg]}},
    )


def _validate_email(value: str) -> str:
    if not EMAIL_RE.match(value):
        raise _err("contact.email", "Invalid email address.")
    return value


def _normalize_phone(value: str) -> str:
    digits = re.sub(r"[\s\-\(\)]", "", value)
    if not PHONE_RE.match(value):
        raise _err("contact.phone", "Invalid phone number format. Expected 7-20 digits, optionally with +, spaces, dashes, parentheses.")
    return digits


def _parse_json_list(raw: str | None, field_name: str, required: bool = False) -> list:
    if not raw:
        if required:
            raise _err(field_name, f"'{field_name}' is required and must be a non-empty JSON array.")
        return []
    try:
        parsed = json.loads(raw)
        if not isinstance(parsed, list):
            raise ValueError
        return parsed
    except (json.JSONDecodeError, ValueError):
        raise _err(field_name, f"'{field_name}' must be a valid JSON array string.")


def _parse_json_object(raw: str | None, field_name: str, required: bool = False) -> dict | None:
    if not raw:
        if required:
            raise _err(field_name, f"'{field_name}' is required and must be a JSON object.")
        return None
    try:
        parsed = json.loads(raw)
        if not isinstance(parsed, dict):
            raise ValueError
        return parsed
    except (json.JSONDecodeError, ValueError):
        raise _err(field_name, f"'{field_name}' must be a valid JSON object string.")


def _validate_contact(obj: dict) -> dict:
    errors: dict[str, list[str]] = {}
    for field in CONTACT_REQUIRED_FIELDS:
        if not obj.get(field):
            errors[f"contact.{field}"] = [f"contact.{field} is required."]
    if errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"errors": errors},
        )
    _validate_email(obj["email"])
    obj["phone"] = _normalize_phone(obj["phone"])
    return obj


def _validate_office_hours(items: list) -> list:
    if not items:
        raise _err("office_hours", "At least 1 office hour entry is required.")
    return items


def _validate_education(items: list) -> list:
    if not items:
        raise _err("education", "At least 1 education entry is required.")
    return items


class CreateEmployee:
    """
    Multipart/form-data schema for creating an employee.

    Translated fields use az_/en_ prefix.
    Nested objects/arrays are sent as JSON strings:
      contact='{"email":"...","phone":"...","building":"...","floor":"...","room":"..."}'
      research='{"scopus_url":"...","orcid_url":"..."}'
      office_hours='[{"day_of_week":"Monday","start_time":"09:00","end_time":"11:00"}]'
      education='[{"degree_level":"PhD","institution_az":"...","institution_en":"...","specialization_az":"...","specialization_en":"...","graduation_year":2015}]'
      courses='[{"course_name_az":"...","course_name_en":"...","education_level":"bachelor"}]'
    """

    def __init__(
        self,
        # Required base
        profile_image: UploadFile,
        faculty_code: str,
        # Required az names
        first_name_az: str,
        last_name_az: str,
        # Optional en names
        first_name_en: Optional[str],
        last_name_en: Optional[str],
        # Optional translated fields
        az_academic_degree: Optional[str],
        en_academic_degree: Optional[str],
        az_academic_title: Optional[str],
        en_academic_title: Optional[str],
        az_position: Optional[str],
        en_position: Optional[str],
        az_scientific_interests: Optional[str],
        en_scientific_interests: Optional[str],
        # Required az biography
        az_biography: str,
        en_biography: Optional[str],
        # Optional
        cafedra_code: Optional[str],
        # Required nested (parsed from JSON strings)
        contact: dict,
        office_hours: list,
        education: list,
        # Optional nested
        research: Optional[dict],
        courses: list,
    ):
        self.profile_image = profile_image
        self.faculty_code = faculty_code
        self.first_name_az = first_name_az
        self.last_name_az = last_name_az
        self.first_name_en = first_name_en
        self.last_name_en = last_name_en
        self.az_academic_degree = az_academic_degree
        self.en_academic_degree = en_academic_degree
        self.az_academic_title = az_academic_title
        self.en_academic_title = en_academic_title
        self.az_position = az_position
        self.en_position = en_position
        self.az_scientific_interests = az_scientific_interests
        self.en_scientific_interests = en_scientific_interests
        self.az_biography = az_biography
        self.en_biography = en_biography
        self.cafedra_code = cafedra_code
        self.contact = contact
        self.office_hours = office_hours
        self.education = education
        self.research = research
        self.courses = courses

    @classmethod
    def as_form(
        cls,
        # Required
        profile_image: UploadFile = File(...),
        faculty_code: str = Form(...),
        first_name_az: str = Form(...),
        last_name_az: str = Form(...),
        az_biography: str = Form(...),
        contact: str = Form(...),
        office_hours: str = Form(...),
        education: str = Form(...),
        # Optional
        first_name_en: Optional[str] = Form(None),
        last_name_en: Optional[str] = Form(None),
        az_academic_degree: Optional[str] = Form(None),
        en_academic_degree: Optional[str] = Form(None),
        az_academic_title: Optional[str] = Form(None),
        en_academic_title: Optional[str] = Form(None),
        az_position: Optional[str] = Form(None),
        en_position: Optional[str] = Form(None),
        az_scientific_interests: Optional[str] = Form(None),
        en_scientific_interests: Optional[str] = Form(None),
        en_biography: Optional[str] = Form(None),
        cafedra_code: Optional[str] = Form(None),
        research: Optional[str] = Form(None),
        courses: Optional[str] = Form(None),
    ):
        contact_obj = _parse_json_object(contact, "contact", required=True)
        _validate_contact(contact_obj)

        oh_list = _parse_json_list(office_hours, "office_hours", required=True)
        _validate_office_hours(oh_list)

        edu_list = _parse_json_list(education, "education", required=True)
        _validate_education(edu_list)

        research_obj = _parse_json_object(research, "research", required=False)
        courses_list = _parse_json_list(courses, "courses", required=False)

        return cls(
            profile_image=profile_image,
            faculty_code=faculty_code,
            first_name_az=first_name_az,
            last_name_az=last_name_az,
            first_name_en=first_name_en,
            last_name_en=last_name_en,
            az_academic_degree=az_academic_degree,
            en_academic_degree=en_academic_degree,
            az_academic_title=az_academic_title,
            en_academic_title=en_academic_title,
            az_position=az_position,
            en_position=en_position,
            az_scientific_interests=az_scientific_interests,
            en_scientific_interests=en_scientific_interests,
            az_biography=az_biography,
            en_biography=en_biography,
            cafedra_code=cafedra_code,
            contact=contact_obj,
            office_hours=oh_list,
            education=edu_list,
            research=research_obj,
            courses=courses_list,
        )


class UpdateEmployee:
    """
    Multipart/form-data schema for updating an employee.
    All fields are optional. Nested arrays replace existing records when provided.
    """

    def __init__(
        self,
        profile_image: Optional[UploadFile],
        faculty_code: Optional[str],
        cafedra_code: Optional[str],
        first_name_az: Optional[str],
        last_name_az: Optional[str],
        first_name_en: Optional[str],
        last_name_en: Optional[str],
        az_academic_degree: Optional[str],
        en_academic_degree: Optional[str],
        az_academic_title: Optional[str],
        en_academic_title: Optional[str],
        az_position: Optional[str],
        en_position: Optional[str],
        az_scientific_interests: Optional[str],
        en_scientific_interests: Optional[str],
        az_biography: Optional[str],
        en_biography: Optional[str],
        contact: Optional[dict],
        research: Optional[dict],
        office_hours: Optional[list],
        education: Optional[list],
        courses: Optional[list],
    ):
        self.profile_image = profile_image
        self.faculty_code = faculty_code
        self.cafedra_code = cafedra_code
        self.first_name_az = first_name_az
        self.last_name_az = last_name_az
        self.first_name_en = first_name_en
        self.last_name_en = last_name_en
        self.az_academic_degree = az_academic_degree
        self.en_academic_degree = en_academic_degree
        self.az_academic_title = az_academic_title
        self.en_academic_title = en_academic_title
        self.az_position = az_position
        self.en_position = en_position
        self.az_scientific_interests = az_scientific_interests
        self.en_scientific_interests = en_scientific_interests
        self.az_biography = az_biography
        self.en_biography = en_biography
        self.contact = contact
        self.research = research
        self.office_hours = office_hours
        self.education = education
        self.courses = courses

    @classmethod
    def as_form(
        cls,
        profile_image: Optional[UploadFile] = File(None),
        faculty_code: Optional[str] = Form(None),
        cafedra_code: Optional[str] = Form(None),
        first_name_az: Optional[str] = Form(None),
        last_name_az: Optional[str] = Form(None),
        first_name_en: Optional[str] = Form(None),
        last_name_en: Optional[str] = Form(None),
        az_academic_degree: Optional[str] = Form(None),
        en_academic_degree: Optional[str] = Form(None),
        az_academic_title: Optional[str] = Form(None),
        en_academic_title: Optional[str] = Form(None),
        az_position: Optional[str] = Form(None),
        en_position: Optional[str] = Form(None),
        az_scientific_interests: Optional[str] = Form(None),
        en_scientific_interests: Optional[str] = Form(None),
        az_biography: Optional[str] = Form(None),
        en_biography: Optional[str] = Form(None),
        contact: Optional[str] = Form(None),
        research: Optional[str] = Form(None),
        office_hours: Optional[str] = Form(None),
        education: Optional[str] = Form(None),
        courses: Optional[str] = Form(None),
    ):
        contact_obj = None
        if contact is not None:
            contact_obj = _parse_json_object(contact, "contact", required=True)
            _validate_contact(contact_obj)

        research_obj = _parse_json_object(research, "research", required=False) if research is not None else None

        oh_list = None
        if office_hours is not None:
            oh_list = _parse_json_list(office_hours, "office_hours", required=True)
            _validate_office_hours(oh_list)

        edu_list = None
        if education is not None:
            edu_list = _parse_json_list(education, "education", required=True)
            _validate_education(edu_list)

        courses_list = _parse_json_list(courses, "courses") if courses is not None else None

        return cls(
            profile_image=profile_image,
            faculty_code=faculty_code,
            cafedra_code=cafedra_code,
            first_name_az=first_name_az,
            last_name_az=last_name_az,
            first_name_en=first_name_en,
            last_name_en=last_name_en,
            az_academic_degree=az_academic_degree,
            en_academic_degree=en_academic_degree,
            az_academic_title=az_academic_title,
            en_academic_title=en_academic_title,
            az_position=az_position,
            en_position=en_position,
            az_scientific_interests=az_scientific_interests,
            en_scientific_interests=en_scientific_interests,
            az_biography=az_biography,
            en_biography=en_biography,
            contact=contact_obj,
            research=research_obj,
            office_hours=oh_list,
            education=edu_list,
            courses=courses_list,
        )
