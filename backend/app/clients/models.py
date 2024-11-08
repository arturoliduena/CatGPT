from pydantic_settings import BaseSettings, SettingsConfigDict
from openai import OpenAI
import requests


class ModelsSettings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env")
    hf_token: str


class OpenAIClient:

    model: str = "tgi"
    stream: bool = False
    max_tokens: int = 1000

    def __init__(self, base_url: str, settings: ModelsSettings = ModelsSettings()):
        self.client = OpenAI(base_url=base_url + "/v1/", api_key=settings.hf_token)

    def answer(self, messages: list = []):
        chat_completion = self.client.chat.completions.create(
            model=self.model,
            stream=self.stream,
            max_tokens=self.max_tokens,
            messages=messages,
        )
        return chat_completion.choices[0].message.content

    def generate(self, prompt: str = ""):
        completion = self.client.completions.create(
            model=self.model,
            stream=self.stream,
            max_tokens=self.max_tokens,
            prompt=prompt,
        )
        return completion.choices[0].text


class TextGeneration(OpenAIClient):

    def generate_text(self, messages: list = []):
        try:
            return self.answer(messages=messages)
        except Exception as e:
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
        data = {"text": text, "voice": voice, "accent": accent}
        response = requests.post(self.api_url, headers=self.headers, json=data)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")


class Translation(OpenAIClient):
    def translate_text(
        self,
        src_lang_code: str = "Catalan",
        tgt_lang_code: str = "English",
        sentence: str = "",
    ):
        prompt = f"[{src_lang_code}] {sentence} \n[{tgt_lang_code}]"
        try:
            return self.generate(prompt=prompt)
        except Exception as e:
            raise Exception(f"Error: {e}")
