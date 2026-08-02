"""Offices & Centres ("Ofis və Mərkəzlər").

Unlike the About pages — a fixed set of seeded documents — an office is a
creatable record: the dashboard adds and removes them, and each one carries the
same rich structure (an About section, goals, core functions, a director with
an education history, a staff roster and contact details).

Language-neutral facts (a slug, a phone number, an ordering, an image path)
live on the row; anything a translator would touch lives on the ``*_tr`` sibling
keyed by ``lang_code``.
"""

from app.core.database import Base
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship


class Office(Base):
    """One office or centre under Management → Offices and Centres."""

    __tablename__ = "offices"

    id = Column(Integer, primary_key=True, index=True)
    # Generated from the name on create; the public site addresses the office by
    # these, per language. Unique so two centres never collide on a URL.
    slug_az = Column(String(255), unique=True)
    slug_en = Column(String(255), unique=True)
    display_order = Column(Integer, nullable=False, default=0)
    # False keeps the office out of the public API while it is being filled in.
    is_active = Column(Boolean, nullable=False, default=False)

    # ── Director contact — language-neutral. ─────────────────────────────────
    director_phone = Column(String(100))
    # Optional internal extension.
    director_phone_code = Column(String(50))
    director_email = Column(String(255))
    # Portrait: an uploaded file's path or a pasted URL.
    director_image_url = Column(String(2048))

    # ── Office contact — language-neutral. ───────────────────────────────────
    contact_phone = Column(String(100))
    contact_phone_code = Column(String(50))
    contact_email = Column(String(255))

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    translations = relationship(
        "OfficeTr",
        back_populates="office",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    functions = relationship(
        "OfficeFunction",
        back_populates="office",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="OfficeFunction.display_order",
    )
    educations = relationship(
        "OfficeEducation",
        back_populates="office",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="OfficeEducation.display_order",
    )
    staff = relationship(
        "OfficeStaff",
        back_populates="office",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="OfficeStaff.display_order",
    )


class OfficeTr(Base):
    __tablename__ = "office_tr"
    __table_args__ = (
        UniqueConstraint("office_id", "lang_code", name="uq_office_tr_office_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    office_id = Column(Integer, ForeignKey("offices.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(10), nullable=False)

    # Hero: the office name and its short description (rich text).
    name = Column(String(500))
    short_description = Column(Text)

    # "About" section: a heading and rich body.
    about_title = Column(String(500))
    about_text = Column(Text)

    # Goals: a heading plus an ordered set of one-line goal strings.
    goal_title = Column(String(500))
    goals = Column(JSONB)

    # Core functions: just the heading here; the cards live on OfficeFunction.
    functions_title = Column(String(500))

    # Director: the section label ("Şöbə müdiri") and the person's details.
    director_title = Column(String(500))
    director_name = Column(String(255))
    director_surname = Column(String(255))
    director_position = Column(String(500))
    director_bio = Column(Text)
    director_room = Column(String(255))
    director_work_hours = Column(String(500))

    # Staff: just the heading; the people live on OfficeStaff.
    staff_title = Column(String(500))

    # Office contact, per language.
    contact_room = Column(String(255))
    contact_work_hours = Column(String(500))

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    office = relationship("Office", back_populates="translations")


class OfficeFunction(Base):
    """One "core function" card — a title and a rich description."""

    __tablename__ = "office_functions"

    id = Column(Integer, primary_key=True, index=True)
    office_id = Column(Integer, ForeignKey("offices.id", ondelete="CASCADE"), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    office = relationship("Office", back_populates="functions")
    translations = relationship(
        "OfficeFunctionTr",
        back_populates="function",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class OfficeFunctionTr(Base):
    __tablename__ = "office_function_tr"
    __table_args__ = (
        UniqueConstraint("function_id", "lang_code", name="uq_office_function_tr_fn_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    function_id = Column(
        Integer, ForeignKey("office_functions.id", ondelete="CASCADE"), nullable=False
    )
    lang_code = Column(String(10), nullable=False)

    title = Column(String(500))
    description = Column(Text)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    function = relationship("OfficeFunction", back_populates="translations")


class OfficeEducation(Base):
    """One line of the director's education history.

    Ordered by ``display_order``, which the dashboard sets highest-degree-first
    (PhD → Bachelor). Years are language-neutral free text; ``end_year`` is left
    empty while a degree is still in progress.
    """

    __tablename__ = "office_educations"

    id = Column(Integer, primary_key=True, index=True)
    office_id = Column(Integer, ForeignKey("offices.id", ondelete="CASCADE"), nullable=False)
    start_year = Column(String(20))
    end_year = Column(String(20))
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    office = relationship("Office", back_populates="educations")
    translations = relationship(
        "OfficeEducationTr",
        back_populates="education",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class OfficeEducationTr(Base):
    __tablename__ = "office_education_tr"
    __table_args__ = (
        UniqueConstraint("education_id", "lang_code", name="uq_office_education_tr_edu_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    education_id = Column(
        Integer, ForeignKey("office_educations.id", ondelete="CASCADE"), nullable=False
    )
    lang_code = Column(String(10), nullable=False)

    # "Doctor of Philosophy in Computer Science" and the awarding institution.
    degree = Column(String(500))
    university = Column(String(500))

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    education = relationship("OfficeEducation", back_populates="translations")


class OfficeStaff(Base):
    """One staff member of the office."""

    __tablename__ = "office_staff"

    id = Column(Integer, primary_key=True, index=True)
    office_id = Column(Integer, ForeignKey("offices.id", ondelete="CASCADE"), nullable=False)
    phone = Column(String(100))
    phone_code = Column(String(50))
    email = Column(String(255))
    image_url = Column(String(2048))
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    office = relationship("Office", back_populates="staff")
    translations = relationship(
        "OfficeStaffTr",
        back_populates="staff",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class OfficeStaffTr(Base):
    __tablename__ = "office_staff_tr"
    __table_args__ = (
        UniqueConstraint("staff_id", "lang_code", name="uq_office_staff_tr_staff_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("office_staff.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(10), nullable=False)

    name = Column(String(255))
    surname = Column(String(255))
    # The person's duty / role in the office.
    duty = Column(String(500))

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    staff = relationship("OfficeStaff", back_populates="translations")
