import numpy as np
import pandas as pd


def percent_larger_than_zero(s: pd.Series) -> int:
    return 100 * (np.sum(s > 0) / len(s))


faces = pd.read_json("results/faces.jsonl", orient="records", lines=True)
faces = faces[faces["type"] == "success"]
faces["n_faces"] = faces["n_faces"].astype(int)

aggregated = faces.groupby(["journal", "decade"]).agg(
    total_faces=("n_faces", "sum"),
    percent_contains_face=("n_faces", percent_larger_than_zero),
)

aggregated
