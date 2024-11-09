import structlog
from fastapi import APIRouter

from app.core.supabase_con.connect import connect

_logger = structlog.get_logger()
router = APIRouter()

@router.get("/municipalities")
async def municipalities():
    _logger.info("GET /municipalities")
    conn = connect()
    cur = conn.cursor()

    cur.execute('SELECT codimuni, nommuni, ST_Extent(wkb_geometry) as bbox FROM municipalities group by codimuni, nommuni')
    data = cur.fetchall()
    result = []
    for muni in data:
        result.append({"codiMunicipi": muni[0], "nomMunicipi": muni[1], "bbox": muni[2]})
    return result