from fastapi import Depends, Form


class CreateFacultyForm:
    def __init__(
        self,
        faculty_name: str = Form(...),
    ):
        self.faculty_name = faculty_name


class CreateFaculty:
    def __init__(
        self,
        az: CreateFacultyForm = Depends(),
        en: CreateFacultyForm = Depends(),
    ):
        self.az = az
        self.en = en

    @classmethod
    def as_form(
        cls,
        az_name: str = Form(...),
        en_name: str = Form(...),
    ):
        az = CreateFacultyForm(faculty_name=az_name)
        en = CreateFacultyForm(faculty_name=en_name)
        return cls(az=az, en=en)


class UpdateFaculty:
    def __init__(
        self,
        az: CreateFacultyForm = Depends(),
        en: CreateFacultyForm = Depends(),
    ):
        self.az = az
        self.en = en

    @classmethod
    def as_form(
        cls,
        az_name: str | None = Form(None),
        en_name: str | None = Form(None),
    ):
        az = CreateFacultyForm(faculty_name=az_name) if az_name is not None else None
        en = CreateFacultyForm(faculty_name=en_name) if en_name is not None else None
        return cls(az=az, en=en)
