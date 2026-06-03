from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import tool

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)


@tool
def buscar_en_contrato(consulta: str) -> str:
    """
    Busca información específica dentro del contrato.
    """

    docs = vectorstore.similarity_search(
        consulta,
        k=3
    )

    return "\n\n".join(
        [doc.page_content for doc in docs]
    )


@tool
def resumir_contrato() -> str:
    """
    Genera un resumen ejecutivo del contrato.
    """

    return """
Resumen Ejecutivo del Contrato

- Empresa usuaria: FedEx Express Chile SPA.
- Cargo: Operario de Bodega.
- Lugar de trabajo: Puerto Montt.
- Fecha de inicio: 17 de diciembre de 2025.
- Fecha de término: 31 de diciembre de 2025.
- El contrato corresponde a servicios transitorios.
- Se encuentra regulado por el Código del Trabajo.
- Define obligaciones laborales, remuneraciones y causales de término.
- Establece deberes de cumplimiento, seguridad y cuidado de equipos.
"""


@tool
def buscar_clausula(clausula: str) -> str:
    """
    Busca cláusulas específicas dentro del contrato.
    """

    docs = vectorstore.similarity_search(
        clausula,
        k=2
    )

    return "\n\n".join(
        [doc.page_content for doc in docs]
    )


@tool
def obtener_duracion_contrato() -> str:
    """
    Entrega información sobre la duración del contrato.
    """

    return """
Duración del Contrato

Fecha de inicio: 17 de diciembre de 2025.
Fecha de término: 31 de diciembre de 2025.

Tipo: Contrato de Servicios Transitorios.
"""