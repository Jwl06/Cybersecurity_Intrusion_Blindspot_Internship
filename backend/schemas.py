"""Pydantic request and response models for the intrusion detection API."""

from pydantic import BaseModel, ConfigDict, Field


class TrafficPredictionRequest(BaseModel):
  """Network flow features submitted for intrusion classification."""

  model_config = ConfigDict(
    json_schema_extra={
      "example": {
        "protocol": "TCP",
        "src_port": 44322,
        "dst_port": 443,
        "bytes_sent": 1200.0,
        "bytes_received": 4500.0,
        "user_agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "is_internal_traffic": False,
      }
    }
  )

  protocol: str = Field(..., description="Transport protocol (e.g. TCP, UDP, ICMP).")
  src_port: int = Field(..., ge=0, le=65535, description="Source port number.")
  dst_port: int = Field(..., ge=0, le=65535, description="Destination port number.")
  bytes_sent: float = Field(..., ge=0, description="Outbound byte volume.")
  bytes_received: float = Field(..., ge=0, description="Inbound byte volume.")
  user_agent: str = Field(..., min_length=1, description="HTTP user-agent string.")
  is_internal_traffic: bool = Field(
    ..., description="Whether the flow stays inside the internal network."
  )


class TrafficPredictionResponse(BaseModel):
  """Classification result with calibrated probabilities."""

  prediction: str = Field(..., description="Human-readable class label.")
  attack_probability: float = Field(
    ..., ge=0.0, le=1.0, description="Probability that the session is an attack."
  )
  confidence: float = Field(
    ..., ge=0.0, le=1.0, description="Maximum class probability returned by the model."
  )


class HealthResponse(BaseModel):
  """Lightweight health probe response."""

  status: str


class RootResponse(BaseModel):
  """API metadata and model readiness information."""

  status: str
  service: str
  version: str
  model_loaded: bool
  model_type: str
  feature_columns: list[str]
  supported_protocols: list[str]
