import os
import json
from typing import Optional
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from state_machine import ClaimRecord, ClaimState

class RiskAssessmentSchema(BaseModel):
    risk_level: str = Field(description="Evaluación del nivel de riesgo: 'low', 'medium' o 'high'")
    confidence_score: float = Field(description="Puntuación de confianza entre 0.0 y 1.0")
    justification: str = Field(description="Explicación detallada de la evaluación")

class InsuranceClaimWorkflowEngine:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def run_intake(self, claim: ClaimRecord):
        claim.log("Extracting document data and initial validation.")
        if claim.claim_id and claim.policy_id and claim.amount > 0:
            claim.state = ClaimState.VALIDATING
        else:
            claim.state = ClaimState.CLOSED_REJECTED

    def run_validation(self, claim: ClaimRecord):
        claim.log(f"Validating policy active={claim.policy_active}, fraud_flag={claim.fraud_flag}")
        if claim.policy_active and not claim.fraud_flag:
            claim.state = ClaimState.ASSESSING_RISK
        else:
            claim.state = ClaimState.CLOSED_REJECTED

    def run_risk_assessment(self, claim: ClaimRecord):
        claim.log("Executing LLM Agent risk assessment.")
        prompt = f"""
Evaluate the insurance claim risk and return the assessment:
Claim ID: {claim.claim_id}
Type: {claim.claim_type}
Amount: ${claim.amount:.2f}
Policy: {claim.policy_id}
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RiskAssessmentSchema,
                temperature=0.0
            )
        )
        assessment = RiskAssessmentSchema.model_validate_json(response.text)
        claim.risk_level = assessment.risk_level.lower()
        claim.confidence_score = assessment.confidence_score
        claim.log(f"Risk: {claim.risk_level}, Confidence: {claim.confidence_score:.2f}. Reason: {assessment.justification}")

        # Guard Conditions (Reglas de transición del estado)
        if claim.confidence_score >= 0.85 and claim.risk_level == "low":
            claim.state = ClaimState.PROCESSING_PAYOUT
        else:
            claim.state = ClaimState.PENDING_HUMAN_REVIEW

    def run_human_checkpoint(self, claim: ClaimRecord, auto_decision: Optional[str] = None):
        claim.log("Triggered HITL Checkpoint. Awaiting human judgment.")
        decision = auto_decision
        if not decision:
            print(f"\n[!] HITL ESCALATION: Claim {claim.claim_id} requires human approval.")
            print(f"Amount: ${claim.amount:.2f} | Risk Level: {claim.risk_level} | Conf: {claim.confidence_score:.2f}")
            while decision not in ["approve", "reject"]:
                decision = input("Enter decision ('approve' / 'reject'): ").strip().lower()

        claim.human_decision = decision
        if decision == "approve":
            claim.log("Human reviewer APPROVED claim.")
            claim.state = ClaimState.PROCESSING_PAYOUT
        else:
            claim.log("Human reviewer REJECTED claim.")
            claim.state = ClaimState.CLOSED_REJECTED

    def run_payout(self, claim: ClaimRecord):
        claim.log(f"Processing electronic funds transfer of ${claim.amount:.2f}")
        claim.state = ClaimState.CLOSED_APPROVED

    def execute(self, claim: ClaimRecord, auto_hitl_decision: Optional[str] = None) -> ClaimRecord:
        """Motor de transición de estados finitos."""
        while claim.state not in [ClaimState.CLOSED_APPROVED, ClaimState.CLOSED_REJECTED]:
            if claim.state == ClaimState.INTAKE:
                self.run_intake(claim)
            elif claim.state == ClaimState.VALIDATING:
                self.run_validation(claim)
            elif claim.state == ClaimState.ASSESSING_RISK:
                self.run_risk_assessment(claim)
            elif claim.state == ClaimState.PENDING_HUMAN_REVIEW:
                self.run_human_checkpoint(claim, auto_decision=auto_hitl_decision)
            elif claim.state == ClaimState.PROCESSING_PAYOUT:
                self.run_payout(claim)
        return claim