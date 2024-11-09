import structlog
from fastapi import APIRouter, Path

from app.core.supabase_con.connect import connect

_logger = structlog.get_logger()
router = APIRouter()

@router.get("/municipalities/{municipality_code}/poi")
async def municipalities(municipality_code: str = Path(...)):
    _logger.info("GET /poi")
    conn = connect()
    cur = conn.cursor()

    cur.execute(f"SELECT codimuni, nommuni, amenity, intersects_floodzone, st_asewkt(wkb_geometry) as geom FROM public.poi where codimuni = '{municipality_code}'")
    result = cur.fetchall()
    return result