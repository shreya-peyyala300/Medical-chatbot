from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
#from langchain.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
def load_pdf_files(directory):
    loader = DirectoryLoader(
        directory,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )

    documents = loader.load()
    return documents

def filter_to_minimal_docs(docs: List[Document])->List[Document]:
    minimal_docs: List[Document]=[]
    for doc in docs:
        src=doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source":src}
            )
        )

    return minimal_docs

def text_split(minimal_docs):
    text_split=RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20
    )
    texts_chunk=text_split.split_documents(minimal_docs)
    return texts_chunk


#Embedding 
import torch
#from langchain.embeddings import HuggingFaceEmbeddings
def download_embeddings():
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    embeddings=HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device":"cuda" if torch.cuda.is_available() else "cpu"}
    )
    return embeddings