"""FastAPI application entry point for Cybersecurity Intrusion Blindspot."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from backend.exceptions import UnknownCategoryError
from backend.schemas import (
  HealthResponse,
  RootResponse,
  TrafficPredictionRequest,
  TrafficPredictionResponse,
)
from backend.services.model_service import ModelService

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

API_VERSION = "1.0.0"
SERVICE_NAME = "Cybersecurity Intrusion Blindspot API"
MODELS_DIR = Path(__file__).resolve().parent.parent / "models"

model_service = ModelService(models_dir=MODELS_DIR)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
  """Load ML artifacts once during application startup."""
  logger.info("Loading model artifacts from %s", MODELS_DIR)
  try:
    model_service.load()
    logger.info("Model artifacts loaded successfully.")
  except Exception:
    logger.exception("Failed to load model artifacts during startup.")
    raise
  yield
  logger.info("Shutting down %s", SERVICE_NAME)


app = FastAPI(
  title=SERVICE_NAME,
  description=(
    "Production inference API for network intrusion detection using a trained "
    "XGBoost classifier."
  ),
  version=API_VERSION,
  lifespan=lifespan,
)


@app.exception_handler(UnknownCategoryError)
async def unknown_category_handler(
  _: Request,
  exc: UnknownCategoryError,
) -> JSONResponse:
  """Map unknown categorical values to a 422 validation-style response."""
  return JSONResponse(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    content={
      "detail": str(exc),
      "field": exc.field,
      "value": exc.value,
    },
  )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
  _: Request,
  exc: RequestValidationError,
) -> JSONResponse:
  """Return a consistent payload for invalid request bodies."""
  return JSONResponse(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    content={"detail": exc.errors()},
  )


@app.get("/", response_model=RootResponse, tags=["System"])
def read_root() -> RootResponse:
  """Return API status and loaded model metadata."""
  metadata = model_service.model_metadata()
  return RootResponse(
    status="ok",
    service=SERVICE_NAME,
    version=API_VERSION,
    **metadata,
  )


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check() -> HealthResponse:
  """Return a lightweight health probe for orchestrators and load balancers."""
  if not model_service.is_loaded:
    raise HTTPException(
      status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
      detail="Model artifacts are not loaded.",
    )
  return HealthResponse(status="healthy")


@app.post(
  "/predict",
  response_model=TrafficPredictionResponse,
  tags=["Inference"],
  summary="Classify a network traffic session",
)
def predict_traffic(
  payload: TrafficPredictionRequest,
) -> TrafficPredictionResponse:
  """
  Classify a single network flow as Normal or Attack.

  Categorical fields are encoded with persisted label encoders before inference.
  """
  if not model_service.is_loaded:
    raise HTTPException(
      status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
      detail="Model artifacts are not loaded.",
    )

  try:
    return model_service.predict(payload)
  except UnknownCategoryError:
    raise
  except ValueError as exc:
    raise HTTPException(
      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
      detail=str(exc),
    ) from exc
  except Exception as exc:
    logger.exception("Unexpected prediction failure.")
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Prediction failed due to an internal error.",
    ) from exc
