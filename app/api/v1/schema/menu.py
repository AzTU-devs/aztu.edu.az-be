from typing import Optional
from pydantic import BaseModel


class TranslationInput(BaseModel):
    az: str
    en: str


class OptionalTranslationInput(BaseModel):
    az: Optional[str] = None
    en: Optional[str] = None


# ── Header Section ────────────────────────────────────────────

class CreateHeaderSection(BaseModel):
    section_key: str
    image_url: str
    display_order: int
    label: TranslationInput
    base_path: TranslationInput


class UpdateHeaderSection(BaseModel):
    image_url: Optional[str] = None
    display_order: Optional[int] = None
    label: Optional[OptionalTranslationInput] = None
    base_path: Optional[OptionalTranslationInput] = None


# ── Header Item ───────────────────────────────────────────────

class CreateHeaderItem(BaseModel):
    section_id: int
    slug: Optional[str] = None
    display_order: int
    title: TranslationInput


class UpdateHeaderItem(BaseModel):
    slug: Optional[str] = None
    display_order: Optional[int] = None
    title: Optional[OptionalTranslationInput] = None


# ── Header Sub-Item ───────────────────────────────────────────

class CreateHeaderSubItem(BaseModel):
    item_id: int
    slug: str
    display_order: int
    title: TranslationInput


class UpdateHeaderSubItem(BaseModel):
    slug: Optional[str] = None
    display_order: Optional[int] = None
    title: Optional[OptionalTranslationInput] = None


# ── Footer Column ─────────────────────────────────────────────

class CreateFooterColumn(BaseModel):
    display_order: int
    title: TranslationInput


class UpdateFooterColumn(BaseModel):
    display_order: Optional[int] = None
    title: Optional[OptionalTranslationInput] = None


# ── Footer Link ───────────────────────────────────────────────

class CreateFooterLink(BaseModel):
    column_id: int
    url: str
    display_order: int
    label: TranslationInput


class UpdateFooterLink(BaseModel):
    url: Optional[str] = None
    display_order: Optional[int] = None
    label: Optional[OptionalTranslationInput] = None


# ── Footer Partner Logo ───────────────────────────────────────

class CreatePartnerLogo(BaseModel):
    label: str
    image_url: str
    url: str
    display_order: int


class UpdatePartnerLogo(BaseModel):
    label: Optional[str] = None
    image_url: Optional[str] = None
    url: Optional[str] = None
    display_order: Optional[int] = None


# ── Footer Quick Icon ─────────────────────────────────────────

class CreateQuickIcon(BaseModel):
    icon: str
    url: str
    display_order: int
    label: TranslationInput


class UpdateQuickIcon(BaseModel):
    icon: Optional[str] = None
    url: Optional[str] = None
    display_order: Optional[int] = None
    label: Optional[OptionalTranslationInput] = None


# ── Social Link ───────────────────────────────────────────────

class CreateSocialLink(BaseModel):
    platform: str
    url: str
    context: str  # 'footer' | 'quick' | 'both'
    display_order: int


class UpdateSocialLink(BaseModel):
    platform: Optional[str] = None
    url: Optional[str] = None
    context: Optional[str] = None
    display_order: Optional[int] = None


# ── Contact ───────────────────────────────────────────────────

class CreateContact(BaseModel):
    context: str  # 'footer' | 'quick'
    email: str
    phones: list[str]
    address: Optional[TranslationInput] = None  # footer only


class UpdateContact(BaseModel):
    email: Optional[str] = None
    phones: Optional[list[str]] = None
    address: Optional[OptionalTranslationInput] = None


# ── Quick Left Item ───────────────────────────────────────────

class CreateQuickLeftItem(BaseModel):
    url: str
    display_order: int
    label: TranslationInput


class UpdateQuickLeftItem(BaseModel):
    url: Optional[str] = None
    display_order: Optional[int] = None
    label: Optional[OptionalTranslationInput] = None


# ── Quick Section ─────────────────────────────────────────────

class CreateQuickSection(BaseModel):
    section_key: str
    display_order: int
    title: TranslationInput


class UpdateQuickSection(BaseModel):
    display_order: Optional[int] = None
    title: Optional[OptionalTranslationInput] = None


# ── Quick Section Item ────────────────────────────────────────

class CreateQuickSectionItem(BaseModel):
    section_id: int
    url: str
    display_order: int
    label: TranslationInput


class UpdateQuickSectionItem(BaseModel):
    url: Optional[str] = None
    display_order: Optional[int] = None
    label: Optional[OptionalTranslationInput] = None
