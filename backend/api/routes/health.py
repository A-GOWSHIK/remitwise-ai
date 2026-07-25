"""
RemitWise AI – Route: Health
==============================
Simple health-check endpoint used by load balancers, orchestrators,
and NitroStack Studio to confirm the backend is running.
"""

import logging
import time
from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

from config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/health", tags=["Health"])

# Record startup time once
_START_TIME = time.time()


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: str
    uptime_seconds: float


@router.get(
    "",
    response_model=HealthResponse,
    summary="Health Check",
    description=(
        "Returns the current health status of the RemitWise AI backend. "
        "Use this endpoint for liveness and readiness probes."
    ),
)
def health_check() -> HealthResponse:
    """
    Liveness check endpoint.

    Returns a 200 OK with service metadata when the backend is operational.
    """
    uptime = round(time.time() - _START_TIME, 2)
    logger.debug("Health check called; uptime=%.2fs", uptime)
    return HealthResponse(
        status="ok",
        service=settings.APP_NAME,
        version=settings.APP_VERSION,
        timestamp=datetime.now(timezone.utc).isoformat(),
        uptime_seconds=uptime,
    )
