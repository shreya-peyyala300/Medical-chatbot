from langchain_pinecone import PineconeVectorStore
from src.helper import load_pdf_files,filter_to_minimal_docs,text_split,download_embeddings
from pinecone import Pinecone
from pinecone import ServerlessSpec
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


extract_data=load_pdf_files("data/")
minimal_docs=filter_to_minimal_docs(extract_data)

text_chunk=text_split(minimal_docs)
print(f"Number of chunks: {len(text_chunk)}")

embeddings=download_embeddings()
pinecone_api_key=PINECONE_API_KEY
pc=Pinecone(api_key=pinecone_api_key)


index_name = "medical-chatbot"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",  # cosine similarity
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index=pc.Index(index_name)


docSearch=PineconeVectorStore.from_documents(
    documents=text_chunk,
    embedding=embeddings,
    index_name=index_name
)