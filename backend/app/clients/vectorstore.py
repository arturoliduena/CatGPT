from langchain_huggingface import HuggingFaceEmbeddings

from langchain_core.documents import Document
import structlog

from langchain_milvus import Milvus

_logger = structlog.get_logger()


class VectorStore:
    embeddings_model = "BAAI/bge-m3"

    def __init__(
        self,
        drop_old: bool = False,
    ):
        embeddings = HuggingFaceEmbeddings(
            model_name=self.embeddings_model, model_kwargs={"device": "cpu"}
        )
        self._vectorstore = Milvus(
            embedding_function=embeddings,
            connection_args={"uri": f"./milvus.db"},
            drop_old=drop_old,
            auto_id=True,
        )
        _logger.info("VectorStore initialized")

    def add_documents(self, documents: list[Document]):
        self._vectorstore.add_documents(documents)

    def similarity_search(self, query: Document, top_k: int = 4):
        return self._vectorstore.similarity_search(query, top_k)


# VectorStore()
