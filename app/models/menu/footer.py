from app.core.database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey


class MenuFooterColumn(Base):
    __tablename__ = "menu_footer_columns"

    id = Column(Integer, primary_key=True, index=True)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class MenuFooterColumnTranslation(Base):
    __tablename__ = "menu_footer_column_translations"

    id = Column(Integer, primary_key=True, index=True)
    column_id = Column(Integer, ForeignKey("menu_footer_columns.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(5), nullable=False)
    title = Column(String(200), nullable=False)


class MenuFooterLink(Base):
    __tablename__ = "menu_footer_links"

    id = Column(Integer, primary_key=True, index=True)
    column_id = Column(Integer, ForeignKey("menu_footer_columns.id", ondelete="CASCADE"), nullable=False)
    url = Column(String(500), nullable=False)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class MenuFooterLinkTranslation(Base):
    __tablename__ = "menu_footer_link_translations"

    id = Column(Integer, primary_key=True, index=True)
    link_id = Column(Integer, ForeignKey("menu_footer_links.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(5), nullable=False)
    label = Column(String(200), nullable=False)


class MenuFooterPartnerLogo(Base):
    __tablename__ = "menu_footer_partner_logos"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(200), nullable=False)
    image_url = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class MenuFooterQuickIcon(Base):
    __tablename__ = "menu_footer_quick_icons"

    id = Column(Integer, primary_key=True, index=True)
    icon = Column(String(100), nullable=False)
    url = Column(Text, nullable=False)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class MenuFooterQuickIconTranslation(Base):
    __tablename__ = "menu_footer_quick_icon_translations"

    id = Column(Integer, primary_key=True, index=True)
    icon_id = Column(Integer, ForeignKey("menu_footer_quick_icons.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(5), nullable=False)
    label = Column(String(200), nullable=False)
