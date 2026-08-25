import os
import sys
from pathlib import Path
import pandas as pd
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Literal, Optional

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

import tools

class LoadCsvParams(BaseModel):
    file_path: str = Field(description="Path to the CSV file")

class AggregateParams(BaseModel):
    group_by_col: str = Field(description="Exact column name to group by")
    agg_col: str = Field(description="Exact numerical column name to aggregate")
    agg_func: Literal["sum", "mean", "count"] = Field(default="sum", description="Aggregation function")

class PlotParams(BaseModel):
    x_col: str = Field(description="Exact column name for X axis from the aggregated data")
    y_col: str = Field(description="Exact column name for Y axis from the aggregated data")
    title: str = Field(description="Chart title")
    output_path: str = Field(description="Path to save the generated PNG chart")

class ToolCallSpec(BaseModel):
    tool_name: Literal["load_csv", "group_by_and_aggregate", "plot_bar_chart"] = Field(
        description="Tool name to execute"
    )
    load_csv_args: Optional[LoadCsvParams] = None
    aggregate_args: Optional[AggregateParams] = None
    plot_args: Optional[PlotParams] = None

class ToolExecutionPlan(BaseModel):
    intent_analysis: str = Field(description="Analysis of user request")
    steps: List[ToolCallSpec] = Field(description="Ordered sequence of tool executions")

class ToolUsingAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self.tool_registry = {
            "load_csv": tools.load_csv,
            "group_by_and_aggregate": tools.group_by_and_aggregate,
            "plot_bar_chart": tools.plot_bar_chart
        }

    def think_and_plan(self, user_query: str, file_path: str, output_path: str) -> ToolExecutionPlan:
        columns = []
        if os.path.exists(file_path):
            sample_df = pd.read_csv(file_path, nrows=1)
            columns = sample_df.columns.tolist()

        prompt = f"""
You are a data analytics orchestrator. Create a strict 3-step execution plan using ONLY these tools:

1. load_csv: file_path="{file_path}"
2. group_by_and_aggregate: group_by_col, agg_col, agg_func="sum"
3. plot_bar_chart: x_col, y_col, title, output_path="{output_path}"

Rules:
- Available original columns: {columns}
- In step 2 (group_by_and_aggregate), set group_by_col to the categorical column and agg_col to the metric column.
- In step 3 (plot_bar_chart), the output columns from step 2 will retain the EXACT SAME column names: x_col must match group_by_col, and y_col must match agg_col. Do NOT invent names like 'total_spend'.

User Request: '{user_query}'
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
        data_state = None
        print(f"\n[Agent: Think] {plan.intent_analysis}")
        print(f"[Agent: Plan] Total steps: {len(plan.steps)}")

        for idx, step in enumerate(plan.steps):
            print(f" -> Executing Step {idx + 1}: {step.tool_name}")
            tool_fn = self.tool_registry.get(step.tool_name)
            if not tool_fn:
                print(f"[Execution Engine] Tool '{step.tool_name}' not found. Aborting.")
                return False

            if step.tool_name == "load_csv":
                args = step.load_csv_args.model_dump()
                data_state = tool_fn(**args)
                if data_state is None:
                    return False

            elif step.tool_name == "group_by_and_aggregate":
                args = step.aggregate_args.model_dump()
                data_state = tool_fn(df=data_state, **args)
                if data_state is None:
                    return False

            elif step.tool_name == "plot_bar_chart":
                args = step.plot_args.model_dump()
                success = tool_fn(df=data_state, **args)
                if not success:
                    return False

        return True