# ⚖️ LexiGuard Agent - Asistente Legal Inteligente con RAG

**Proyecto Académico – Ingeniería de Soluciones con Inteligencia Artificial (ISY0101)**

**Docente:** Héctor Morel

## 👥 Integrantes

- Mayckol Mardones
- Martin Baza
- Martin Silva

---

## 📖 Descripción General

LexiGuard Agent es una solución de Inteligencia Artificial desarrollada para apoyar el análisis de contratos laborales y documentación legal mediante técnicas de Recuperación Aumentada por Generación (RAG).

El sistema combina búsqueda semántica sobre documentos legales, almacenamiento vectorial y herramientas especializadas para asistir en tareas de consulta, análisis y recuperación de información contractual.

---

## 🎯 Objetivo del Proyecto

Desarrollar un agente inteligente capaz de:

- Analizar contratos laborales.
- Recuperar información relevante desde documentos PDF.
- Responder consultas específicas utilizando contexto documental.
- Resumir documentos legales.
- Buscar cláusulas específicas.
- Mantener historial de interacción durante la ejecución.

---

## 🛠️ Tecnologías Utilizadas

- Python 3.12
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Sentence Transformers
- PyPDF
- GitHub

---

## 🏗️ Arquitectura General

```text
Usuario
    │
    ▼
LexiGuard Agent
    │
    ▼
Planificación y Toma de Decisiones
    │
    ├── buscar_en_contrato()
    ├── resumir_contrato()
    └── buscar_clausula()
    │
    ▼
ChromaDB
    │
    ▼
Contrato PDF
    │
    ▼
Respuesta al Usuario
```

---

## ⚙️ Componentes del Sistema

### 1. Ingesta de Documentos

El módulo `ingestion.py` realiza:

- Lectura del contrato PDF.
- División del documento en fragmentos (chunks).
- Generación de embeddings.
- Almacenamiento de vectores en ChromaDB.

### 2. Base de Datos Vectorial

Se utiliza ChromaDB para almacenar representaciones vectoriales del contrato y permitir búsquedas semánticas eficientes.

### 3. Herramientas del Agente

#### buscar_en_contrato()

Permite recuperar información específica relacionada con una consulta del usuario.

#### resumir_contrato()

Obtiene información relevante del contrato para generar un resumen ejecutivo.

#### buscar_clausula()

Permite localizar cláusulas específicas dentro del documento.

---

## 🧠 Memoria y Recuperación de Contexto

### Memoria de Corto Plazo

El sistema mantiene un historial de interacciones durante la ejecución para conservar el contexto conversacional.

### Memoria de Largo Plazo

La información contractual se almacena en ChromaDB mediante embeddings semánticos, permitiendo recuperación contextual basada en similitud.

---

## 🤖 Planificación y Toma de Decisiones

El agente analiza la intención de cada consulta y selecciona automáticamente la herramienta más adecuada.

### Ejemplos

**Consulta:**

```text
Genera un resumen del contrato
```

**Acción seleccionada:**

```text
resumir_contrato()
```

**Consulta:**

```text
Busca la cláusula de indemnización
```

**Acción seleccionada:**

```text
buscar_clausula()
```

**Consulta:**

```text
¿Cuáles son las obligaciones del trabajador?
```

**Acción seleccionada:**

```text
buscar_en_contrato()
```

Esta lógica permite adaptar el comportamiento del agente según las necesidades del usuario.

---

## 🚀 Instalación

### Clonar repositorio

```bash
git clone https://github.com/mvrtinnbz/evaluacion-ia-lexiguard.git
cd evaluacion-ia-lexiguard
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecución

### Procesar documento PDF

```bash
python src/ingestion.py
```

### Ejecutar pruebas

```bash
python tests.py
```

---

## 📂 Estructura del Proyecto

```text
evaluacion-ia-lexiguard/
│
├── chroma_db/
│
├── data/
│   └── contrato_fedex.pdf
│
├── src/
│   ├── agent.py
│   ├── ingestion.py
│   └── tools.py
│
├── tests.py
├── requirements.txt
└── README.md
```

---

## ✅ Funcionalidades Implementadas

- Recuperación semántica mediante ChromaDB.
- Uso de múltiples herramientas especializadas.
- Procesamiento de documentos PDF.
- Planificación basada en intención.
- Memoria conversacional.
- Recuperación contextual mediante embeddings.
- Búsqueda de cláusulas específicas.
- Generación de resúmenes documentales.

---

## 🔧 Desafíos Encontrados

Durante el desarrollo se presentaron dificultades relacionadas con la compatibilidad entre distintas versiones de LangChain, LangGraph y modelos de lenguaje externos.

Para garantizar estabilidad y reproducibilidad durante la evaluación, se optó por una arquitectura completamente local basada en:

- ChromaDB
- HuggingFace Embeddings
- Sentence Transformers
- Herramientas implementadas mediante LangChain

Esta solución permitió mantener las funcionalidades principales del agente sin depender de servicios externos.

---

## 🎓 Contexto Académico

Proyecto desarrollado para la asignatura **Ingeniería de Soluciones con Inteligencia Artificial (ISY0101)**.

El trabajo aplica conceptos fundamentales de:

- Agentes Inteligentes
- Retrieval Augmented Generation (RAG)
- Bases de Datos Vectoriales
- Memoria Conversacional
- Recuperación de Contexto
- Planificación
- Toma de Decisiones
- Procesamiento Inteligente de Documentos

---
