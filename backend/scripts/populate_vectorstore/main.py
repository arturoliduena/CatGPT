from uuid import uuid4

from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.clients.vectorstore import VectorStore
from docling.document_converter import DocumentConverter
from langchain_core.documents import Document
import os
import structlog

_logger = structlog.get_logger()


def run():
    vectorstore = VectorStore(drop_old=True)
    converter = DocumentConverter()
    # read pdfs from docs folder
    docs_urls = ["https://interior.gencat.cat/web/.content/home/030_arees_dactuacio/proteccio_civil/plans_de_proteccio_civil/plans_de_proteccio_civil_a_catalunya/02-plans-especials/inuncat/document-pla-inuncat.pdf"]
    docs = []
    _logger.info("Reading pdfs")
    for doc_url in docs_urls:
        _logger.info("Processing file", doc_url=doc_url)
        doc = converter.convert(doc_url).document
        text = doc.export_to_markdown()
        docs.append(Document(page_content=text))

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    splits = text_splitter.split_documents(docs)
    vectorstore.add_documents(splits)


if __name__ == "__main__":
    run()
