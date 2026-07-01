import uuid
import enum
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Text, DateTime, Enum, JSON, Uuid
from backend.db.database import Base

class ClaimStatus(str, enum.Enum):
    """The lifecycle stages of a fact-check request."""
    pending = "pending"
    processing = "processing"
    verified = "verified"
    debunked = "debunked"
    inconclusive = "inconclusive"

class Claim(Base):
    """SQLAlchemy model for the 'claims' table in PostgreSQL."""
    __tablename__ = "claims"

    # Unique identifier automatically generated on creation
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # The actual statement the user wants verified
    claim_text = Column(String, nullable=False, index=True)
    
    # The current state of the evaluation
    status = Column(Enum(ClaimStatus), default=ClaimStatus.pending, nullable=False)
    
    # The AI's confidence score (0.0 to 1.0)
    confidence = Column(Float, nullable=True)
    
    # The LangChain-generated reasoning
    justification = Column(Text, nullable=True)
    
    # A list of retrieved URLs or document references
    sources = Column(JSON, default=list)
    
    # Timezone-aware timestamp for historical tracking
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
