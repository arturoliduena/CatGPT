from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from pydantic_settings import BaseSettings, SettingsConfigDict
import structlog
from supabase.client import Client, create_client

_logger = structlog.get_logger()


class SupabaseConfig(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    supabase_url: str
    supabase_key: str


class VectorStore:
    embeddings_model = "BAAI/bge-m3"

    def __init__(
        self,
        settings: SupabaseConfig = SupabaseConfig(),
    ):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embeddings_model, model_kwargs={"device": "cpu"}
        )
        self.client: Client = create_client(
            settings.supabase_url, settings.supabase_key
        )
        _logger.info("RAG loaded!")


VectorStore()
