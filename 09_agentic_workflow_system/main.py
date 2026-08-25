from dotenv import load_dotenv, find_dotenv
from state_machine import ClaimRecord
from workflow import InsuranceClaimWorkflowEngine

# Cargar automáticamente el .env de la raíz
load_dotenv(find_dotenv())

if __name__ == "__main__":
    engine = InsuranceClaimWorkflowEngine()

    # Caso de prueba: Reclamo CLM-4821
    claim = ClaimRecord(
        claim_id="CLM-4821",
        policy_id="POL-992317",
        claim_type="Water Damage - Commercial Property",
        amount=18400.00,
        policy_active=True,
        fraud_flag=False
    )

    print(f"Starting workflow for Claim #{claim.claim_id}...")
    final_record = engine.execute(claim, auto_hitl_decision="approve")

    print(f"\nFinal State: {final_record.state.value}")
    print("\n--- Complete Audit Trail ---")
    for log_entry in final_record.audit_notes:
        print(log_entry)