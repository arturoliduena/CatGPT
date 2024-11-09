import structlog
from fastapi import APIRouter, Body
from pydantic import BaseModel, Field

from app.api.poi_router import get_poi_list_for_LLM
from app.clients.models import TextGeneration, Translation
from app.clients.vectorstore import VectorStore
from app.services import riskpoint_service
from app.services.opendata import get_open_data

_logger = structlog.get_logger()
router = APIRouter()


class PrecipitationSummaryParams(BaseModel):
    municipe_code: str = Field(..., description="The code of the municipality")
    alert_message: str = Field(..., description="The alert message")
    severity: str = Field(..., description="The severity of the alert")
    target_audience: str = Field(..., description="The target audience of the alert")

mock_weather_data_res = " {'origen': {'productor': 'Agencia Estatal de Meteorología - AEMET. Gobierno de España', 'web': 'https://www.aemet.es', 'enlace': 'https://www.aemet.es/es/eltiempo/prediccion/municipios/horas/melide-id15046', 'language': 'es', 'copyright': '© AEMET. Autorizado el uso de la información y su reproducción citando a AEMET como autora de la misma.', 'notaLegal': 'https://www.aemet.es/es/nota_legal'}, 'elaborado': '2024-11-09T06:52:12', 'nombre': 'Melide', 'provincia': 'A Coruña', 'prediccion': {'dia': [{'fecha': '2024-11-10T00:00:00', 'estadoCielo': [{'value': '16n', 'periodo': '00', 'descripcion': 'Cubierto'}], 'precipitacion': [{'value': '5', 'periodo': '00'}], 'probPrecipitacion': [{'value': '85', 'periodo': '0001'}], 'probTormenta': [{'value': '20', 'periodo': '0001'}], 'nieve': [{'value': '0', 'periodo': '00'}], 'probNieve': [{'value': '0', 'periodo': '0001'}], 'temperatura': [{'value': '15', 'periodo': '00'}], 'sensTermica': [{'value': '14', 'periodo': '00'}], 'humedadRelativa': [{'value': '90', 'periodo': '00'}], 'vientoAndRachaMax': [{'direccion': ['O'], 'velocidad': ['10'], 'periodo': '00'}, {'value': '20', 'periodo': '00'}], 'orto': '08:00', 'ocaso': '18:00'}]}, 'id': '15046', 'version': '1.0'}"
import ast
async def fetch_weather_data(municipe_code: str):
    # data = await get_open_data(municipe_code)
    # return data[0]
    return ast.literal_eval(mock_weather_data_res)


amenities_dict = {
    "camp_site": "càmping", "cinema": "cinema", "clinic": "clínica", "college":"centre educatiu", 
    "hospital": "hospital", "kindergarten": "Escola infantil", "library": "biblioteca", 
    "place_of_worship": "Església", "school": "escola",
    "university": "universitat"
}

