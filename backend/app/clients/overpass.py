from typing import List, Dict

import requests
from pydantic_settings import BaseSettings, SettingsConfigDict


class OverpassSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    overpass_url: str


class Overpass:

    AMENITY_LIST = [
        "school",
        "college",
        "kindergarten",
        "library",
        "university",
        "clinic",
        "hospital",
        "veterinary",
        "cinema",
        "place_of_worship",
        "refugee_site"
    ]

    def __init__(
            self,
            settings: OverpassSettings = OverpassSettings(),
    ):
        self.overpass_url = settings.overpass_url

    def get_overpass_elements(self, polygon: str) -> List[Dict]:
        url = self._build_url(polygon)
        response = requests.get(url)
        if response.status_code == 200:
            return self._parse_response(response.json())
        else:
            return []

    def _build_url(self, polygon: str) -> str:
        url = f'{self.overpass_url}/api/interpreter?data=[out:json][timeout:25000];('
        for amenity in self.AMENITY_LIST:
            url += f'nwr["amenity"="{amenity}"](poly:"{polygon}");'
        url += ");out center;"
        return url

    def _parse_response(self, response: Dict) -> List[Dict]:
        _elements = response.get("elements")
        return [element.get("tags") for element in _elements]
