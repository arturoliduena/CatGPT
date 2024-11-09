from typing import List

from app.core.supabase_con.connect import connect
from app.schemas.flood_municipality import FloodMunicipality


class FloodMunicipalityRepository:

    def __init__(self):
        self.conn = connect()


    def get_flood_municipality_zones(self, municipality_code: str) -> List[FloodMunicipality]:
        cur = self.conn.cursor()
        cur.execute(
            f"SELECT codimuni, nommuni, floodable_geometry, ST_AsEWKT(floodable_geometry) FROM flood_municipalities WHERE codimuni = '{municipality_code}'")
        result = cur.fetchall()
        return [
            FloodMunicipality(
                municipality_code=_result[0],
                municipality_name=_result[1],
                floodable_geometry=_result[2],
                floodable_geometry_ewkt=_result[3]
            )
            for _result in result
        ]
