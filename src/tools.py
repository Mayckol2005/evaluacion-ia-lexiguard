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
    Entrega un resumen general del contrato.
    """

    docs = vectorstore.similarity_search(
        "objetivo general del contrato",
        k=5
    )

    texto = "\n".join(
        [doc.page_content for doc in docs]
    )

    return texto[:1000]


@tool
def buscar_clausula(clausula: str) -> str:
    """
    Busca cláusulas específicas.
    """

    docs = vectorstore.similarity_search(
        clausula,
        k=2
    )

    return "\n".join(
        [doc.page_content for doc in docs]
    )