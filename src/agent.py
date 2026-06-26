import json
import os
import time
from datetime import datetime
import psutil  # Métrica IE2: Monitoreo de Recursos de Hardware Local

from src.tools import (
    buscar_en_contrato,
    buscar_clausula,
    resumir_contrato,
    obtener_duracion_contrato,
    obtener_ultima_precision
)

LOG_FILE = "telemetry_logs.json"


def registrar_telemetria(modulo: str, datos: dict):
    """
    Registra la telemetría expandida del agente en un archivo JSON.
    """
    log = {
        "timestamp": datetime.now().isoformat(),
        "modulo": modulo,
        **datos
    }

    historial = []

    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as archivo:
                historial = json.load(archivo)
        except json.JSONDecodeError:
            historial = []

    historial.append(log)

    with open(LOG_FILE, "w", encoding="utf-8") as archivo:
        json.dump(
            historial,
            archivo,
            indent=4,
            ensure_ascii=False
        )


class LexiGuardAgent:
    """
    Agente principal de LexiGuard con soporte de memoria por sesión
    y telemetría avanzada para la rúbrica de la Evaluación Parcial 3.
    """

    def __init__(self):
        # Corrección del Profesor: Historial encapsulado por instancia y sesión
        self.sesiones_historial = {}

    def _obtener_historial(self, session_id: str):
        if session_id not in self.sesiones_historial:
            self.sesiones_historial[session_id] = []
        return self.sesiones_historial[session_id]

    def invoke(
        self,
        consulta,
        session_id="default_session"
    ):
        if isinstance(consulta, dict):
            consulta = (
                consulta.get("input")
                or consulta.get("consulta")
                or ""
            )

        # Captura de recursos de hardware pre-ejecución (IE2)
        proceso_actual = psutil.Process(os.getpid())
        ram_inicial = proceso_actual.memory_info().rss / (1024 * 1024)  # MB
        inicio_tiempo = time.time()

        historial = self._obtener_historial(session_id)

        historial.append({
            "rol": "usuario",
            "mensaje": consulta,
            "hora": datetime.now().strftime("%H:%M:%S")
        })

        herramienta = "buscar_en_contrato"
        respuesta = ""
        estado = "SUCCESS"
        error = ""
        tipo_error = ""

        try:
            consulta_min = consulta.lower()

            # Enrutamiento determinista local
            if any(
                p in consulta_min
                for p in ["resumen", "resumir", "resume", "síntesis", "sintesis", "explica"]
            ):
                herramienta = "resumir_contrato"
                respuesta = resumir_contrato.invoke({})

            elif any(
                p in consulta_min
                for p in ["vigencia", "duración", "duracion", "plazo", "término", "fecha", "inicio", "fin"]
            ):
                herramienta = "obtener_duracion_contrato"
                respuesta = obtener_duracion_contrato.invoke({})

            elif any(
                p in consulta_min
                for p in ["cláusula", "clausula", "confidencialidad", "multa", "rescisión", "obligación"]
            ):
                herramienta = "buscar_clausula"
                respuesta = buscar_clausula.invoke({"clausula": consulta})

            else:
                herramienta = "buscar_en_contrato"
                respuesta = buscar_en_contrato.invoke({"consulta": consulta})

        except Exception as ex:
            estado = "ERROR"
            error = str(ex)
            tipo_error = type(ex).__name__
            respuesta = (
                "Error durante la ejecución del agente.\n\n"
                f"{error}"
            )

        historial.append({
            "rol": "agente",
            "mensaje": respuesta,
            "hora": datetime.now().strftime("%H:%M:%S")
        })

        # Captura de métricas post-ejecución
        latencia = round(time.time() - inicio_tiempo, 4)
        ram_final = proceso_actual.memory_info().rss / (1024 * 1024)
        cpu_uso = psutil.cpu_percent(interval=None)

        # Recuperar score numérico de precisión semántica calculado en tools.py (IE1)
        precision_rag = obtener_ultima_precision() if estado == "SUCCESS" else 0.0

        # Métrica de Consistencia Operacional (IE1): Estabilidad del flujo
        consistencia_operacional = 1.0 if estado == "SUCCESS" else 0.0

        preview = (
            respuesta[:200] + "..."
            if len(respuesta) > 200
            else respuesta
        )

        # Inyección de las nuevas métricas solicitadas por la rúbrica de la EP3
        registrar_telemetria(
            "LexiGuardAgent",
            {
                "session_id": session_id,
                "consulta": consulta,
                "consulta_longitud": len(consulta),
                "herramienta": herramienta,
                "latencia_segundos": latencia,
                "estado": estado,
                "tipo_error": tipo_error,
                "error_mensaje": error,
                "respuesta_longitud": len(respuesta),
                "tokens_aproximados": len(respuesta.split()),
                "respuesta_preview": preview,
                # NUEVAS MÉTRICAS EXIGIDAS EN EP3 (IE1 e IE2)
                "precision_score": precision_rag,
                "consistencia_score": consistencia_operacional,
                "ram_uso_mb": round(ram_final, 2),
                "cpu_porcentaje": round(cpu_uso, 2)
            }
        )

        return {
            "output": respuesta,
            "respuesta": respuesta,
            "herramienta_utilizada": herramienta,
            "accion": herramienta,
            "latencia": latencia,
            "precision": precision_rag,
            "ram_mb": round(ram_final, 2)
        }


def crear_agente():
    """Función de compatibilidad de factoría."""
    return LexiGuardAgent()