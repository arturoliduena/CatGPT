import requests
import structlog

_logger = structlog.get_logger()


async def get_open_data():
    url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/montaña/pasada/area/peu1"
    headers = {
        "api_key": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJydmVjaWFuYUBnbWFpbC5jb20iLCJqdGkiOiI3YTZiYjFjYi1lZDc4LTQ5NTUtYjI5Ni05YTliY2ZiZGQ1YzIiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTczMDM5NjYyNywidXNlcklkIjoiN2E2YmIxY2ItZWQ3OC00OTU1LWIyOTYtOWE5YmNmYmRkNWMyIiwicm9sZSI6IiJ9.USMSRChqiP-HIMSBsmyLvBpSZXzLolqaNC1eP28mUfI"
    }
    res = requests.get(url, headers=headers)
    res_json = res.json()
    res = requests.get(res_json["datos"])
    _logger.info("Open data response: %s", res.json())
    return res.json()
