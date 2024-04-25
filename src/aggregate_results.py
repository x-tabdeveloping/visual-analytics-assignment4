from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px


def percent_larger_than_zero(s: pd.Series) -> int:
    return 100 * (np.sum(s > 0) / len(s))


results_dir = Path("results")
figures_dir = Path("figures")
figures_dir.mkdir(exist_ok=True)

faces = pd.read_json(results_dir.joinpath("faces.jsonl"), orient="records", lines=True)
faces = faces[faces["type"] == "success"]
faces["n_faces"] = faces["n_faces"].astype(int)

aggregated = faces.groupby(["journal", "decade"]).agg(
    total_faces=("n_faces", "sum"),
    percent_contains_face=("n_faces", percent_larger_than_zero),
)
for journal, data in aggregated.groupby("journal"):
    fig = px.line(data.reset_index(), x="decade", y="percent_contains_face")
    fig.update_layout(width=800, height=800)
    fig.update_layout(xaxis_title="Decade")
    fig.update_layout(yaxis_title="% pages with faces")
    fig.write_image(figures_dir.joinpath(f"{journal}.png"), scale=2)
    data.to_csv(results_dir.joinpath(f"{journal}.csv"))
