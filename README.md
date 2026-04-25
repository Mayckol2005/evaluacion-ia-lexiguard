# ⚖️ LexiGuard - Asistente Legal con IA (RAG)

LexiGuard es una solución de Inteligencia Artificial diseñada para **LexiFlow Solutions**, una consultora especializada en cumplimiento corporativo y derecho laboral en Chile. El sistema utiliza una arquitectura de **Generación Aumentada por Recuperación (RAG)** para analizar contratos y normativas chilenas con alta precisión, mitigando el riesgo de alucinaciones y garantizando la trazabilidad de la información.

---

## 🎯 Objetivo del Proyecto
Automatizar la revisión legal de documentos internos, contrastándolos con normativas específicas para detectar riesgos de incumplimiento, reducir tiempos de revisión y asegurar la precisión jurídica mediante el uso de fuentes documentales verificables.

## 🛠️ Arquitectura y Tecnologías Implementadas
Para esta fase de evaluación, el sistema se construyó con el siguiente stack tecnológico:

* **Modelo de Lenguaje (LLM):** Google Gemini 1.5 Flash (vía API).
* **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (HuggingFace) para la vectorización local de alta eficiencia.
* **Orquestador:** LangChain (Arquitectura RAG directa y Agentes ReAct).
* **Base de Datos Vectorial:** ChromaDB (Persistencia local de fragmentos de documentos).
* **Procesamiento de Documentos:** PyPDF para la extracción de texto de contratos en formato PDF.

## 🚀 Implementación Técnica (Fase de Evaluación)
Durante el desarrollo se implementaron y testearon los siguientes componentes:

* **Pipeline de Ingesta:** Carga de PDFs, división de texto en fragmentos (*chunks*) y generación de embeddings para almacenamiento en la base de datos vectorial (`chroma_db`).
* **Sistema de Recuperación:** Implementación de búsqueda por similitud de coseno para extraer los 3 fragmentos más relevantes de cada consulta.
* **Interfaz de Agente:** Se intentó inicialmente una implementación mediante Agentes ReAct (`AgentExecutor`) para otorgar autonomía en la toma de decisiones. Ante desafíos de compatibilidad de versiones de librerías modernas (LangChain 0.3.x / Pydantic V2), se migró exitosamente a una arquitectura de RAG Directo, garantizando estabilidad y precisión en la respuesta del LLM.

## ✨ Características Principales
* **Control de Alucinaciones (Grounding):** El LLM recibe instrucciones estrictas para responder únicamente basándose en el contexto extraído del contrato de FedEx analizado.
* **Local Embeddings:** Uso de modelos de HuggingFace corriendo localmente para optimizar costos y mejorar la velocidad de búsqueda.
* **Prompt Engineering Avanzado:** Uso de plantillas personalizadas que definen el rol de LexiGuard como experto legal chileno.

## 🔧 Desafíos y Lecciones Aprendidas
* **Compatibilidad de Ecosistema:** Se trabajó profundamente en la resolución de conflictos entre versiones de dependencias (Pydantic, LangChain Core y Google GenAI), logrando un entorno virtual estable.
* **Consumo de APIs:** Ajuste dinámico de parámetros de conexión con Google Gemini para manejar versiones de API (v1 vs v1beta) según la región y disponibilidad de modelos.
* **Modularidad:** La separación entre `ingestion.py` y `agent.py` permite escalar la base de conocimientos sin necesidad de procesar los documentos en cada consulta.

---
