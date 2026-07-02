from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from backend.db.models import ClaimStatus

# 1. What the user sends to the API
class ClaimCreate(BaseModel):
    claim_text: str

# 2. Schema for batch ingestion
class ClaimBatchCreate(BaseModel):
    claims: List[str]

# 3. What the API returns to the user
class ClaimResponse(BaseModel):
    id: UUID
    claim_text: str
    status: ClaimStatus
    confidence: Optional[float] = None
    justification: Optional[str] = None
    sources: List[str] = []
    created_at: datetime

    # This tells Pydantic it can read data directly from a SQLAlchemy database object
    model_config = ConfigDict(from_attributes=True)
