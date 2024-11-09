import re
from typing import List, Dict

import structlog

from app.clients.overpass import Overpass
from app.repositories.flood_municipality_repository import FloodMunicipalityRepository

_logger = structlog.get_logger()
overpass_client = Overpass()
flood_municipality_repository = FloodMunicipalityRepository()

def get_riskpoint(municipality_code: str) -> List[Dict]:
    flood_municipality_zones = flood_municipality_repository.get_flood_municipality_zones(municipality_code)
    riskpoints = []
    for zone in flood_municipality_zones:
        polygon = parse_geometry_ewkt(zone.floodable_geometry_ewkt)
        if polygon is None:
            continue
        response = overpass_client.get_overpass_elements(polygon)
        for _response in response:
            riskpoints.append(_response)

    return riskpoints


def parse_geometry_ewkt(geometry_ewkt: str):
    matches = re.search(r'\(\((.*?)\)\)', geometry_ewkt)
    if matches:
        coords = matches.group(1)
        return " ".join(f"{y} {x}" for x, y in (pair.split() for pair in coords.split(',')))
    return None