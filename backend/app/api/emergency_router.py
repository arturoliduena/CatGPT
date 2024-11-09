import json

import structlog
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.api.utils.opendata import get_open_data
from app.clients.models import TextGeneration

_logger = structlog.get_logger()
router = APIRouter()


class PrecipitationSummaryParams(BaseModel):
    municipe_code: str = Field(..., description="The code of the municipality")
    alert_message: str = Field(..., description="The code of the municipality")


@router.post("/forecast-summary")
async def get_forecast_summary(params: PrecipitationSummaryParams = Depends()):
    _logger.info("GET /forcast-summary", municipe_code=params.municipe_code)
    open_data = await get_open_data(params.municipe_code)
    open_data = open_data[0]
    open_data["prediccion"]["dia"] = [open_data["prediccion"]["dia"][0]]
    json_text = json.dumps(open_data, indent=4)
    text_generation = TextGeneration(
        base_url="https://hijbc1ux6ie03ouo.us-east-1.aws.endpoints.huggingface.cloud",
    )
    # Define a focused system message
    system_message = (
        "You are a weather assistant. Based on the following data, provide a clear summary of the rain and precipitation forecast. "
        "Include details like the probability of precipitation, expected rainfall amounts, cloud coverage, and any indications of storms or fog. "
        "If no precipitation is expected, clarify that as well. Use the format:\n"
        "Location: {location}\n"
        "Date: {date}\n"
        "Rain Probability: {prob_precipitation}%\n"
        "Rain Amount: {rain_amount} mm\n"
        "Cloud Cover: {cloud_cover}\n"
        "Other conditions: {other_conditions}"
    )

    # Define messages to send for text generation
    messages = [
        {
            "role": "system",
            "content": system_message + "\n\n" + json_text,
        },
        {
            "role": "user",
            "content": "Provide a summary of the rain and precipitation forecast.",
        },
    ]
    return text_generation.generate_text(messages=messages)
