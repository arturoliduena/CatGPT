import structlog
from fastapi import APIRouter, Path

from app.core.supabase_con.connect import connect

_logger = structlog.get_logger()
router = APIRouter()

amenities_dict = {
    "camp_site": "càmping",
    "cinema": "cinema",
    "clinic": "clínica",
    "college": "centre educatiu",
    "hospital": "hospital",
    "kindergarten": "Escola infantil",
    "library": "biblioteca",
    "place_of_worship": "Església",
    "school": "escola",
    "university": "universitat",
}


def get_poi_list_for_LLM(municipality_code: str):
    conn = connect()
    cur = conn.cursor()

    cur.execute(f"SELECT codimuni, nommuni, amenity, name, intersects_floodzone FROM public.poi where codimuni = '{municipality_code}'")
    result = cur.fetchall()
    return result

@router.get("/municipalities/{municipality_code}/poi")
async def municipalities(municipality_code: str = Path(...)):
    _logger.info("GET /poi")
    conn = connect()
    cur = conn.cursor()

    cur.execute(f"SELECT codimuni, nommuni, amenity, intersects_floodzone, st_asewkt(wkb_geometry) as geom, name FROM public.poi where codimuni = '{municipality_code}'")
    data = cur.fetchall()

    result = []
    for muni in data:
        result.append({"codiMunicipi": muni[0], "nomMunicipi": muni[1], "amenity": amenities_dict[muni[2]], "floodable": muni[3], "geom": muni[4], "name": muni[5]})

    return result