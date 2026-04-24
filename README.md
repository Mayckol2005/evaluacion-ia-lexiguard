# ⚖️ LexiGuard - Asistente Legal con IA (RAG)

**LexiGuard** es una solución de Inteligencia Artificial diseñada para **LexiFlow Solutions**, una consultora especializada en cumplimiento corporativo y derecho laboral en Chile. El sistema utiliza una arquitectura de **Generación Aumentada por Recuperación (RAG)** basada en agentes para analizar contratos y normativas chilenas con alta precisión, mitigando el riesgo de alucinaciones y garantizando la trazabilidad de la información.

---

## 🎯 Objetivo del Proyecto
Automatizar la revisión legal de más de 5.000 documentos internos de la consultora, contrastándolos con la normativa chilena vigente (Ley Chile) para detectar riesgos de incumplimiento, reducir tiempos de revisión en un 70% y asegurar la precisión jurídica mediante citas exactas a las fuentes documentales.

## 🛠️ Arquitectura y Tecnologías
El sistema está diseñado bajo un enfoque modular y escalable:

* **Orquestador:** LangChain / LlamaIndex
* **Base de Datos Vectorial:** ChromaDB / Pinecone (Almacenamiento de embeddings de los 5.000 documentos)
* **Modelo de Lenguaje (LLM):** OpenAI (GPT-4) o Anthropic (Claude)
* **Fuentes Externas (API):** API de la Biblioteca del Congreso Nacional (BCN) - Ley Chile
* **Diagramación:** Mermaid

## ✨ Características Principales
1. **Control de Alucinaciones (Grounding):** El LLM está restringido a responder *únicamente* usando los fragmentos de texto recuperados por la base de datos vectorial.
2. **Trazabilidad de Datos:** Inyección de metadatos que obliga a la IA a citar el documento fuente y la cláusula específica en cada respuesta.
3. **Validación en Tiempo Real:** Búsqueda asíncrona que contrasta los contratos privados con las leyes públicas actualizadas mediante la API de la BCN.
4. **Agente Inteligente:** Toma de decisiones autónoma para usar la herramienta de búsqueda interna (documentos) o externa (leyes) según el contexto de la pregunta del usuario.
