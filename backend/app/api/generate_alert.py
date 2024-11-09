import ast

import structlog
from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel, Field

from app.api.poi_router import get_poi_list_for_LLM
from app.clients.models import TextGeneration, Translation
from app.clients.vectorstore import VectorStore
from app.services.opendata import get_open_data

_logger = structlog.get_logger()
router = APIRouter()


class PrecipitationSummaryParams(BaseModel):
    municipe_code: str = Field(..., description="The code of the municipality")
    municipe_name: str = Field(..., description="The name of the municipality")
    alert_message: str = Field(..., description="The alert message")
    severity: str = Field(..., description="The severity of the alert")
    target_audience: str = Field(..., description="The target audience of the alert")
    languages: str = Field(..., description="List of languages, separated by commas")

mock_weather_data_res = " {'origen': {'productor': 'Agencia Estatal de Meteorología - AEMET. Gobierno de España', 'web': 'https://www.aemet.es', 'enlace': 'https://www.aemet.es/es/eltiempo/prediccion/municipios/horas/melide-id15046', 'language': 'es', 'copyright': '© AEMET. Autorizado el uso de la información y su reproducción citando a AEMET como autora de la misma.', 'notaLegal': 'https://www.aemet.es/es/nota_legal'}, 'elaborado': '2024-11-09T06:52:12', 'nombre': 'Melide', 'provincia': 'A Coruña', 'prediccion': {'dia': [{'fecha': '2024-11-10T00:00:00', 'estadoCielo': [{'value': '16n', 'periodo': '00', 'descripcion': 'Cubierto'}], 'precipitacion': [{'value': '5', 'periodo': '00'}], 'probPrecipitacion': [{'value': '85', 'periodo': '0001'}], 'probTormenta': [{'value': '20', 'periodo': '0001'}], 'nieve': [{'value': '0', 'periodo': '00'}], 'probNieve': [{'value': '0', 'periodo': '0001'}], 'temperatura': [{'value': '15', 'periodo': '00'}], 'sensTermica': [{'value': '14', 'periodo': '00'}], 'humedadRelativa': [{'value': '90', 'periodo': '00'}], 'vientoAndRachaMax': [{'direccion': ['O'], 'velocidad': ['10'], 'periodo': '00'}, {'value': '20', 'periodo': '00'}], 'orto': '08:00', 'ocaso': '18:00'}]}, 'id': '15046', 'version': '1.0'}"


async def fetch_weather_data(municipe_code: str):
    # data = await get_open_data(municipe_code)
    # return data[0]
    return ast.literal_eval(mock_weather_data_res)


amenities_dict = {
    "camp_site": "càmping",
    "cinema": "cinema",
    "clinic": "clínica",
    "college": "centre educatiu",
    "hospital": "hospital",
    "kindergarten": "escola infantil",
    "library": "biblioteca",
    "place_of_worship": "església",
    "school": "escola",
    "university": "universitat",
}


def format_risk_points(municipe_code: str):
    # riskpoints = riskpoint_service.get_riskpoint(municipe_code)
    # return "\n".join(f"{rp['amenity'].capitalize()}: {rp['name']}" for rp in riskpoints)
    poi = get_poi_list_for_LLM(municipe_code)

    result = ""
    for point in poi:
        result += f"- {point[3]} ({amenities_dict[point[2]]}): {"no inundable" if point[4]==False else "inundable"}\n"

    return result


def translate_docs():
    # Define a query string to find similar documents
    query = "Quines són les mesures a seguir en cas d'inundació?"
    # Perform the similarity search
    similar_docs = VectorStore().similarity_search(query, top_k=3)
    # translated_docs = []
    # for doc in similar_docs:
    #     translated_docs.append(
    #         Translation(
    #             base_url="https://o9vasr2oal4oyt2j.us-east-1.aws.endpoints.huggingface.cloud"
    #         )
    # .translate_text(
    #     src_lang_code="Catalan",
    #     tgt_lang_code="English",
    #     sentence=doc.page_content,
    # )
    # )
    # Format similar documents for inclusion in the system message
    # similar_docs_text = "\n".join(
    #     f"{i}. {doc}" for i, doc in enumerate(translated_docs, 1)
    # )
    # for i, doc in enumerate(similar_docs, 1):
    #     _logger.info("Document", index=i, document=doc.page_content)

    return similar_docs


@router.post("/generate-alert")
async def generate_alert(
    params: PrecipitationSummaryParams = Body(),
    vectorstore: VectorStore = Depends(VectorStore),
):
    _logger.info(
        "POST /generate-alert",
        municipe_code=params.municipe_code,
        municipe_name=params.municipe_name,
        alert_message=params.alert_message,
        severity=params.severity,
        target_audience=params.target_audience,
    )

    # Fetch data and risk points
    open_data = await fetch_weather_data(params.municipe_code)

    riskpoints_text = format_risk_points(params.municipe_code)

    query = "Quines són les mesures a seguir en cas d'inundació?"
    similar_docs_text = vectorstore.similarity_search(query, top_k=3)
    # Format context for the system prompt
    context = "---\n"
    for doc in similar_docs_text:
        context += doc.page_content
        context += "\n---\n"

    text_generation = TextGeneration(
        base_url="https://hijbc1ux6ie03ouo.us-east-1.aws.endpoints.huggingface.cloud",
    )

    messages = [
        {
            "role": "user",
            "content": f"Genera consells de seguretat relacionats amb la següent alerta:\n\nAlerta: {params.alert_message}\nSeveritat de l'alerta: {params.severity}\nPúblic objectiu: {params.target_audience}\nCiutat: {params.municipe_name}\nContext:\n{context}Utilitza aquesta informació i el context per generar els consells de seguretat. Sigues clar i concís.",
        },
    ]
    result = text_generation.generate_text(messages=messages)
    result += f"\n\nPunts de risc:\n{riskpoints_text}"

    _logger.info("Text generation:", result=result)

    final_result = {"Catalan": result}

    translation = Translation(
                base_url="https://o9vasr2oal4oyt2j.us-east-1.aws.endpoints.huggingface.cloud"
            )
    
    if len(params.languages.split(",")) > 0:
        for language in params.languages.split(","):
            
            result_trans = translation.translate_text(
                src_lang_code="Catalan", tgt_lang_code="English", sentence=result
            )
            final_result[language]=result_trans
 

    return final_result
