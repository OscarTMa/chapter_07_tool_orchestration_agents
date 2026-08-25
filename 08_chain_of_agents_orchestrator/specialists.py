from typing import Dict, Any

def news_specialist_agent(company_name: str) -> Dict[str, Any]:
    """Especialista en recopilación y extracción de noticias."""
    return {
        "source": "NewsAgent",
        "status": "success",
        "data": {
            "headlines": [
                f"{company_name} secures major enterprise contract expansion",
                f"Regulatory review clears {company_name} of compliance concerns"
            ]
        }
    }

def financial_specialist_agent(company_name: str) -> Dict[str, Any]:
    """Especialista en telemetría de rendimiento bursátil y financiero."""
    return {
        "source": "FinancialAgent",
        "status": "success",
        "data": {
            "pe_ratio": 28.4,
            "revenue_growth": 0.18,
            "stock_change_pct": -4.2  # Señal bajista
        }
    }

def sentiment_specialist_agent(company_name: str) -> Dict[str, Any]:
    """Especialista en minería de sentimiento público y redes sociales."""
    return {
        "source": "SentimentAgent",
        "status": "success",
        "data": {
            "sentiment_score": 0.85,  # Señal altamente alcista (+1 a -1)
            "label": "very_positive",
            "evidence": "Broad investor optimism following infrastructure rollout."
        }
    }