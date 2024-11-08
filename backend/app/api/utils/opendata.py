import requests
import structlog
from pydantic_settings import BaseSettings, SettingsConfigDict

_logger = structlog.get_logger()


class ModelsSettings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    hf_token: str
    open_data_api_key: str


settings = ModelsSettings()


async def get_open_data(municipe_code: str):
    url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/{municipe_code}"
    headers = {"api_key": settings.open_data_api_key}
    res = requests.get(url, headers=headers)
    res_json = res.json()
    res = requests.get(res_json["datos"])
    _logger.info("Open data response: %s", res.json())
    return res.json()
