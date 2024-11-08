import requests
import structlog
from openai import OpenAI
from pydantic_settings import BaseSettings, SettingsConfigDict

_logger = structlog.get_logger()


class ModelsSettings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    hf_token: str


class OpenAIClient:

    model: str = "tgi"
    stream: bool = False
    max_tokens: int = 1000

    def __init__(
        self,
        base_url: str,
        temperature: float = 0.0,
        settings: ModelsSettings = ModelsSettings(),
    ):
        self.client = OpenAI(base_url=base_url + "/v1/", api_key=settings.hf_token)
        self.temperature = temperature

    def answer(self, messages: list = []):
        _logger.info("Generating answer with messages: %s", messages)
        try:
            chat_completion = self.client.chat.completions.create(
                model=self.model,
                stream=self.stream,
                max_tokens=self.max_tokens,
                messages=messages,
                temperature=self.temperature,
            )
            _logger.info("Answer generated successfully")
            return chat_completion.choices[0].message.content
        except Exception as e:
            _logger.error("Error generating answer: %s", e)
            raise

    def generate(self, prompt: str = ""):
        _logger.info("Generating completion with prompt: %s", prompt)
        try:
            completion = self.client.completions.create(
                model=self.model,
                stream=self.stream,
                max_tokens=self.max_tokens,
                prompt=prompt,
                temperature=self.temperature,
            )
            _logger.info("Completion generated successfully")
            return completion.choices[0].text
        except Exception as e:
            _logger.error("Error generating completion: %s", e)
            raise


class TextGeneration(OpenAIClient):

    def generate_text(self, messages: list = []):
        _logger.info("Generating text with messages: %s", messages)
        try:
            return self.answer(messages=messages)
        except Exception as e:
            _logger.error("Error generating text: %s", e)
            raise Exception(f"Error: {e}")


class TextToSpeech:

    def __init__(self, api_url: str, settings: ModelsSettings = ModelsSettings()):
        self.api_url = api_url
        self.headers = {"Authorization": f"Bearer {settings.hf_token}"}

    def generate_audio(
        self,
        text: str,
        voice: str = "gina",
        accent: str = "valencia",
    ):
        _logger.info(
            "Generating audio with text: %s, voice: %s, accent: %s", text, voice, accent
        )
        data = {"text": text, "voice": voice, "accent": accent}
        try:
            response = requests.post(self.api_url, headers=self.headers, json=data)
            if response.status_code == 200:
                _logger.info("Audio generated successfully")
                return response.content
            else:
                _logger.error(
                    "Error generating audio: %s - %s",
                    response.status_code,
                    response.text,
                )
                raise Exception(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            _logger.error("Exception during audio generation: %s", e)
            raise


class Translation(OpenAIClient):
    def translate_text(
        self,
        src_lang_code: str = "Catalan",
        tgt_lang_code: str = "English",
        sentence: str = "",
    ):
        _logger.info(
            "Translating text from %s to %s: %s", src_lang_code, tgt_lang_code, sentence
        )
        prompt = f"[{src_lang_code}] {sentence} \n[{tgt_lang_code}]"
        try:
            return self.generate(prompt=prompt)
        except Exception as e:
            _logger.error("Error translating text: %s", e)
            raise Exception(f"Error: {e}")


# Usage examples
# text_gen = TextGeneration(
#     base_url="https://hijbc1ux6ie03ouo.us-east-1.aws.endpoints.huggingface.cloud",
# )
# result_gen = text_gen.generate_text(
#     messages=[
#         {
#             "role": "system",
#             "content": "Ets un asistent que ajuda als ajuntaments a donar avisos a la ciutadania.",
#         },
#         {
#             "role": "user",
#             "content": "Soc l'alcalde de Barcelona i vull enviar un missatge a la ciutadania sobre les inundacions.",
#         },
#     ],
# )
# print("Text generation:")
# print(result_gen)

# tts = TextToSpeech(
#     api_url="https://p1b28cv1e843tih1.eu-west-1.aws.endpoints.huggingface.cloud/api/tts"
# )
# response = tts.generate_audio("Bon dia Roger i Arturo, com esteu?")
# with open("output.wav", "wb") as f:
#     f.write(response)

# translation = Translation(
#     base_url="https://o9vasr2oal4oyt2j.us-east-1.aws.endpoints.huggingface.cloud"
# )
# result_trans = translation.translate_text(
#     src_lang_code="Catalan", tgt_lang_code="English", sentence=result_gen
# )
# print("Translation:")
# print(result_trans)
