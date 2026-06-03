from src.agent import crear_agente

agente = crear_agente()

print("\n=== PRUEBA 1 ===")

resultado = agente.invoke(
    "¿Cuáles son las responsabilidades de FedEx?"
)

print(resultado["accion"])
print(resultado["respuesta"])


print("\n=== PRUEBA 2 ===")

resultado = agente.invoke(
    "Genera un resumen del contrato"
)

print(resultado["accion"])
print(resultado["respuesta"])


print("\n=== PRUEBA 3 ===")

resultado = agente.invoke(
    "Busca la cláusula relacionada con indemnización"
)

print(resultado["accion"])
print(resultado["respuesta"])