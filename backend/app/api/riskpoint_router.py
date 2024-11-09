from typing import Dict, List

from fastapi import APIRouter, Path

from app.services import riskpoint_service

router = APIRouter()


@router.get("/municipalities/{municipality_code}/riskpoints")
async def get_riskpoints(municipality_code: str = Path(...)) -> List[Dict]:
    return riskpoint_service.get_riskpoint(municipality_code)
