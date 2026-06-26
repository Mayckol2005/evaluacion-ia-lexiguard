import json
import os
import pandas as pd
import streamlit as st
from src.agent import LexiGuardAgent

st.set_page_config(
    page_title="LexiGuard - Panel de Observabilidad",
    page_icon="⚖️",
    layout="wide"
)

LOG_FILE = "telemetry_logs.json"

if "agente_legal" not in st.session_state:
    st.session_state.agente_legal = LexiGuardAgent()

if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = []


def traducir_herramienta(nombre):
    traducciones = {
        "buscar_en_contrato": "🔎 Búsqueda General",
        "buscar_clausula": "📑 Búsqueda de Cláusulas",
        "resumir_contrato": "📝 Resumen Ejecutivo",
        "obtener_duracion_contrato": "📅 Vigencia del Contrato"
    }
    return traducciones.get(nombre, nombre)


def cargar_logs():
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        return pd.DataFrame()

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        df = pd.DataFrame(datos)
        if df.empty:
            return df

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["latencia_segundos"] = df["latencia_segundos"].astype(float)
        df["herramienta_legible"] = df["herramienta"].apply(traducir_herramienta)

        # Conversión segura para las nuevas columnas de la Entrega 3
        for col in ["precision_score", "consistencia_score", "ram_uso_mb", "cpu_porcentaje"]:
            if col in df.columns:
                df[col] = df[col].astype(float)
            else:
                df[col] = 0.0

        return df
    except Exception as e:
        st.error(f"No fue posible cargar telemetry_logs.json\n\n{e}")
        return pd.DataFrame()


df = cargar_logs()

st.title("⚖️ LexiGuard")
st.caption("Dashboard de Observabilidad Centralizado • Arquitectura RAG Local")

st.markdown(
    "Este panel permite monitorear en tiempo real el comportamiento del "
    "agente LexiGuard, visualizar métricas operacionales avanzadas y consultar "
    "el contrato cargado mediante recuperación semántica."
)

