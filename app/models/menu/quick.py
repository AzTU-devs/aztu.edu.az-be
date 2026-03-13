from app.core.database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey


class MenuQuickLeftItem(Base):
    __tablename__ = "menu_quick_left_items"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, nullable=False)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class MenuQuickLeftItemTranslation(Base):
    __tablename__ = "menu_quick_left_item_translations"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("menu_quick_left_items.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(5), nullable=False)
    label = Column(String(200), nullable=False)


class MenuQuickSection(Base):
    __tablename__ = "menu_quick_sections"

    id = Column(Integer, primary_key=True, index=True)
    section_key = Column(String(50), unique=True, nullable=False)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class MenuQuickSectionTranslation(Base):
    __tablename__ = "menu_quick_section_translations"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("menu_quick_sections.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(5), nullable=False)
    title = Column(String(200), nullable=False)


class MenuQuickSectionItem(Base):
    __tablename__ = "menu_quick_section_items"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("menu_quick_sections.id", ondelete="CASCADE"), nullable=False)
    url = Column(Text, nullable=False)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class MenuQuickSectionItemTranslation(Base):
    __tablename__ = "menu_quick_section_item_translations"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("menu_quick_section_items.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(5), nullable=False)
    label = Column(String(200), nullable=False)
