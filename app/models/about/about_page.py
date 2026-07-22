"""About-section pages — a block CMS behind the header's "Haqqımızda" dropdown.

Every page under /about used to live as hand-typed copy in the website's locale
files. Rather than mint a bespoke table per page (there are two dozen, each with
its own shape), a page is stored as an ordered list of typed *sections*, and each
section owns ordered *items* — or, for the leadership pages, *people*.

The section's ``section_type`` is what the admin form and the website renderer
both switch on. The union of columns below is deliberately wide: it is the union
of every field the static pages carried, so nothing has to be squeezed into a
generic blob. ``extra`` (JSONB) exists only for genuinely repeating sub-lists —
a KPI card's target chips, a table row's cells — which have no fixed arity.

Language-neutral facts (an image, a URL, a year) live on the row; anything a
translator would touch lives on the ``*_tr`` sibling, keyed by ``lang_code``.
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


class AboutPage(Base):
    """One screen in the About dropdown. ``page_key`` is the stable admin/API id."""

    __tablename__ = "about_pages"

    id = Column(Integer, primary_key=True, index=True)
    page_key = Column(String(100), unique=True, nullable=False)
    # Which dropdown column the page hangs under: vision_mission, leadership,
    # affiliated, policies, other. Drives the sidebar grouping in the dashboard.
    group_key = Column(String(50), nullable=False, default="other")
    # The page's layout family. The website picks a renderer from this; the admin
    # picks nothing from it — the section list alone drives the form.
    template = Column(String(50), nullable=False, default="generic")
    slug_az = Column(String(255))
    slug_en = Column(String(255))
    display_order = Column(Integer, nullable=False, default=0)
    # False keeps a page out of the public API while it is being filled in, which
    # is the whole point of building this before the website switches over.
    is_active = Column(Boolean, nullable=False, default=False)

    hero_image = Column(String(1024))
    hero_video_url = Column(String(2048))
    cover_image = Column(String(1024))
    pdf_url = Column(String(2048))
    pdf_filename = Column(String(255))
    website_url = Column(String(2048))
    video_url = Column(String(2048))

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    translations = relationship(
        "AboutPageTr",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    sections = relationship(
        "AboutSection",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AboutSection.display_order",
    )


class AboutPageTr(Base):
    __tablename__ = "about_page_tr"
    __table_args__ = (
        UniqueConstraint("page_id", "lang_code", name="uq_about_page_tr_page_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("about_pages.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(10), nullable=False)

    eyebrow = Column(String(255))
    title = Column(String(500))
    subtitle = Column(Text)
    breadcrumb = Column(String(255))
    intro = Column(Text)
    meta_title = Column(String(500))
    meta_description = Column(Text)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("AboutPage", back_populates="translations")


class AboutSection(Base):
    """An ordered block on a page. ``section_key`` is stable; the copy is not."""

    __tablename__ = "about_sections"
    __table_args__ = (
        UniqueConstraint("page_id", "section_key", name="uq_about_sections_page_key"),
    )

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("about_pages.id", ondelete="CASCADE"), nullable=False)
    section_key = Column(String(100), nullable=False)
    # paragraphs | list | stats | timeline | pillars | people | table |
    # documents | links | facts | contact | video | quote | gallery |
    # ranking_systems | ranking_positions | group_list | cards
    section_type = Column(String(50), nullable=False, default="paragraphs")
    display_order = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)

    image_url = Column(String(1024))
    link_url = Column(String(2048))
    pdf_url = Column(String(2048))
    video_url = Column(String(2048))
    icon = Column(String(100))
    extra = Column(JSONB)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("AboutPage", back_populates="sections")
    translations = relationship(
        "AboutSectionTr",
        back_populates="section",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    items = relationship(
        "AboutItem",
        back_populates="section",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AboutItem.display_order",
    )
    people = relationship(
        "AboutPerson",
        back_populates="section",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AboutPerson.display_order",
    )


class AboutSectionTr(Base):
    __tablename__ = "about_section_tr"
    __table_args__ = (
        UniqueConstraint("section_id", "lang_code", name="uq_about_section_tr_section_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("about_sections.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(10), nullable=False)

    title = Column(String(500))
    subtitle = Column(Text)
    description = Column(Text)
    # Rich text. Paragraph arrays on the static pages collapse into one HTML body
    # here, so the editor is a normal Tiptap field rather than a list of strings.
    body_html = Column(Text)
    footer = Column(Text)
    note = Column(Text)
    cta_label = Column(String(255))
    pdf_url = Column(String(2048))
    # The anniversary film is a different YouTube cut per language, so the URL
    # belongs to the translation rather than the block.
    video_url = Column(String(2048))
    # A block can carry a heading, a rich-text lead AND a list (e.g. the units
    # reporting to the Rector); `description` is already the plain lead.
    list_intro = Column(Text)
    # Table column headers, per language: ["№", "S.A.A.", "Vəzifəsi"].
    headers = Column(JSONB)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    section = relationship("AboutSection", back_populates="translations")


class AboutItem(Base):
    """One row inside a section — a stat, a milestone, a document, a link."""

    __tablename__ = "about_items"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("about_sections.id", ondelete="CASCADE"), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)
    # Free-form grouping tag — a policy document's category, a duration block's
    # "phd"/"ds". Never shown; only ever matched on.
    item_key = Column(String(100))
    is_active = Column(Boolean, nullable=False, default=True)

    image_url = Column(String(1024))
    link_url = Column(String(2048))
    pdf_url = Column(String(2048))
    email = Column(String(255))
    phone = Column(String(100))
    icon = Column(String(100))
    slug = Column(String(255))
    year = Column(String(50))
    num = Column(String(50))
    # Kept as text on purpose: "476", "851-900", "25,000+", "3 247".
    value = Column(String(255))
    extra = Column(JSONB)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    section = relationship("AboutSection", back_populates="items")
    translations = relationship(
        "AboutItemTr",
        back_populates="item",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class AboutItemTr(Base):
    __tablename__ = "about_item_tr"
    __table_args__ = (
        UniqueConstraint("item_id", "lang_code", name="uq_about_item_tr_item_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("about_items.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(10), nullable=False)

    title = Column(Text)
    subtitle = Column(Text)
    description = Column(Text)
    label = Column(String(500))
    value_text = Column(String(500))
    caption = Column(Text)
    link_label = Column(String(500))
    # Per-language file: the policy library ships a separate AZ and EN PDF.
    file_url = Column(String(2048))
    # Repeating sub-lists with no fixed arity — a KPI card's target chips, a
    # table row's cells, a duration block's lines.
    extra = Column(JSONB)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    item = relationship("AboutItem", back_populates="translations")


class AboutPerson(Base):
    """A named individual on a leadership page — rector, vice-rector, staff."""

    __tablename__ = "about_people"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("about_sections.id", ondelete="CASCADE"), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)

    # Detail-page slug (/about/vice-rector/subhan-namazov). Null for staff rows
    # that are only ever rendered inside a card list.
    slug = Column(String(255))
    image_url = Column(String(1024))
    email = Column(String(255))
    phone = Column(String(100))
    phone_internal = Column(String(50))
    room_number = Column(String(100))

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    section = relationship("AboutSection", back_populates="people")
    translations = relationship(
        "AboutPersonTr",
        back_populates="person",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    educations = relationship(
        "AboutPersonEducation",
        back_populates="person",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AboutPersonEducation.display_order",
    )


class AboutPersonTr(Base):
    __tablename__ = "about_person_tr"
    __table_args__ = (
        UniqueConstraint("person_id", "lang_code", name="uq_about_person_tr_person_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("about_people.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(10), nullable=False)

    full_name = Column(String(500))
    degree = Column(String(500))
    position = Column(String(500))
    office = Column(String(500))
    hours = Column(String(255))
    bio_html = Column(Text)
    achievements = Column(Text)
    # One interest per line. A plain list of strings with no other attributes,
    # so a child table would buy nothing an editor can feel.
    research_interests = Column(Text)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    person = relationship("AboutPerson", back_populates="translations")


class AboutPersonEducation(Base):
    __tablename__ = "about_person_education"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("about_people.id", ondelete="CASCADE"), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)
    # "2012-2016" verbatim — the static pages never split it, and some rows are
    # open-ended ("2021–").
    period = Column(String(100))

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    person = relationship("AboutPerson", back_populates="educations")
    translations = relationship(
        "AboutPersonEducationTr",
        back_populates="education",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class AboutPersonEducationTr(Base):
    __tablename__ = "about_person_education_tr"
    __table_args__ = (
        UniqueConstraint("education_id", "lang_code", name="uq_about_person_edu_tr_edu_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    education_id = Column(
        Integer, ForeignKey("about_person_education.id", ondelete="CASCADE"), nullable=False
    )
    lang_code = Column(String(10), nullable=False)

    degree = Column(String(500))
    institution = Column(String(1000))

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    education = relationship("AboutPersonEducation", back_populates="translations")
