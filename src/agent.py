from src.tools import (
    buscar_en_contrato,
    resumir_contrato,
    buscar_clausula
)

HISTORIAL = []


class LexiGuardAgent:

    def invoke(self, pregunta):

        pregunta_lower = pregunta.lower()

        HISTORIAL.append(
            ("usuario", pregunta)
        )

        # PLANIFICACIÓN Y DECISIÓN

        if "resumen" in pregunta_lower:

            accion = "resumir"

            respuesta = resumir_contrato.invoke({})

        elif "cláusula" in pregunta_lower:

            accion = "buscar_clausula"

            respuesta = buscar_clausula.invoke(
                {"clausula": pregunta}
            )

        else:

            accion = "buscar_contrato"

            respuesta = buscar_en_contrato.invoke(
                {"consulta": pregunta}
            )

        HISTORIAL.append(
            ("agente", respuesta)
        )

        return {
            "accion": accion,
            "respuesta": respuesta
        }


def crear_agente():
    return LexiGuardAgent()