"""HTTP client for the intrusion detection inference API."""

from __future__ import annotations

import os
from typing import Any

import requests

DEFAULT_API_URL = os.getenv(
    "API_URL",
    "https://cyber-intrusion-api.onrender.com"
)


def predict_traffic(payload: dict[str, Any], api_url: str = DEFAULT_API_URL) -> dict[str, Any]:
    """Submit network flow features and return the classification response."""
    response = requests.post(
        f"{api_url.rstrip('/')}/predict",
        json=payload,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def api_available(api_url: str = DEFAULT_API_URL) -> bool:
    """Return whether the inference API is reachable."""
    try:
        response = requests.get(f"{api_url.rstrip('/')}/health", timeout=3)
        return response.status_code == 200
    except requests.RequestException:
        return False
