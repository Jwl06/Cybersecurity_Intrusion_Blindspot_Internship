"""Model loading and inference helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

from backend.exceptions import UnknownCategoryError
from backend.schemas import TrafficPredictionRequest, TrafficPredictionResponse

FEATURE_COLUMNS: list[str] = [
  "src_port",
  "dst_port",
  "protocol",
  "bytes_sent",
  "bytes_received",
  "user_agent",
  "is_internal_traffic",
]

LABEL_MAP: dict[int, str] = {0: "Normal", 1: "Attack"}


@dataclass(slots=True)
class ModelArtifacts:
  """Container for loaded model assets."""

  model: XGBClassifier
  encoders: dict[str, LabelEncoder]
  feature_columns: list[str]


class ModelService:
  """Encapsulates artifact loading and prediction logic."""

  def __init__(self, models_dir: Path) -> None:
    self._models_dir = models_dir
    self._artifacts: ModelArtifacts | None = None

  @property
  def is_loaded(self) -> bool:
    """Return whether model artifacts are available in memory."""
    return self._artifacts is not None

  @property
  def artifacts(self) -> ModelArtifacts:
    """Return loaded artifacts or raise if startup loading failed."""
    if self._artifacts is None:
      raise RuntimeError("Model artifacts are not loaded.")
    return self._artifacts

  def load(self) -> None:
    """Load serialized model and encoders from disk."""
    model_path = self._models_dir / "xgboost_model.pkl"
    encoder_path = self._models_dir / "label_encoders.pkl"

    if not model_path.exists():
      raise FileNotFoundError(f"Model file not found: {model_path}")
    if not encoder_path.exists():
      raise FileNotFoundError(f"Encoder file not found: {encoder_path}")

    model = joblib.load(model_path)
    encoders = joblib.load(encoder_path)

    if not isinstance(model, XGBClassifier):
      raise TypeError("xgboost_model.pkl must contain an XGBClassifier instance.")
    if not isinstance(encoders, dict):
      raise TypeError("label_encoders.pkl must contain a dictionary of encoders.")

    for key in ("protocol", "user_agent"):
      if key not in encoders:
        raise KeyError(f"Missing '{key}' encoder in label_encoders.pkl.")

    self._artifacts = ModelArtifacts(
      model=model,
      encoders=encoders,
      feature_columns=FEATURE_COLUMNS,
    )

  def supported_protocols(self) -> list[str]:
    """Return protocol labels known to the training encoders."""
    encoder = self.artifacts.encoders["protocol"]
    return [str(value) for value in encoder.classes_]

  def model_metadata(self) -> dict[str, Any]:
    """Return descriptive metadata for the root endpoint."""
    artifacts = self.artifacts
    return {
      "model_loaded": True,
      "model_type": type(artifacts.model).__name__,
      "feature_columns": artifacts.feature_columns,
      "supported_protocols": self.supported_protocols(),
    }

  def _encode_category(self, field: str, value: str) -> int:
    """Encode a categorical feature using the persisted label encoder."""
    encoder = self.artifacts.encoders[field]
    classes = [str(item) for item in encoder.classes_]

    if field == "protocol":
      normalized = value.strip().upper()
      lookup = {item.upper(): item for item in classes}
      if normalized not in lookup:
        raise UnknownCategoryError(field, value, classes)
      canonical = lookup[normalized]
    else:
      if value not in classes:
        raise UnknownCategoryError(field, value, classes)
      canonical = value

    return int(encoder.transform([canonical])[0])

  def _build_feature_frame(self, payload: TrafficPredictionRequest) -> pd.DataFrame:
    """Transform API input into the training feature matrix."""
    encoded_protocol = self._encode_category("protocol", payload.protocol)
    encoded_user_agent = self._encode_category("user_agent", payload.user_agent)

    row = {
      "src_port": payload.src_port,
      "dst_port": payload.dst_port,
      "protocol": encoded_protocol,
      "bytes_sent": float(payload.bytes_sent),
      "bytes_received": float(payload.bytes_received),
      "user_agent": encoded_user_agent,
      "is_internal_traffic": int(payload.is_internal_traffic),
    }

    return pd.DataFrame([row], columns=self.artifacts.feature_columns)

  def predict(self, payload: TrafficPredictionRequest) -> TrafficPredictionResponse:
    """Run classification and return formatted probabilities."""
    features = self._build_feature_frame(payload)
    model = self.artifacts.model

    prediction_index = int(model.predict(features)[0])
    probabilities = model.predict_proba(features)[0]

    attack_probability = float(probabilities[1])
    confidence = float(max(probabilities))
    prediction_label = LABEL_MAP.get(prediction_index, "Unknown")

    return TrafficPredictionResponse(
      prediction=prediction_label,
      attack_probability=attack_probability,
      confidence=confidence,
    )
