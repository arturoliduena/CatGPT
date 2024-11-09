from pydantic import Field, BaseModel


class FloodMunicipality(BaseModel):
    municipality_code: str = Field(...)
    municipality_name: str = Field(...)
    floodable_geometry: str = Field(...)
    floodable_geometry_ewkt: str = Field(...)
