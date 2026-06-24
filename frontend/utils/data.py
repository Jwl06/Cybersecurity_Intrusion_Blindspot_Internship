"""Dashboard metrics and chart data."""

import pandas as pd

MODEL_METRICS = {
    "accuracy": 0.9665,
    "precision": 0.58,
    "recall": 0.60,
    "f1_score": 0.59,
}

FEATURE_IMPORTANCE = pd.DataFrame(
    {
        "feature": [
            "src_port",
            "dst_port",
            "protocol",
            "bytes_sent",
            "bytes_received",
            "user_agent",
            "is_internal_traffic",
        ],
        "importance": [
            0.152565,
            0.233119,
            0.072330,
            0.147910,
            0.077048,
            0.266626,
            0.050402,
        ],
    }
).sort_values("importance", ascending=True)

CONFUSION_MATRIX = pd.DataFrame(
    [[1885, 35], [32, 48]],
    index=["Actual Normal", "Actual Attack"],
    columns=["Pred Normal", "Pred Attack"],
)

DATASET_STATS = {
    "total_flows": 10_000,
    "normal_flows": 9_600,
    "attack_flows": 400,
    "features": 7,
}
