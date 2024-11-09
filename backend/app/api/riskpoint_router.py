from typing import Dict, List

import structlog
from fastapi import APIRouter, Path

from app.services import riskpoint_service

_logger = structlog.get_logger()

router = APIRouter()


@router.get("/municipalities/{municipality_code}/riskpoints")
async def get_riskpoints(municipality_code: str = Path(...)) -> List[Dict]:
    _logger.info(f"GET /municipalities/{municipality_code}/riskpoints")
    return riskpoint_service.get_riskpoint(municipality_code)
