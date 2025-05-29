# scripts/ingest.py

import os
import warnings
import logging
import pdfplumber
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from PyPDF2.errors import PdfReadWarning

# ✅ Load your OpenAI API key from .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# ✅ Suppress PDF parsing warnings
warnings.filterwarnings("ignore", category=PdfReadWarning)
logging.getLogger("pdfminer").setLevel(logging.ERROR)
logging.getLogger("PyPDF2").setLevel(logging.ERROR)

# ✅ Paths
DATA_DIR = "../pdf_data"
VECTOR_DIR = "../pdf_vectorstore"

def load_pdf_text(file_path):
    """Extract text from all pages of a PDF file."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def ingest_pdfs():
    """Ingest PDFs, split into chunks with per-file indexing, and store in FAISS."""
    all_chunks = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            print(f"📄 Processing: {file}")
            full_path = os.path.join(DATA_DIR, file)
            raw_text = load_pdf_text(full_path)

            doc = Document(page_content=raw_text, metadata={"source": file})
            file_chunks = splitter.split_documents([doc])

            for idx, chunk in enumerate(file_chunks):
                chunk.metadata["chunk_index"] = idx  # reset index per file
                chunk.metadata["summary"] = chunk.page_content[:50] + "..."
                chunk.metadata["source"] = file      # ensure file info stays

            all_chunks.extend(file_chunks)

    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    vectordb = FAISS.from_documents(all_chunks, embedding_model)
    vectordb.save_local(VECTOR_DIR)

    print(f"\n✅ Ingestion complete. {len(all_chunks)} chunks saved to FAISS.\n")

if __name__ == "__main__":
    ingest_pdfs()



# import os
# from dotenv import load_dotenv
# load_dotenv()  # ✅ Load your OpenAI API key from .env
#
# openai_api_key = os.getenv("OPENAI_API_KEY")
# import warnings
# from PyPDF2.errors import PdfReadWarning
# warnings.filterwarnings("ignore", category=PdfReadWarning)
# import logging
# logging.getLogger("pdfminer").setLevel(logging.ERROR)  # optional for pdfminer
# logging.getLogger("PyPDF2").setLevel(logging.ERROR)    # THIS is key
#
#
# import pdfplumber
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.docstore.document import Document
#
# DATA_DIR = "../pdf_data"
# VECTOR_DIR = "../pdf_vectorstore"
#
# def load_pdf_text(file_path):
#     text = ""
#     with pdfplumber.open(file_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() + "\n"
#     return text
#
# def ingest_pdfs():
#     all_docs = []
#     for file in os.listdir(DATA_DIR):
#         if file.endswith(".pdf"):
#             print(f"Processing: {file}")
#             full_path = os.path.join(DATA_DIR, file)
#             raw_text = load_pdf_text(full_path)
#
#             doc = Document(page_content=raw_text, metadata={"source": file})
#             all_docs.append(doc)
#
#     splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     chunks = splitter.split_documents(all_docs)
#
#     embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
#
#     vectordb = FAISS.from_documents(chunks, embedding_model)
#     vectordb.save_local(VECTOR_DIR)
#
#     print(f"✅ Ingestion complete. {len(chunks)} chunks saved to FAISS.")
#
# if __name__ == "__main__":
#     ingest_pdfs()