def format_risk_points(municipe_code: str):
    # riskpoints = riskpoint_service.get_riskpoint(municipe_code)
    # return "\n".join(f"{rp['amenity'].capitalize()}: {rp['name']}" for rp in riskpoints)
    poi = get_poi_list_for_LLM(municipe_code)

    result = ""
    for point in poi:
        result += f"{amenities_dict[point[2]]}:{point[3]} - {"no inundable" if point[4]==False else "inundable"}\n"

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
async def generate_alert(params: PrecipitationSummaryParams = Body()):
    _logger.info("POST /generate-alert", municipe_code=params.municipe_code)

    # Fetch data and risk points
    open_data = await fetch_weather_data(params.municipe_code)


    riskpoints_text = format_risk_points(params.municipe_code)

    similar_docs_text = translate_docs()

    text_generation = TextGeneration(
        base_url="https://hijbc1ux6ie03ouo.us-east-1.aws.endpoints.huggingface.cloud",
    )

        # f"You are a detailed weather assistant tasked with providing an informative, clear, and user-friendly weather alert based on the provided forecast data. "
        # f"Your goal is to explain the weather conditions in an easily understandable manner, while also giving practical safety advice based on the flood risk and relevant documents.\n\n"
        # f"### **Weather Forecast for the Affected Area:**\n"
        # f"Please summarize the key weather conditions expected for the next 24 hours, providing the following details based on the input data:\n"
        # f"- **Location**: {open_data['nombre']}, {open_data['provincia']}.\n"
        # f"- **Date**: {open_data['prediccion']['dia'][0]['fecha']}.\n"
        # f"- **Sky Conditions**: {open_data['prediccion']['dia'][0]['estadoCielo'][0]['descripcion']} (e.g., overcast, clear, cloudy).\n"
        # f"- **Precipitation**: {open_data['prediccion']['dia'][0]['precipitacion'][0]['value']} mm of rain expected with a probability of {open_data['prediccion']['dia'][0]['probPrecipitacion'][0]['value']}%.\n"
        # f"- **Temperature**: {open_data['prediccion']['dia'][0]['temperatura'][0]['value']}°C, feels like {open_data['prediccion']['dia'][0]['sensTermica'][0]['value']}°C.\n"
        # f"- **Wind**: Wind from {open_data['prediccion']['dia'][0]['vientoAndRachaMax'][0]['direccion'][0]} at {open_data['prediccion']['dia'][0]['vientoAndRachaMax'][0]['velocidad'][0]} km/h with gusts up to {open_data['prediccion']['dia'][0]['vientoAndRachaMax'][1]['value']} km/h.\n"
        # f"- **Humidity**: Relative humidity is {open_data['prediccion']['dia'][0]['humedadRelativa'][0]['value']}%.\n"
        # f"- **Other Conditions**: Storm chance of {open_data['prediccion']['dia'][0]['probTormenta'][0]['value']}%.\n\n"
        # f"### **Flood Risk and Safety Measures**:\n"
        # f"Provide information on the risk of flooding and any safety measures to follow, using the flood safety documents (from the similar docs) to give actionable advice. Please include the following:\n"
        # f"- **Risk Points**: Critical locations that are at risk of flooding:\n"
        # f"  - {riskpoints_text}.\n"
        # f"- **Evacuation Plans and Measures**: Based on flood safety documents, you can include steps such as the evacuation of residents, relocation to safe shelters, or any actions that need to be taken. For example:\n"
        # f"  - {similar_docs_text}\n"
        # f"- **Recommendations**: Based on the forecast and safety measures, suggest steps residents should take to protect themselves and others (e.g., avoid flood-prone areas, prepare an emergency kit, stay informed via official sources).\n\n"
        # f"### **Important Notes**:\n"
        # f"Please ensure that your summary is:\n"
        # f"- **Clear and Easy to Understand**: Use simple language and provide a detailed but digestible explanation of weather conditions and safety measures.\n"
        # f"- **Actionable**: Provide practical advice that residents can follow to stay safe.\n"
        # f"- **Comprehensive**: Include all the relevant weather information and safety measures in detail, addressing both the short-term conditions and the flood-related risks.\n\n"
        # f"End with a reminder for residents to stay updated on weather alerts and to follow local emergency guidelines if the situation worsens."
    # Define a more structured, human-readable system message
    system_message = (
        f"Ets un tècnic d'alertes d'inundació. La teva tasca és proveïr d'informació concisa i amigable sobre els perills quan les dades indiquen que pot haver-hi perill"
        f"L'usuari enviarà un text amb el missatge de perill i tu has de generar les recomanacions"
        f"***Condicions meteorològiques de l'àrea afectada***"
        f"Please summarize the key weather conditions expected for the next 24 hours, providing the following details based on the input data:\n"
        f"- **Date**: {open_data['prediccion']['dia'][0]['fecha']}.\n"
        f"- **Estat del cel**: {open_data['prediccion']['dia'][0]['estadoCielo'][0]['descripcion']}.\n"
        f"- **Precipitació**: {open_data['prediccion']['dia'][0]['precipitacion'][0]['value']} mm de pluja prevista amb una probabilitat del {open_data['prediccion']['dia'][0]['probPrecipitacion'][0]['value']}%.\n"
        f"**Probabilitat de tormenta**: {open_data['prediccion']['dia'][0]['probTormenta'][0]['value']}%.\n\n"
        f"### **Risc d'inundació i mesures preventives**:\n"
        f"Proporcioneu informació sobre el risc d'inundació i les mesures de seguretat a seguir, utilitzant els documents de seguretat contra inundacions (dels documents similars) per donar consells útils. Incloeu el següent:\n"
        f"- **Punts de risc**: Punts de risc en cas que hi hagi inundacions:\n"
        f"  - {riskpoints_text}.\n"
        f"- **Plans i mesures d'evacuació**: a partir dels documents de seguretat contra inundacions, podeu incloure mesures com ara l'evacuació dels residents, el trasllat a refugis segurs o qualsevol acció que calgui prendre. Per exemple:\n"
        f"  - {similar_docs_text}\n"
        f"**Recomanacions**: d'acord amb la previsió i les mesures de seguretat, suggereix les mesures que els residents haurien de prendre per protegir-se i protegir els altres (p. ex., evitar zones propenses a inundacions, preparar un kit d'emergència, mantenir-se informat a través de fonts oficials).\n\n"
        f"### **Notes Importants**:\n"
        f"Assegura’t que el teu resum sigui:\n"
        f"- **Clar i Fàcil d’Entendre**: Utilitza un llenguatge senzill i proporciona una explicació detallada però comprensible de les condicions meteorològiques i de les mesures de seguretat.\n"
        f"- **Pràctic**: Dona consells pràctics que els residents puguin seguir per mantenir-se segurs.\n"
        f"- **Complet**: Inclou tota la informació meteorològica rellevant i les mesures de seguretat detallades, abordant tant les condicions immediates com els riscos relacionats amb inundacions.\n\n"
        f"Finalitza amb un recordatori als residents perquè es mantinguin informats sobre els avisos meteorològics i segueixin les pautes d’emergència locals si la situació empitjora."

    )

    # Define messages to send for text generation
    messages = [
        {
            "role": "system",
            "content": system_message,
        },
        {
            "role": "user",
            "content": f"L'usuari acaba de rebre el següent avís, si us plau escriu les recomanacions: {params.alert_message}",
        },
    ]
    return text_generation.generate_text(messages=messages)
