from datetime import datetime, timedelta

import requests
import structlog
from pydantic_settings import BaseSettings, SettingsConfigDict

_logger = structlog.get_logger()


class ModelsSettings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    open_data_api_key: str
    is_mock_open_data: bool


settings = ModelsSettings()


def mock_data(municipe_code: str, data: dict):
    next_day = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT00:00:00")
    data[0]["prediccion"] = {
        "dia": [
            {
                "fecha": next_day,
                "estadoCielo": [
                    {"value": "16n", "periodo": "00", "descripcion": "Cubierto"}
                ],
                "precipitacion": [
                    {"value": "5", "periodo": "00"}
                ],  # Mocked precipitation value
                "probPrecipitacion": [{"value": "85", "periodo": "0001"}],
                "probTormenta": [{"value": "20", "periodo": "0001"}],
                "nieve": [{"value": "0", "periodo": "00"}],
                "probNieve": [{"value": "0", "periodo": "0001"}],
                "temperatura": [{"value": "15", "periodo": "00"}],
                "sensTermica": [{"value": "14", "periodo": "00"}],
                "humedadRelativa": [{"value": "90", "periodo": "00"}],
                "vientoAndRachaMax": [
                    {"direccion": ["O"], "velocidad": ["10"], "periodo": "00"},
                    {"value": "20", "periodo": "00"},
                ],
                "orto": "08:00",
                "ocaso": "18:00",
            }
        ]
    }
    return data


async def get_open_data(municipe_code: str):
    url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/15046"
    headers = {"api_key": settings.open_data_api_key}
    res = requests.get(url, headers=headers)
    res_json = res.json()
    res = requests.get(res_json["datos"])
    _logger.info("Open data response: %s", res.json())

    if settings.is_mock_open_data:
        return mock_data(municipe_code, res.json())

    return res.json()
