import json
import re
from typing import Optional
from fastapi import Form, UploadFile, File, HTTPException, status


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^\+?[0-9\s\-\(\)]{7,20}$")


def _validate_email(value: str | None) -> str | None:
    if value and not EMAIL_RE.match(value):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid email address.",
        )
    return value


def _validate_phone(value: str | None) -> str | None:
    if value and not PHONE_RE.match(value):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid phone number format.",
        )
    return value


def _parse_json_field(raw: str | None, field_name: str) -> list:
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
        if not isinstance(parsed, list):
            raise ValueError
        return parsed
    except (json.JSONDecodeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"'{field_name}' must be a valid JSON array string.",
        )


class CreateEmployee:
    """
    Multipart/form-data schema for creating an employee.

    Nested arrays (education, courses, office_hours) are sent as JSON strings:
      education='[{"degree_level":"PhD","institution":"AzTU","specialization":"CS","graduation_year":2010}]'
      courses='[{"course_name":"Data Structures","education_level":"bachelor"}]'
      office_hours='[{"day_of_week":"Monday","start_time":"09:00","end_time":"11:00"}]'
    """

    def __init__(
        self,
        first_name: str,
        last_name: str,
        az_biography: Optional[str],
        en_biography: Optional[str],
        profile_image: Optional[UploadFile],
        academic_degree: Optional[str],
        academic_title: Optional[str],
        position: Optional[str],
        faculty_code: Optional[str],
        cafedra_code: Optional[str],
        email: Optional[str],
        phone: Optional[str],
        building: Optional[str],
        floor: Optional[str],
        room: Optional[str],
        scopus_url: Optional[str],
        google_scholar_url: Optional[str],
        orcid_url: Optional[str],
        researchgate_url: Optional[str],
        academia_url: Optional[str],
        scientific_interests: Optional[str],
        publications: Optional[str],
        education: list,
        courses: list,
        office_hours: list,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = f"{first_name} {last_name}"
        self.az_biography = az_biography
        self.en_biography = en_biography
        self.profile_image = profile_image
        self.academic_degree = academic_degree
        self.academic_title = academic_title
        self.position = position
        self.faculty_code = faculty_code
        self.cafedra_code = cafedra_code
        self.email = email
        self.phone = phone
        self.building = building
        self.floor = floor
        self.room = room
        self.scopus_url = scopus_url
        self.google_scholar_url = google_scholar_url
        self.orcid_url = orcid_url
        self.researchgate_url = researchgate_url
        self.academia_url = academia_url
        self.scientific_interests = scientific_interests
        self.publications = publications
        self.education = education
        self.courses = courses
        self.office_hours = office_hours

    @classmethod
    def as_form(
        cls,
        first_name: str = Form(...),
        last_name: str = Form(...),
        az_biography: Optional[str] = Form(None),
        en_biography: Optional[str] = Form(None),
        profile_image: Optional[UploadFile] = File(None),
        academic_degree: Optional[str] = Form(None),
        academic_title: Optional[str] = Form(None),
        position: Optional[str] = Form(None),
        faculty_code: Optional[str] = Form(None),
        cafedra_code: Optional[str] = Form(None),
        email: Optional[str] = Form(None),
        phone: Optional[str] = Form(None),
        building: Optional[str] = Form(None),
        floor: Optional[str] = Form(None),
        room: Optional[str] = Form(None),
        scopus_url: Optional[str] = Form(None),
        google_scholar_url: Optional[str] = Form(None),
        orcid_url: Optional[str] = Form(None),
        researchgate_url: Optional[str] = Form(None),
        academia_url: Optional[str] = Form(None),
        scientific_interests: Optional[str] = Form(None),
        publications: Optional[str] = Form(None),
        education: Optional[str] = Form(None),
        courses: Optional[str] = Form(None),
        office_hours: Optional[str] = Form(None),
    ):
        return cls(
            first_name=first_name,
            last_name=last_name,
            az_biography=az_biography,
            en_biography=en_biography,
            profile_image=profile_image,
            academic_degree=academic_degree,
            academic_title=academic_title,
            position=position,
            faculty_code=faculty_code,
            cafedra_code=cafedra_code,
            email=_validate_email(email),
            phone=_validate_phone(phone),
            building=building,
            floor=floor,
            room=room,
            scopus_url=scopus_url,
            google_scholar_url=google_scholar_url,
            orcid_url=orcid_url,
            researchgate_url=researchgate_url,
            academia_url=academia_url,
            scientific_interests=scientific_interests,
            publications=publications,
            education=_parse_json_field(education, "education"),
            courses=_parse_json_field(courses, "courses"),
            office_hours=_parse_json_field(office_hours, "office_hours"),
        )


class UpdateEmployee:
    """
    Multipart/form-data schema for updating an employee.
    All fields are optional. Nested arrays replace existing records when provided.
    """

    def __init__(
        self,
        first_name: Optional[str],
        last_name: Optional[str],
        az_biography: Optional[str],
        en_biography: Optional[str],
        profile_image: Optional[UploadFile],
        academic_degree: Optional[str],
        academic_title: Optional[str],
        position: Optional[str],
        faculty_code: Optional[str],
        cafedra_code: Optional[str],
        email: Optional[str],
        phone: Optional[str],
        building: Optional[str],
        floor: Optional[str],
        room: Optional[str],
        scopus_url: Optional[str],
        google_scholar_url: Optional[str],
        orcid_url: Optional[str],
        researchgate_url: Optional[str],
        academia_url: Optional[str],
        scientific_interests: Optional[str],
        publications: Optional[str],
        education: Optional[list],
        courses: Optional[list],
        office_hours: Optional[list],
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.az_biography = az_biography
        self.en_biography = en_biography
        self.profile_image = profile_image
        self.academic_degree = academic_degree
        self.academic_title = academic_title
        self.position = position
        self.faculty_code = faculty_code
        self.cafedra_code = cafedra_code
        self.email = email
        self.phone = phone
        self.building = building
        self.floor = floor
        self.room = room
        self.scopus_url = scopus_url
        self.google_scholar_url = google_scholar_url
        self.orcid_url = orcid_url
        self.researchgate_url = researchgate_url
        self.academia_url = academia_url
        self.scientific_interests = scientific_interests
        self.publications = publications
        self.education = education
        self.courses = courses
        self.office_hours = office_hours

    @classmethod
    def as_form(
        cls,
        first_name: Optional[str] = Form(None),
        last_name: Optional[str] = Form(None),
        az_biography: Optional[str] = Form(None),
        en_biography: Optional[str] = Form(None),
        profile_image: Optional[UploadFile] = File(None),
        academic_degree: Optional[str] = Form(None),
        academic_title: Optional[str] = Form(None),
        position: Optional[str] = Form(None),
        faculty_code: Optional[str] = Form(None),
        cafedra_code: Optional[str] = Form(None),
        email: Optional[str] = Form(None),
        phone: Optional[str] = Form(None),
        building: Optional[str] = Form(None),
        floor: Optional[str] = Form(None),
        room: Optional[str] = Form(None),
        scopus_url: Optional[str] = Form(None),
        google_scholar_url: Optional[str] = Form(None),
        orcid_url: Optional[str] = Form(None),
        researchgate_url: Optional[str] = Form(None),
        academia_url: Optional[str] = Form(None),
        scientific_interests: Optional[str] = Form(None),
        publications: Optional[str] = Form(None),
        education: Optional[str] = Form(None),
        courses: Optional[str] = Form(None),
        office_hours: Optional[str] = Form(None),
    ):
        return cls(
            first_name=first_name,
            last_name=last_name,
            az_biography=az_biography,
            en_biography=en_biography,
            profile_image=profile_image,
            academic_degree=academic_degree,
            academic_title=academic_title,
            position=position,
            faculty_code=faculty_code,
            cafedra_code=cafedra_code,
            email=_validate_email(email),
            phone=_validate_phone(phone),
            building=building,
            floor=floor,
            room=room,
            scopus_url=scopus_url,
            google_scholar_url=google_scholar_url,
            orcid_url=orcid_url,
            researchgate_url=researchgate_url,
            academia_url=academia_url,
            scientific_interests=scientific_interests,
            publications=publications,
            education=_parse_json_field(education, "education") if education is not None else None,
            courses=_parse_json_field(courses, "courses") if courses is not None else None,
            office_hours=_parse_json_field(office_hours, "office_hours") if office_hours is not None else None,
        )
