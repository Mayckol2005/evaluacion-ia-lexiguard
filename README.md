# ⚖️ LexiGuard
## Sistema de Observabilidad, Trazabilidad y Agente RAG Local

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-purple)
![License](https://img.shields.io/badge/License-Academic-lightgrey)

Asignatura **Ingeniería de Soluciones con Inteligencia Artificial**

**Institución:** Duoc UC

**Docente:** Héctor Morel

---

# 👥 Integrantes

- Mayckol Mardones
- Martin Baza

---

# 📚 Descripción

LexiGuard es una solución empresarial basada en Inteligencia Artificial diseñada para apoyar el análisis de contratos laborales y documentos legales mediante técnicas de **Retrieval Augmented Generation (RAG)**.

El sistema incorpora:

- Búsqueda semántica sobre documentos PDF
- Base de datos vectorial local
- Observabilidad en tiempo real
- Trazabilidad completa de consultas
- Arquitectura completamente local
- Protección de datos sensibles

A diferencia de soluciones tradicionales con respuestas hardcodeadas, LexiGuard genera respuestas dinámicamente utilizando únicamente el contenido presente en los documentos cargados.

---

# 🎯 Objetivos

El proyecto busca desarrollar un agente inteligente capaz de:

- Analizar contratos dinámicamente
- Implementar observabilidad (IL3.1)
- Implementar trazabilidad (IL3.2)
- Garantizar un uso responsable de IA (IL3.3)
- Evaluar la escalabilidad (IL3.4)

---

# 🛠 Tecnologías

| Tecnología | Uso |
|------------|------|
| Python 3.12 | Lenguaje principal |
| Streamlit | Dashboard |
| LangChain | Framework RAG |
| ChromaDB | Base vectorial |
| HuggingFace Embeddings | Embeddings locales |
| Sentence Transformers | Modelo semántico |
| PyPDFLoader | Lectura de PDF |

---

# 🏗 Arquitectura

```
Usuario
   │
   ▼
Dashboard (Streamlit)
   │
   ▼
Agent (LangChain)
   │
   ├──────── buscar_en_contrato()
   ├──────── buscar_clausula()
   └──────── resumir_contrato()
             │
             ▼
        ChromaDB
             │
             ▼
         Documentos PDF
             │
             ▼
 telemetry_logs.json
```

---

# ⚙ Componentes

## Ingesta dinámica

El sistema:

- Detecta automáticamente todos los PDF dentro de `data/`
- Divide los documentos en chunks
- Genera embeddings
- Guarda la información en ChromaDB

No existen nombres de archivos fijos.

---

## Herramientas del agente

### buscar_en_contrato()

Realiza búsquedas semánticas sobre el contrato.

### buscar_clausula()

Encuentra cláusulas específicas.

### resumir_contrato()

Genera un resumen ejecutivo del documento.

---

## Telemetría

Cada interacción queda registrada en:

```
telemetry_logs.json
```

Ejemplo:

```json
{
  "timestamp": "2026-06-26T17:15:32",
  "session_id": "st-session-df89c2",
  "user_query": "¿Cuál es el sueldo?",
  "retrieved_chunks_count": 4,
  "execution_time_ms": 1820,
  "status": "SUCCESS"
}
```

---

# 🧠 Uso Responsable (IL3.3)

## Memoria

- Historial conversacional temporal
- Memoria vectorial persistente mediante ChromaDB

## Mitigación de Alucinaciones

El agente solamente responde utilizando información recuperada desde el documento.

Si la información no existe, responde que no puede encontrarla.

---

# 🤖 Flujo del Agente

Pregunta del usuario

↓

Identificación de intención

↓

Selección automática de herramienta

↓

Recuperación de contexto

↓

Generación de respuesta

---

# 🚀 Instalación

## Clonar repositorio

```bash
git clone https://github.com/Mayckol2005/evaluacion-ia-lexiguard.git

cd evaluacion-ia-lexiguard
```

---

## Crear entorno virtual

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```
---

## Instalar dependencias

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

---

# ▶ Ejecución

## 1. Eliminar la base vectorial

Eliminar completamente la carpeta

```
chroma_db/
```

---

## 2. Copiar el contrato

Guardar únicamente el contrato que será analizado dentro de

```
data/
```

---

## 3. Ejecutar la ingesta

```bash
python src/ingestion.py
```

Salida esperada

```
📂 Archivos detectados:

contrato_ficticio_chile.pdf

✅ Base vectorial actualizada correctamente.
```

---

## 4. Ejecutar Streamlit

```bash
streamlit run dashboard.py
```

Abrir

```
http://localhost:8501
```

---

# 🧪 Casos de prueba

## Jornada laboral

```
¿Cuál es la jornada laboral de Alejandro?
```

Debe responder:

- 40 horas semanales
- lunes a viernes
- 09:00 a 17:00
- 45 minutos de colación

---

## Remuneración

```
¿Cuál es la remuneración?
```

Debe recuperar:

- $2.800.000
- Colación $90.000
- Movilización $70.000

---

## Telemetría

Verificar:

- Precisión de contexto
- Latencia
- Consumo RAM
- telemetry_logs.json

---

# 📁 Estructura del proyecto

```
evaluacion-ia-lexiguard/

│

├── chroma_db/

├── data/

│ └── contrato_ficticio_chile.pdf

├── src/

│ ├── agent.py

│ ├── ingestion.py

│ └── tools.py

├── dashboard.py

├── telemetry_logs.json

├── tests.py

├── requirements.txt

└── README.md
```

---

# 🎓 Contexto Académico

Proyecto desarrollado para la asignatura:

**Ingeniería de Soluciones con Inteligencia Artificial**

Escuela de Informática y Telecomunicaciones

Duoc UC

---

# 📖 Conceptos aplicados

- Agentes Inteligentes
- Retrieval Augmented Generation (RAG)
- ChromaDB
- Embeddings
- LangChain
- Memoria Conversacional
- Observabilidad
- Trazabilidad
- IA Responsable