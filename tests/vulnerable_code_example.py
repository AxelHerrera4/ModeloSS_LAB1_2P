# vulnerable_code_example.py
# Ejemplo de código vulnerable para pruebas ML

def ejecutar_codigo(codigo):
    # Vulnerabilidad: uso de eval
    return eval(codigo)

def consulta_sql(user_input):
    # Vulnerabilidad: concatenación directa en consulta SQL
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    return query

def xss_vulnerable(user_input):
    # Vulnerabilidad: simulación de XSS en Python (solo para test)
    html = f"<div>{user_input}</div>"
    return html

# Pruebas
if __name__ == "__main__":
    print(ejecutar_codigo('2+2'))
    print(consulta_sql("admin' OR '1'='1"))
    print(xss_vulnerable('<img src=x onerror=alert(1)>'))
