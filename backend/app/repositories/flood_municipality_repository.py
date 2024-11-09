from typing import List

from app.core.supabase_con.connect import connect
from app.schemas.flood_municipality import FloodMunicipality, FullFloodMunicipality


class FloodMunicipalityRepository:

    def get_flood_municipality_zones(self, municipality_code: str) -> List[FloodMunicipality]:
        conn = connect()
        cur = conn.cursor()
        cur.execute(
            f"SELECT codimuni, ST_AsEWKT(floodable_geometry) FROM flood_municipalities WHERE codimuni = '{municipality_code}'")
        result = cur.fetchall()
        return [
            FloodMunicipality(
                municipality_code=_result[0],
                floodable_geometry_ewkt=_result[1]
            )
            for _result in result
        ]

    def get_full_flood_municipality_zones(self, municipality_code: str) -> List[FullFloodMunicipality]:
        cur = self.conn.cursor()
        cur.execute(
            f"SELECT codimuni, nommuni, floodable_geometry, ST_AsEWKT(floodable_geometry) FROM flood_municipalities WHERE codimuni = '{municipality_code}'")
        result = cur.fetchall()
        return [
            FullFloodMunicipality(
                municipality_code=_result[0],
                municipality_name=_result[1],
                floodable_geometry=_result[2],
                floodable_geometry_ewkt=_result[3]
            )
            for _result in result
        ]
