import os
import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional

def load_csv(file_path: str) -> Optional[pd.DataFrame]:
    """Carga datos desde un archivo CSV hacia un DataFrame de pandas."""
    try:
        df = pd.read_csv(file_path)
        print(f"[Tool: load_csv] Loaded {len(df)} rows from '{file_path}'.")
        return df
    except Exception as e:
        print(f"[Tool: load_csv] Error loading '{file_path}': {e}")
        return None

def group_by_and_aggregate(
    df: pd.DataFrame, group_by_col: str, agg_col: str, agg_func: str = "sum"
) -> Optional[pd.DataFrame]:
    """Agrupa el DataFrame y aplica una función de agregación ('sum', 'mean', 'count')."""
    if df is None:
        print("[Tool: group_by_and_aggregate] Error: input DataFrame is None.")
        return None
    if group_by_col not in df.columns or agg_col not in df.columns:
        print(f"[Tool: group_by_and_aggregate] Error: Columns '{group_by_col}' or '{agg_col}' not found.")
        return None
    func = {"sum": "sum", "mean": "mean", "count": "count"}.get(agg_func, "sum")
    result = df.groupby(group_by_col)[agg_col].agg(func).reset_index()
    print(f"[Tool: group_by_and_aggregate] Aggregated '{agg_col}' by '{group_by_col}' using '{func}'.")
    return result

def plot_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str, output_path: str) -> bool:
    """Genera y guarda un gráfico de barras a partir del DataFrame estructurado."""
    if df is None or x_col not in df.columns or y_col not in df.columns:
        print("[Tool: plot_bar_chart] Error: invalid DataFrame or column names.")
        return False
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(df[x_col].astype(str), df[y_col], color="#2b5c8f")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(title)
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"[Tool: plot_bar_chart] Chart saved to '{output_path}'.")
    return True