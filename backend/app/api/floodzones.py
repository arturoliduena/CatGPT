import structlog
from fastapi import APIRouter, Path

from app.core.supabase_con.connect import connect

_logger = structlog.get_logger()
router = APIRouter()

@router.get("/municipalities/{municipality_code}/floodzones")
async def floodzones(municipality_code: str = Path(...)):
    _logger.info(f"GET /floodzones/{municipality_code}")
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        f"""SELECT b.codimuni, b.nommuni, ST_AsGeoJSON(a.wgs84_geometry)
FROM floodzones a, municipalities b
WHERE 
	b.codimuni = '{municipality_code}' and
	ST_Within(a.wgs84_geometry, ST_Envelope(b.wkb_geometry));
"""
    )
    data = cur.fetchall()
    result = []
    for muni in data:
        result.append({"codiMunicipi": muni[0], "nomMunicipi": muni[1], "geom": muni[2]})

    return result