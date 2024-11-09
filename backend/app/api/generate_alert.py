import json

import structlog
from fastapi import APIRouter, Body
from pydantic import BaseModel, Field

from app.clients.models import TextGeneration, Translation
from app.clients.vectorstore import VectorStore
from app.services import riskpoint_service
from app.services.opendata import get_open_data

_logger = structlog.get_logger()
router = APIRouter()


class PrecipitationSummaryParams(BaseModel):
    municipe_code: str = Field(..., description="The code of the municipality")
    alert_message: str = Field(..., description="The code of the municipality")


base_url = "https://hijbc1ux6ie03ouo.us-east-1.aws.endpoints.huggingface.cloud"


@router.post("/generate-alert")
async def generate_alert(params: PrecipitationSummaryParams = Body()):
    _logger.info("POST /generate-alert", municipe_code=params.municipe_code)
    open_data = await get_open_data(params.municipe_code)
    open_data = open_data[0]
    open_data["prediccion"]["dia"] = [open_data["prediccion"]["dia"][0]]
    json_text = json.dumps(open_data, indent=4)
    riskpoints = riskpoint_service.get_riskpoint(params.municipe_code)
    # Define a query string to find similar documents
    query = "Quines són les mesures a seguir en cas d'inundació?"
    # Perform the similarity search
    similar_docs = VectorStore().similarity_search(query, top_k=3)
    translated_docs = []
    for doc in similar_docs:
        translated_docs.append(
            Translation(base_url=base_url).translate_text(
                src_lang_code="Catalan",
                tgt_lang_code="English",
                sentence=doc.page_content,
            )
        )
    # Format similar documents for inclusion in the system message
    similar_docs_text = "\n".join(
        f"{i}. {doc}" for i, doc in enumerate(translated_docs, 1)
    )
    # Print the results
    for i, doc in enumerate(similar_docs, 1):
        _logger.info("Document", index=i, document=doc.page_content)
    riskpoints_text = "\n".join(
        f"{rp['amenity'].capitalize()}: {rp['name']} (Ref: {rp['ref']})"
        for rp in riskpoints
    )
    text_generation = TextGeneration(
        base_url=base_url,
    )

    # Define a more structured, human-readable system message
    system_message = (
        f"You are a detailed weather assistant tasked with providing an informative, clear, and user-friendly weather alert based on the provided forecast data. "
        f"Your goal is to explain the weather conditions in an easily understandable manner, while also giving practical safety advice based on the flood risk and relevant documents.\n\n"
        f"### **Weather Forecast for the Affected Area:**\n"
        f"Please summarize the key weather conditions expected for the next 24 hours, providing the following details based on the input data:\n"
        f"- **Location**: {open_data['nombre']}, {open_data['provincia']}.\n"
        f"- **Date**: {open_data['prediccion']['dia'][0]['fecha']}.\n"
        f"- **Sky Conditions**: {open_data['prediccion']['dia'][0]['estadoCielo'][0]['descripcion']} (e.g., overcast, clear, cloudy).\n"
        f"- **Precipitation**: {open_data['prediccion']['dia'][0]['precipitacion'][0]['value']} mm of rain expected with a probability of {open_data['prediccion']['dia'][0]['probPrecipitacion'][0]['value']}%.\n"
        f"- **Temperature**: {open_data['prediccion']['dia'][0]['temperatura'][0]['value']}°C, feels like {open_data['prediccion']['dia'][0]['sensTermica'][0]['value']}°C.\n"
        f"- **Wind**: Wind from {open_data['prediccion']['dia'][0]['vientoAndRachaMax'][0]['direccion'][0]} at {open_data['prediccion']['dia'][0]['vientoAndRachaMax'][0]['velocidad'][0]} km/h with gusts up to {open_data['prediccion']['dia'][0]['vientoAndRachaMax'][1]['value']} km/h.\n"
        f"- **Humidity**: Relative humidity is {open_data['prediccion']['dia'][0]['humedadRelativa'][0]['value']}%.\n"
        f"- **Other Conditions**: Storm chance of {open_data['prediccion']['dia'][0]['probTormenta'][0]['value']}%.\n\n"
        f"### **Flood Risk and Safety Measures**:\n"
        f"Provide information on the risk of flooding and any safety measures to follow, using the flood safety documents (from the similar docs) to give actionable advice. Please include the following:\n"
        f"- **Risk Points**: Critical locations that are at risk of flooding:\n"
        f"  - {riskpoints_text}.\n"
        f"- **Evacuation Plans and Measures**: Based on flood safety documents, you can include steps such as the evacuation of residents, relocation to safe shelters, or any actions that need to be taken. For example:\n"
        f"  - {similar_docs_text}\n"
        f"- **Recommendations**: Based on the forecast and safety measures, suggest steps residents should take to protect themselves and others (e.g., avoid flood-prone areas, prepare an emergency kit, stay informed via official sources).\n\n"
        f"### **Important Notes**:\n"
        f"Please ensure that your summary is:\n"
        f"- **Clear and Easy to Understand**: Use simple language and provide a detailed but digestible explanation of weather conditions and safety measures.\n"
        f"- **Actionable**: Provide practical advice that residents can follow to stay safe.\n"
        f"- **Comprehensive**: Include all the relevant weather information and safety measures in detail, addressing both the short-term conditions and the flood-related risks.\n\n"
        f"End with a reminder for residents to stay updated on weather alerts and to follow local emergency guidelines if the situation worsens."
    )

    # Define messages to send for text generation
    messages = [
        {
            "role": "system",
            "content": system_message,
        },
        {
            "role": "user",
            "content": "Please provide a comprehensive and human-readable weather alert, summarizing the forecast, explaining the weather conditions, and providing safety measures for flood risks. Include all relevant details about the weather, affected locations, and necessary actions for residents.",
        },
    ]
    return text_generation.generate_text(messages=messages)
