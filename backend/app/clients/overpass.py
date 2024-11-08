from typing import List, Dict

import requests
from pydantic_settings import BaseSettings, SettingsConfigDict


class OverpassSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    overpass_url: str


class Overpass:

    def __init__(
            self,
            settings: OverpassSettings = OverpassSettings(),
    ):
        self.overpass_url = settings.overpass_url

    def get_overpass_elements(self, polygon: str) -> List[Dict]:
        url = self._build_base_url() + f'(poly:"{polygon}");out;'
        response = requests.get(url)
        if response.status_code == 200:
            return self._parse_response(response.json())
        else:
            raise Exception("Riskpoints not found")

    def _build_base_url(self) -> str:
        return f'{self.overpass_url}/api/interpreter?data=[out:json][timeout:25000];nwr["amenity"="school"]'

    def _parse_response(self, response: Dict) -> List[Dict]:
        _elements = response.get("elements")
        return [element.get("tags") for element in _elements]
