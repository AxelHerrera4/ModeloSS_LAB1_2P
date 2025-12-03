"""
Ejemplo de código vulnerable para demostración.
Este archivo contiene múltiples patrones de vulnerabilidades detectables.
"""

import os
import pickle
import subprocess


def dangerous_eval_function(user_input):
    """Función que usa eval() - PELIGROSO"""
    # VULNERABILIDAD: eval() permite ejecución de código arbitrario
    result = eval(user_input)
    return result


def sql_injection_example(username):
    """Ejemplo de SQL injection"""
    import sqlite3
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # VULNERABILIDAD: Concatenación de strings en query SQL
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    
    return cursor.fetchall()


def command_injection_example(filename):
    """Ejemplo de command injection"""
    # VULNERABILIDAD: subprocess con shell=True permite inyección de comandos
    subprocess.call(f"cat {filename}", shell=True)


def hardcoded_secrets():
    """Secretos hardcodeados"""
    # VULNERABILIDAD: Credenciales en el código
    api_key = "sk-1234567890abcdefghijklmnop"
    password = "SuperSecret123!"
    db_connection = "postgresql://admin:password123@localhost/mydb"
    
    return api_key, password


def unsafe_deserialization(data):
    """Deserialización insegura"""
    # VULNERABILIDAD: pickle.loads puede ejecutar código arbitrario
    obj = pickle.loads(data)
    return obj


def weak_crypto():
    """Uso de criptografía débil"""
    import hashlib
    
    # VULNERABILIDAD: MD5 es débil para criptografía
    password = "mypassword"
    hashed = hashlib.md5(password.encode()).hexdigest()
    
    return hashed


def path_traversal(user_file):
    """Riesgo de path traversal"""
    # VULNERABILIDAD: Path traversal sin validación
    file_path = "/uploads/" + user_file
    with open(file_path, 'r') as f:
        return f.read()


def bare_except_handler():
    """Manejo de excepciones inseguro"""
    try:
        risky_operation()
    except:  # VULNERABILIDAD: Bare except oculta errores
        pass


def os_system_usage(command):
    """Uso peligroso de os.system"""
    # VULNERABILIDAD: os.system es peligroso
    os.system(command)


class VulnerableClass:
    """Clase con múltiples problemas"""
    
    def __init__(self):
        # VULNERABILIDAD: Secreto hardcodeado
        self.secret_token = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"
    
    def execute_code(self, code):
        """Ejecución de código arbitrario"""
        # VULNERABILIDAD: exec() permite ejecución arbitraria
        exec(code)
    
    def format_string_vuln(self, template, data):
        """Format string vulnerability"""
        # VULNERABILIDAD: Format string sin validación
        return template % data


if __name__ == '__main__':
    # Código de prueba (también vulnerable)
    user_input = input("Ingresa comando: ")  # VULNERABILIDAD: Input sin validación
    dangerous_eval_function(user_input)
