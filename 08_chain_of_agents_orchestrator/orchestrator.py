import os
from google import genai
from typing import Dict, Any
from memory import MultiAgentMemory
from specialists import news_specialist_agent, financial_specialist_agent, sentiment_specialist_agent

class ChainOfAgentsOrchestrator:
    def __init__(self):
        self.memory = MultiAgentMemory()
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def run_market_intelligence(self, company_name: str) -> str:
        print(f"[Orchestrator] Dispatching tasks for target: {company_name}")
        
        # 1. Delegación a especialistas concurrentes/secuenciales
        news_out = news_specialist_agent(company_name)
        fin_out = financial_specialist_agent(company_name)
        sent_out = sentiment_specialist_agent(company_name)

        # 2. Persistencia en memoria
        self.memory.log_episode("NewsAgent", news_out["data"])
        self.memory.log_episode("FinancialAgent", fin_out["data"])
        self.memory.log_episode("SentimentAgent", sent_out["data"])

        # 3. Detección matemática de divergencias / conflictos
        fin_data = fin_out["data"]
        sent_data = sent_out["data"]
        
        stock_change_norm = fin_data["stock_change_pct"] / 10.0  # Normalizado a escala [-1, 1]
        sentiment_norm = sent_data["sentiment_score"]
        conflict_score = abs(sentiment_norm - stock_change_norm)

        print(f"[Orchestrator] Conflict Score Detected: {conflict_score:.2f}")

        # 4. Arbitraje asistido por LLM (Reasoning Core)
        context = f"""
Market Intelligence Snapshot for {company_name}:
- News Highlights: {news_out['data']['headlines']}
- Financials: P/E Ratio={fin_data['pe_ratio']}, Rev Growth={fin_data['revenue_growth']*100}%, Daily Move={fin_data['stock_change_pct']}%
- Sentiment: Score={sent_data['sentiment_score']} ({sent_data['label']})
- Conflict Index: {conflict_score:.2f} (Divergence between market action and sentiment)
"""
        prompt = f"""
You are the Lead Arbiter Agent. Synthesize the findings from the specialist agents into an executive briefing.
Reconcile any conflicting signals (e.g., strong public sentiment vs negative short-term price movement).

Context:
{context}
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text