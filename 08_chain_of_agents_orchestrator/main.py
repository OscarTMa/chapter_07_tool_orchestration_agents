from dotenv import load_dotenv
from orchestrator import ChainOfAgentsOrchestrator

load_dotenv()

if __name__ == "__main__":
    orchestrator = ChainOfAgentsOrchestrator()
    target_company = "ApexCloud Systems"
    report = orchestrator.run_market_intelligence(target_company)
    print("\n================ FINAL SYNTHESIS & ARBITRATION REPORT ================")
    print(report)