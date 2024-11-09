import re
from typing import Dict, List

from app.clients.overpass import Overpass
from app.repositories.flood_municipality_repository import FloodMunicipalityRepository

overpass_client = Overpass()
flood_municipality_repository = FloodMunicipalityRepository()


def get_riskpoint(municipality_code: str) -> List[Dict]:
    flood_municipality_zones = (
        flood_municipality_repository.get_flood_municipality_zones(municipality_code)
    )
    print(flood_municipality_zones)

    response = []
    for zone in flood_municipality_zones:
        polygon = parse_geometry_ewkt(zone.floodable_geometry_ewkt)
        response = overpass_client.get_overpass_elements(polygon)
        if len(response) > 0:
            break
    return response


def _get_flood_zones_intersection(municipality_code: str) -> str:
    return "41.44259 1.21693 41.44552 1.20786 41.44527 1.20527 41.44471 1.20393 41.44357 1.19601 41.44438 1.19214 41.44323 1.18919 41.43939 1.18935 41.43815 1.19014 41.43789 1.18947 41.43636 1.19081 41.43401 1.19658 41.43319 1.19906 41.43325 1.19987 41.4342 1.2011 41.43476 1.204 41.4283 1.21057 41.42816 1.21102 41.42837 1.21129 41.42783 1.21227 41.42714 1.21272 41.42613 1.21382 41.42544 1.21449 41.42473 1.21305 41.42412 1.21259 41.42331 1.21279 41.42132 1.21592 41.42094 1.2144 41.42117 1.21187 41.42103 1.21116 41.42064 1.20538 41.39718 1.1961 41.3922 1.20882 41.38003 1.23898 41.38386 1.24046 41.38483 1.25366 41.38777 1.25227 41.39081 1.25596 41.39859 1.26119 41.40385 1.25939 41.40616 1.26327 41.40806 1.27096 41.41622 1.28159 41.41511 1.27506 41.41826 1.25654 41.42176 1.24653 41.43554 1.22864 41.44259 1.21693"


def parse_geometry_ewkt(geometry_ewkt: str):
    matches = re.search(r"\(\((.*?)\)\)", geometry_ewkt)
    if matches:
        coords = matches.group(1)
        return " ".join(
            f"{y} {x}" for x, y in (pair.split() for pair in coords.split(","))
        )

