import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from agent import ToolUsingAgent

# Carga automática del .env desde la raíz del proyecto
load_dotenv(find_dotenv())

if __name__ == "__main__":
    csv_file = "campaign_data.csv"
    chart_output = "campaign_spend_summary.png"

    # Generar dataset de prueba sintético
    df_mock = pd.DataFrame({
        "campaign_name": ["Alpha", "Beta", "Alpha", "Gamma", "Beta", "Gamma"],
        "spend": [1200.50, 850.00, 450.00, 2100.00, 950.00, 300.00],
        "conversions": [45, 30, 18, 90, 40, 12]
    })
    df_mock.to_csv(csv_file, index=False)

    agent = ToolUsingAgent()
    query = "Create a bar chart showing the total spend grouped by campaign name."
    
    plan = agent.think_and_plan(query, file_path=csv_file, output_path=chart_output)
    success = agent.act(plan)
    print(f"\nWorkflow Status: {'SUCCESS' if success else 'FAILED'}")