from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class ChatbotKnowledge(Base):
    __tablename__ = "chatbot_knowledge"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("chatbot_knowledge_sources.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    scraped_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, nullable=False, default=True)

    source = relationship("ChatbotKnowledgeSource", back_populates="knowledge")
