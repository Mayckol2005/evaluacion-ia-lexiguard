import os

from langchain_core.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

PERSIST_DIRECTORY = "chroma_db"

# Variable global a nivel de módulo para comunicar la precisión del RAG al agente
ULTIMA_PRECISION_RAG = 1.0

print("Cargando modelo de embeddings locales (all-MiniLM-L6-v2)...")

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

if os.path.exists(PERSIST_DIRECTORY):
    vector_store = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )
else:
    vector_store = None
    print(
        f"⚠ No se encontró '{PERSIST_DIRECTORY}'. Ejecuta primero ingestion.py"
    )


def obtener_ultima_precision():
    """Permite al agente consultar el score de la última ejecución."""
    global ULTIMA_PRECISION_RAG
    return round(ULTIMA_PRECISION_RAG, 4)


def recuperar_contexto(
    consulta: str,
    k: int = 3,
    umbral_similitud: float = 0.35
):
    """
    Recuperación semántica optimizada con cálculo de score de precisión.
    Filtra fragmentos irrelevantes utilizando las distancias vectoriales de Chroma.
    """
    global ULTIMA_PRECISION_RAG

    if vector_store is None:
        ULTIMA_PRECISION_RAG = 0.0
        return "Error: Base de conocimientos no disponible."

    try:
        # Usamos similarity_search_with_score para obtener las distancias L2 de Chroma
        docs_con_score = vector_store.similarity_search_with_score(
            consulta,
            k=k
        )

        resultados = []
        vistos = set()
        scores_similitud = []

        for doc, distancia in docs_con_score:
            texto = doc.page_content.strip()

            # En Chroma, menor distancia es mayor similitud. 
            # Convertimos la distancia L2 a un porcentaje de precisión estimado (0.0 a 1.0)
            similitud = max(0.0, min(1.0, 1.0 - (distancia / 2.0)))

            # Corrección Profesor: Filtramos textos irrelevantes bajo el umbral configurado
            if similitud >= umbral_similitud and texto not in vistos:
                vistos.add(texto)
                scores_similitud.append(similitud)
                resultados.append(texto)

        # Guardamos el promedio de precisión de los fragmentos recuperados (Métrica IE1)
        if scores_similitud:
            ULTIMA_PRECISION_RAG = sum(scores_similitud) / len(scores_similitud)
        else:
            ULTIMA_PRECISION_RAG = 0.0

        if not resultados:
            return (
                "No se encontraron cláusulas o fragmentos con la suficiente "
                "relevancia semántica en el contrato actual para responder con certeza."
            )

        return "\n\n----------------------------------------\n\n".join(
            resultados
        )

    except Exception as e:
        ULTIMA_PRECISION_RAG = 0.0
        return f"Error durante la recuperación: {e}"


@tool
def buscar_en_contrato(consulta: str) -> str:
    """
    Realiza una búsqueda semántica general sobre el contrato.
    """
    contexto = recuperar_contexto(
        consulta=consulta,
        k=4,
        umbral_similitud=0.35
    )
    return (
        "Fragmentos relevantes encontrados en el contrato:\n\n"
        f"{contexto}"
    )


@tool
def buscar_clausula(clausula: str) -> str:
    """
    Localiza cláusulas específicas del contrato.
    """
    contexto = recuperar_contexto(
        consulta=clausula,
        k=3,
        umbral_similitud=0.40
    )
    return (
        f"Cláusulas relacionadas con '{clausula}':\n\n"
        f"{contexto}"
    )


@tool
def resumir_contrato() -> str:
    """
    Recupera los fragmentos más relevantes para elaborar
    un resumen del contrato.
    """
    consulta = (
        "objeto del contrato empresa trabajador cargo funciones "
        "obligaciones vigencia jornada remuneración"
    )
    contexto = recuperar_contexto(
        consulta=consulta,
        k=5,
        umbral_similitud=0.30
    )
    return (
        "Resumen estructural construido dinámicamente a partir de las "
        "cláusulas principales del documento indexado:\n\n"
        f"{contexto}"
    )


@tool
def obtener_duracion_contrato() -> str:
    """
    Recupera información relacionada con la vigencia,
    duración y fechas importantes del contrato.
    """
    consulta = (
        "vigencia contrato fecha de inicio fecha de término duración plazo"
    )
    contexto = recuperar_contexto(
        consulta=consulta,
        k=4,
        umbral_similitud=0.38  # Mayor exigencia para evitar textos de fraude ruidosos
    )
    return (
        "Información temporal y de vigencia recuperada dinámicamente:\n\n"
        f"{contexto}"
    )