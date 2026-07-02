from sqlalchemy.orm import Session
from uuid import UUID
from backend.db.models import Claim
from backend.services.ai import evaluate_claim
from typing import List

def create_and_process_claim(db: Session, claim_text: str):
    """Saves a new claim, runs AI evaluation, and updates the database."""
    
    # 1. Create the initial database record
    # We set it to 'processing' while the AI thinks
    new_claim = Claim(claim_text=claim_text, status="processing")
    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)

    # 2. Trigger the LangChain pipeline
    print(f"Evaluating claim: '{claim_text}'...")
    ai_result = evaluate_claim(claim_text)
    print(f"AI Result: {ai_result}")

    # 3. Update the database record with the AI's JSON verdict
    new_claim.status = ai_result.get("status", "inconclusive")
    new_claim.confidence = ai_result.get("confidence", 0.0)
    new_claim.justification = ai_result.get("justification", "Evaluation failed.")
    
    # 4. Save the final results to PostgreSQL
    db.commit()
    db.refresh(new_claim)
    
    return new_claim

def create_and_process_batch(db: Session, claims: List[str]):
    """Iterates through a list of claims and processes them sequentially."""
    results = []
    for text in claims:
        # We simply reuse our robust single-claim logic!
        claim_result = create_and_process_claim(db=db, claim_text=text)
        results.append(claim_result)
    return results

def get_all_claims(db: Session, skip: int = 0, limit: int = 10):
    """Retrieves a paginated list of claims, newest first."""
    return db.query(Claim).order_by(Claim.created_at.desc()).offset(skip).limit(limit).all()

def get_claim_by_id(db: Session, claim_id: UUID):
    """Fetches a specific claim by its unique ID."""
    return db.query(Claim).filter(Claim.id == claim_id).first()
