from src.tools import (
    buscar_en_contrato,
    resumir_contrato,
    buscar_clausula,
    obtener_duracion_contrato
)

PROMPT_SISTEMA = """
Eres LexiGuard Agent, un asistente legal inteligente.

Tu función es analizar contratos laborales,
buscar cláusulas específicas, generar resúmenes
y responder consultas utilizando la información
contenida en los documentos.
"""

HISTORIAL = []


class LexiGuardAgent:

    def invoke(self, pregunta):

        pregunta_lower = pregunta.lower()

        HISTORIAL.append(
            ("usuario", pregunta)
        )

        # RESUMEN

        if (
            "resumen" in pregunta_lower
            or "resumir" in pregunta_lower
        ):

            accion = "resumir_contrato"

            respuesta = resumir_contrato.invoke({})

        # DURACIÓN

        elif (
            "duración" in pregunta_lower
            or "duracion" in pregunta_lower
            or "inicio" in pregunta_lower
            or "término" in pregunta_lower
            or "termino" in pregunta_lower
            or "vigencia" in pregunta_lower
        ):

            accion = "obtener_duracion_contrato"

            respuesta = obtener_duracion_contrato.invoke({})

        # CLÁUSULAS

        elif (
            "cláusula" in pregunta_lower
            or "clausula" in pregunta_lower
        ):

            accion = "buscar_clausula"

            respuesta = buscar_clausula.invoke(
                {"clausula": pregunta}
            )

        # CONSULTA GENERAL

        else:

            accion = "buscar_en_contrato"

            respuesta = buscar_en_contrato.invoke(
                {"consulta": pregunta}
            )

        HISTORIAL.append(
            ("agente", respuesta)
        )

        return {
            "accion": accion,
            "respuesta": respuesta,
            "historial": HISTORIAL
        }


def crear_agente():
    return LexiGuardAgent()