if not df.empty:
    st.markdown("---")
    st.subheader("📊 Métricas Generales Operacionales")

    total_consultas = len(df)
    latencia_promedio = df["latencia_segundos"].mean()
    tiempo_total = df["latencia_segundos"].sum()
    tasa_exito = (len(df[df["estado"] == "SUCCESS"]) / total_consultas) * 100
    sesiones = df["session_id"].nunique()
    herramienta_top = df["herramienta_legible"].mode()[0] if not df["herramienta_legible"].empty else "N/A"

    # Fila 1 de KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Consultas", total_consultas)
    k2.metric("Latencia Promedio", f"{latencia_promedio:.3f} s")
    k3.metric("Tiempo Total CPU", f"{tiempo_total:.2f} s")
    k4.metric("Tasa de Éxito", f"{tasa_exito:.1f}%")

    # Fila 2 de KPIs: Requisitos Rúbrica EP3 (IE1, IE2)
    st.markdown("#### 🛡️ Indicadores Clave de Calidad y Recursos (Rúbrica Entrega 3)")
    k5, k6, k7, k8 = st.columns(4)
    
    prec_prom = df["precision_score"].mean() * 100 if "precision_score" in df.columns else 0.0
    cons_prom = df["consistencia_score"].mean() * 100 if "consistencia_score" in df.columns else 0.0
    ram_prom = df["ram_uso_mb"].mean() if "ram_uso_mb" in df.columns else 0.0
    cpu_prom = df["cpu_porcentaje"].mean() if "cpu_porcentaje" in df.columns else 0.0

    k5.metric("Precisión RAG Promedio", f"{prec_prom:.1f}%")
    k6.metric("Consistencia del Sistema", f"{cons_prom:.1f}%")
    k7.metric("Uso RAM Promedio", f"{ram_prom:.1f} MB")
    k8.metric("Carga CPU Promedio", f"{cpu_prom:.1f}%")

    # Sección de filtros
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        filtro_herramienta = st.selectbox("Filtrar por Herramienta", ["Todas"] + sorted(df["herramienta_legible"].unique().tolist()))
    with c2:
        filtro_estado = st.selectbox("Filtrar por Estado de Ejecución", ["Todos", "SUCCESS", "ERROR"])

    df_filtrado = df.copy()
    if filtro_herramienta != "Todas":
        df_filtrado = df_filtrado[df_filtrado["herramienta_legible"] == filtro_herramienta]
    if filtro_estado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["estado"] == filtro_estado]

    # Gráficos de telemetría originales
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Latencia por Consulta Temporal")
        st.line_chart(data=df_filtrado.sort_values("timestamp"), x="timestamp", y="latencia_segundos", use_container_width=True)
    with col2:
        st.subheader("🧰 Frecuencia de Uso de Herramientas")
        st.bar_chart(df_filtrado["herramienta_legible"].value_counts(), use_container_width=True)

    # NUEVA SECCIÓN DE GRÁFICOS EXIGIDA POR LA RÚBRICA (IE1, IE2, Evidencia Visual IE8)
    st.markdown("---")
    st.subheader("🎯 Análisis de Trazabilidad y Capacidad Local (IE1 & IE2)")
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("🎯 Evolución de la Precisión de Contexto (Similitud Vectorial)")
        st.line_chart(data=df_filtrado.sort_values("timestamp"), x="timestamp", y="precision_score", use_container_width=True)
    with col4:
        st.subheader("💾 Huella de Memoria RAM del Proceso Local (MB)")
        st.area_chart(data=df_filtrado.sort_values("timestamp"), x="timestamp", y="ram_uso_mb", use_container_width=True)

    # Tabla histórica de logs
    st.markdown("---")
    st.subheader("📋 Registro Histórico de Eventos")
    columnas_mostrar = ["timestamp", "consulta", "herramienta_legible", "estado", "latencia_segundos", "precision_score", "ram_uso_mb"]
    disponibles = [c for c in columnas_mostrar if c in df_filtrado.columns]
    
    tabla_renombrada = df_filtrado[disponibles].sort_values(by="timestamp", ascending=False).rename(
        columns={
            "timestamp": "Fecha/Hora", "consulta": "Consulta Usuario", "herramienta_legible": "Herramienta",
            "estado": "Estado", "latencia_segundos": "Latencia (s)", "precision_score": "Precisión RAG", "ram_uso_mb": "RAM (MB)"
        }
    )
    st.dataframe(tabla_renombrada, hide_index=True, use_container_width=True)

    # Panel de errores (IE3)
    errores_df = df_filtrado[df_filtrado["estado"] == "ERROR"]
    if not errores_df.empty:
        st.markdown("---")
        st.subheader("🚨 Diagnóstico de Cuellos de Botella y Errores (IE3)")
        st.dataframe(errores_df[["timestamp", "consulta", "tipo_error", "error_mensaje"]], hide_index=True, use_container_width=True)

# Sección Interactiva de Chat RAG
st.markdown("---")
st.subheader("💬 Chat Interactivo con LexiGuard")
st.caption("Cada interacción generará datos dinámicos en los gráficos superiores de manera inmediata.")

for autor, mensaje in st.session_state.historial_chat:
    with st.chat_message(autor):
        st.write(mensaje)

pregunta = st.chat_input("Escribe tu consulta sobre las cláusulas del contrato aquí...")

if pregunta:
    with st.chat_message("user"):
        st.write(pregunta)
    st.session_state.historial_chat.append(("user", pregunta))

    with st.spinner("Realizando consulta semántica en la base de datos local ChromaDB..."):
        resultado = st.session_state.agente_legal.invoke(consulta=pregunta, session_id="streamlit")

    respuesta = resultado["respuesta"]
    with st.chat_message("assistant"):
        st.write(respuesta)
        st.caption(
            f"**Métricas de esta ejecución:** Herramienta: {traducir_herramienta(resultado['herramienta_utilizada'])} | "
            f"Latencia: {resultado['latencia']:.3f} s | Precisión: {resultado['precision']*100:.1f}% | RAM: {resultado['ram_mb']} MB"
        )
    st.session_state.historial_chat.append(("assistant", respuesta))
    st.rerun()

st.markdown("---")
st.caption("LexiGuard • Duoc UC • Escuela de Informática y Telecomunicaciones • Ingeniería de Soluciones con IA 2026")