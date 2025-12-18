# test_vulnerable.py
# Versión segura: evita SQL Injection y uso de eval

def buscar_usuario(nombre):
    # Solución: usar parámetros en la consulta
    query = "SELECT * FROM usuarios WHERE nombre = ?"
    print(query, nombre)
    # ...ejecutar query con parámetros...

def ejecutar_codigo(codigo):
    # Solución: no usar eval, solo operaciones seguras
    try:
        resultado = int(codigo) + 2  # Solo como ejemplo seguro
    except Exception:
        resultado = None
    print(resultado)

if __name__ == "__main__":
    buscar_usuario("admin' OR '1'='1")
    ejecutar_codigo("2")
