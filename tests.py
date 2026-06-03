import sys

sys.stdout.reconfigure(encoding="utf-8")
from src.agent import crear_agente

agente = crear_agente()

print("\n=== PRUEBA 1 ===")
print("Consulta sobre responsabilidades\n")

resultado = agente.invoke(
    "¿Cuáles son las responsabilidades de FedEx?"
)

print("Herramienta utilizada:")
print(resultado["accion"])

print("\nRespuesta:")
print(resultado["respuesta"])


print("\n\n=== PRUEBA 2 ===")
print("Generación de resumen\n")

resultado = agente.invoke(
    "Genera un resumen del contrato"
)

print("Herramienta utilizada:")
print(resultado["accion"])

print("\nRespuesta:")
print(resultado["respuesta"])


print("\n\n=== PRUEBA 3 ===")
print("Búsqueda de cláusula\n")

resultado = agente.invoke(
    "Busca la cláusula relacionada con indemnización"
)

print("Herramienta utilizada:")
print(resultado["accion"])

print("\nRespuesta:")
print(resultado["respuesta"])


print("\n\n=== PRUEBA 4 ===")
print("Consulta de duración\n")

resultado = agente.invoke(
    "¿Cuál es la duración del contrato?"
)

print("Herramienta utilizada:")
print(resultado["accion"])

print("\nRespuesta:")
print(resultado["respuesta"])