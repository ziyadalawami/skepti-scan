from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from backend.db.database import get_db
from backend.api.schemas import ClaimCreate, ClaimResponse
from backend.services import claim_service

# Group all these endpoints under the /api/v1 prefix
router = APIRouter(prefix="/api/v1", tags=["Verification"])

@router.post("/verify", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
def verify_claim(claim_in: ClaimCreate, db: Session = Depends(get_db)):
    """Submit a new claim for fact-checking."""
    return claim_service.create_and_process_claim(db=db, claim_text=claim_in.claim_text)

@router.get("/claims", response_model=List[ClaimResponse])
def list_claims(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Retrieve a list of historical fact-checks."""
    return claim_service.get_all_claims(db=db, skip=skip, limit=limit)

@router.get("/claims/{claim_id}", response_model=ClaimResponse)
def get_claim(claim_id: UUID, db: Session = Depends(get_db)):
    """Fetch a specific fact-check by its ID."""
    claim = claim_service.get_claim_by_id(db=db, claim_id=claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim
