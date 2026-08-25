import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
import tools

class ToolCallSpec(BaseModel):
    tool_name: Literal["load_csv", "group_by_and_aggregate", "plot_bar_chart"]
    parameters: dict = Field(default_factory=dict)

class ToolExecutionPlan(BaseModel):
    intent_analysis: str = Field(description="Desglose del objetivo del usuario")
    steps: List[ToolCallSpec] = Field(description="Secuencia ordenada de herramientas a ejecutar")

class ToolUsingAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self.tool_registry = {
            "load_csv": tools.load_csv,
            "group_by_and_aggregate": tools.group_by_and_aggregate,
            "plot_bar_chart": tools.plot_bar_chart
        }

    def think_and_plan(self, user_query: str, file_path: str, output_path: str) -> ToolExecutionPlan:
        """Etapa THINK y PLAN: Genera un plan estructurado validado con Pydantic."""
        prompt = f"""
Analyze the user request and generate an execution plan using only the available tools:
Available tools:
- load_csv(file_path: str)
- group_by_and_aggregate(df: pd.DataFrame, group_by_col: str, agg_col: str, agg_func: str)
- plot_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str, output_path: str)

Query: '{user_query}'
Source File: '{file_path}'
Target Output Image: '{output_path}'
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ToolExecutionPlan,
                temperature=0.0
            )
        )
        return ToolExecutionPlan.model_validate_json(response.text)

    def act(self, plan: ToolExecutionPlan) -> bool:
        """Etapa ACT: Motor de ejecución con propagación de estado."""
        data_state = None
        print(f"\n[Agent: Think] {plan.intent_analysis}")
        print(f"[Agent: Plan] Total steps: {len(plan.steps)}")

        for idx, step in enumerate(plan.steps):
            print(f" -> Executing Step {idx + 1}: {step.tool_name}")
            tool_fn = self.tool_registry.get(step.tool_name)
            if not tool_fn:
                print(f"[Execution Engine] Tool '{step.tool_name}' not found in registry. Aborting.")
                return False

            kwargs = step.parameters.copy()
            if step.tool_name in ["group_by_and_aggregate", "plot_bar_chart"]:
                kwargs["df"] = data_state

            result = tool_fn(**kwargs)
            if step.tool_name in ["load_csv", "group_by_and_aggregate"]:
                if result is None:
                    print("[Execution Engine] Step failed. Halting workflow.")
                    return False
                data_state = result
            elif step.tool_name == "plot_bar_chart" and not result:
                return False

        return True