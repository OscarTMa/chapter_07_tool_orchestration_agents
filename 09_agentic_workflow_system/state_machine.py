from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

class ClaimState(str, Enum):
    INTAKE = "INTAKE"
    VALIDATING = "VALIDATING"
    ASSESSING_RISK = "ASSESSING_RISK"
    PENDING_HUMAN_REVIEW = "PENDING_HUMAN_REVIEW"
    PROCESSING_PAYOUT = "PROCESSING_PAYOUT"
    CLOSED_APPROVED = "CLOSED_APPROVED"
    CLOSED_REJECTED = "CLOSED_REJECTED"

class ClaimRecord(BaseModel):
    claim_id: str
    policy_id: str
    claim_type: str
    amount: float
    policy_active: bool = True
    fraud_flag: bool = False
    confidence_score: float = 0.0
    risk_level: str = "unknown"
    state: ClaimState = ClaimState.INTAKE
    human_decision: Optional[str] = None
    audit_notes: list[str] = Field(default_factory=list)

    def log(self, note: str):
        self.audit_notes.append(f"[{self.state.value}] {note}")