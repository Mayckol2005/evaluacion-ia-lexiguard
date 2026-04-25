import os
import sys
from dotenv import load_dotenv

# === BLOQUE DE BLINDAJE ANTI-ERRORES ===
import pydantic
import langchain_core
if not hasattr(langchain_core, "pydantic_v1"):
    try:
        from pydantic import v1 as pydantic_v1
        langchain_core.pydantic_v1 = pydantic_v1
    except ImportError:
        langchain_core.pydantic_v1 = pydantic
# =======================================

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

def ejecutar_ingesta(ruta_pdf):
    print(f"--- Iniciando Ingesta Local de: {ruta_pdf} ---")
    
    if not os.path.exists(ruta_pdf):
        print(f"ERROR: No se encuentra el archivo en {ruta_pdf}")
        return

    loader = PyPDFLoader(ruta_pdf)
    paginas = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    textos = splitter.split_documents(paginas)
    
    print("Cargando modelo de embeddings local (all-MiniLM-L6-v2)...")
    # Usamos la forma más compatible de cargar el modelo
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    print("Guardando en base de datos local (chroma_db)...")
    vectorstore = Chroma.from_documents(
        documents=textos, 
        embedding=embeddings, 
        persist_directory="./chroma_db"
    )
    vectorstore.persist()
    print("¡VICTORIA! El conocimiento de FedEx ha sido guardado.")

if __name__ == "__main__":
    ejecutar_ingesta("data/contrato_fedex.pdf")