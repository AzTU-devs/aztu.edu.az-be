from app.core.database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey


class MenuSocialLink(Base):
    __tablename__ = "menu_social_links"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False)
    url = Column(Text, nullable=False)
    context = Column(String(20), nullable=False)  # 'footer', 'quick', 'both'
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class MenuContact(Base):
    __tablename__ = "menu_contacts"

    id = Column(Integer, primary_key=True, index=True)
    context = Column(String(20), nullable=False)  # 'footer', 'quick'
    email = Column(String(200), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class MenuContactPhone(Base):
    __tablename__ = "menu_contact_phones"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("menu_contacts.id", ondelete="CASCADE"), nullable=False)
    phone = Column(String(50), nullable=False)
    display_order = Column(Integer, nullable=False)


class MenuContactAddress(Base):
    __tablename__ = "menu_contact_addresses"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("menu_contacts.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(5), nullable=False)
    address = Column(Text, nullable=False)
