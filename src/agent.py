import os
from dotenv import load_dotenv

# Imports limpios
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.tools import tool

load_dotenv()

@tool
def buscar_en_contrato(consulta: str) -> str:
    """Busca información específica dentro del contrato de FedEx."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    docs = vectorstore.similarity_search(consulta, k=3)
    return "\n\n".join([doc.page_content for doc in docs])

def ejecutar_agente():
    print("\n--- LexiGuard Activo (Modo Directo) ---")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        temperature=0,
        client_options={"api_version": "v1"} 
    )
    
    pregunta = "¿Cuáles son las responsabilidades de FedEx según el contrato?"
    
    print("Buscando en el contrato...")
    try:
        contexto = buscar_en_contrato.invoke(pregunta)
        
        prompt = f"""Eres LexiGuard, un experto legal. 
        Basándote SOLO en el siguiente extracto del contrato de FedEx, responde la pregunta del usuario.
        
        CONTRATO:
        {contexto}
        
        PREGUNTA:
        {pregunta}
        """
        
        print("Generando respuesta final...")
        respuesta = llm.invoke(prompt)
        
        print("\nRespuesta de LexiGuard:")
        print("-" * 30)
        print(respuesta.content)
        print("-" * 30)
        
    except Exception as e:
        print(f"\nHubo un problema: {e}")

if __name__ == "__main__":
    ejecutar_agente()