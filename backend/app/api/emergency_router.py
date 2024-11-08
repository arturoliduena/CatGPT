import json

import structlog
from fastapi import APIRouter

from app.api.utils.opendata import get_open_data
from app.clients.models import TextGeneration

_logger = structlog.get_logger()
router = APIRouter()


@router.get("/emergency")
async def root():
    _logger.info("GET /emergency")
    open_data = await get_open_data()
    json_text = json.dumps(open_data, indent=4)

    text_generation = TextGeneration(
        base_url="https://hijbc1ux6ie03ouo.us-east-1.aws.endpoints.huggingface.cloud",
    )
    messages = [
        {
            "role": "system",
            "content": json_text,
        },
        {
            "role": "user",
            "content": "explain the context of the system message",
        },
    ]

    return text_generation.generate_text(messages=messages)
