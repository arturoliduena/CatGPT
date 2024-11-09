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

    cur.execute(
        "SELECT codimuni, nommuni, ST_Extent(wkb_geometry) as bbox FROM municipalities group by codimuni, nommuni"
    )
    data = cur.fetchall()
    result = []
    for muni in data:
        bbox_str = muni[2]
        bbox_coords = bbox_str.replace("BOX(", "").replace(")", "").split(",")
        xmin, ymin = map(float, bbox_coords[0].split())
        xmax, ymax = map(float, bbox_coords[1].split())
        bbox = {"xmin": xmin, "ymin": ymin, "xmax": xmax, "ymax": ymax}
        result.append({"codiMunicipi": muni[0], "nomMunicipi": muni[1], "bbox": bbox})
    return result
