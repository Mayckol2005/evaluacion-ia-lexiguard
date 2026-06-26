import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DATA_DIRECTORY = "data"
PERSIST_DIRECTORY = "chroma_db"

print(f"--- Iniciando Ingesta Local Temática en: {DATA_DIRECTORY} ---")

# 1. Buscar de forma dinámica TODOS los archivos PDF en la carpeta data
archivos_pdf = [f for f in os.listdir(DATA_DIRECTORY) if f.endswith('.pdf')]

if not archivos_pdf:
    print(f"No se encontraron archivos PDF en la carpeta '{DATA_DIRECTORY}'.")
    exit()

print(f"Archivos detectados para procesar: {archivos_pdf}")

# Lista para acumular todos los fragmentos de todos los documentos
todos_los_documentos = []

# 2. Cargar y dividir cada documento encontrado
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

for archivo in archivos_pdf:
    ruta_completa = os.path.join(DATA_DIRECTORY, archivo)
    print(f"Procesando: {ruta_completa}...")
    
    loader = PyPDFLoader(ruta_completa)
    docs = loader.load()
    
    fragmentos = text_splitter.split_documents(docs)
    todos_los_documentos.extend(fragmentos)

print(f"Total de fragmentos generados entre todos los contratos: {len(todos_los_documentos)}")

# 3. Inicializar embeddings locales
print("Cargando modelo de embeddings local (all-MiniLM-L6-v2)...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 4. Construir y persistir la base de datos vectorial
print(f"Guardando fragmentos en base de datos local ({PERSIST_DIRECTORY})...")

vectorstore = Chroma.from_documents(
    documents=todos_los_documentos,
    embedding=embeddings,
    persist_directory=PERSIST_DIRECTORY
)

print("¡VICTORIA! La base de conocimientos local ha sido actualizada exitosamente con todos los contratos.")