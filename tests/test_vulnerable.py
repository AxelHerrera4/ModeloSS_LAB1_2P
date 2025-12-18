# test_vulnerable.py
# Ejemplo vulnerable: SQL Injection y uso de eval

def buscar_usuario(nombre):
    # Vulnerabilidad: concatenación directa en query (SQL Injection)
    query = "SELECT * FROM usuarios WHERE nombre = '" + nombre + "'"
    print(query)
    # ...ejecutar query...

def ejecutar_codigo(codigo):
    # Vulnerabilidad: uso de eval
    resultado = eval(codigo)
    print(resultado)

if __name__ == "__main__":
    buscar_usuario("admin' OR '1'='1")
    ejecutar_codigo("2 + 2")
