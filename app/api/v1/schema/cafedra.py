from fastapi import Depends, Form


class CreateCafedraForm:
    def __init__(
        self,
        cafedra_name: str = Form(...),
    ):
        self.cafedra_name = cafedra_name


class CreateCafedra:
    def __init__(
        self,
        faculty_code: str = Form(...),
        az: CreateCafedraForm = Depends(),
        en: CreateCafedraForm = Depends(),
    ):
        self.faculty_code = faculty_code
        self.az = az
        self.en = en

    @classmethod
    def as_form(
        cls,
        faculty_code: str = Form(...),
        az_name: str = Form(...),
        en_name: str = Form(...),
    ):
        az = CreateCafedraForm(cafedra_name=az_name)
        en = CreateCafedraForm(cafedra_name=en_name)
        return cls(faculty_code=faculty_code, az=az, en=en)


class UpdateCafedra:
    def __init__(
        self,
        az: CreateCafedraForm = Depends(),
        en: CreateCafedraForm = Depends(),
    ):
        self.az = az
        self.en = en

    @classmethod
    def as_form(
        cls,
        az_name: str | None = Form(None),
        en_name: str | None = Form(None),
    ):
        az = CreateCafedraForm(cafedra_name=az_name) if az_name is not None else None
        en = CreateCafedraForm(cafedra_name=en_name) if en_name is not None else None
        return cls(az=az, en=en)
