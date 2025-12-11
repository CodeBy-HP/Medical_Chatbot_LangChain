from pinecone import Pinecone, ServerlessSpec
from src.helper import (
    load_pdf_files,
    filter_to_minimal_docs,
    text_split,
    download_embeddings,
)
from langchain_pinecone import PineconeVectorStore
from src.config import Config

Config.validate()


PINECONE_API_KEY = Config.PINECONE_API_KEY
GEMINI_API_KEY = Config.GEMINI_API_KEY


extracted_data = load_pdf_files(data=Config.DATA_PATH)
filter_data = filter_to_minimal_docs(extracted_data)
text_chunks = text_split(filter_data)

embedding = download_embeddings()


pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = Config.PINECONE_INDEX_NAME

# Create index if it doesn't exist
if not pc.has_index(index_name):
    print(f"Creating new Pinecone index: {index_name}")
    pc.create_index(
        name=index_name,
        dimension=Config.PINECONE_DIMENSION,
        metric=Config.PINECONE_METRIC,
        spec=ServerlessSpec(cloud=Config.PINECONE_CLOUD, region=Config.PINECONE_REGION),
    )


index = pc.Index(index_name)


print("Storing documents embeddings in Pinecone")
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks, embedding=embedding, index_name=index_name
)
