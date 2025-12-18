"""
Ejemplo de código seguro.
Este archivo ha sido limpiado de patrones de vulnerabilidades.
"""

import os
import subprocess
from pathlib import Path
import json
from cryptography.fernet import Fernet


def safe_eval_function(user_input):
    # No usar eval, solo operaciones seguras
    try:
        result = int(user_input) + 2
    except Exception:
        result = None
    return result


def safe_query(cursor, username):
    # Usar parámetros en la consulta
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))


def safe_subprocess(filename):
    # No usar shell=True
    result = subprocess.run(["cat", filename], capture_output=True)
    return result.stdout


def no_hardcoded_secrets():
    # No hay secretos hardcodeados
    api_key = os.environ.get("API_KEY")
    password = os.environ.get("PASSWORD")
    return api_key, password


def safe_deserialization(data):
    # Usar json en vez de pickle
    obj = json.loads(data)
    return obj


def strong_crypto():
    # Usar algoritmo seguro
    key = Fernet.generate_key()
    cipher = Fernet(key)
    return cipher


def safe_path(user_file, base_dir):
    # Validar path y prevenir traversal
    base_path = Path(base_dir).resolve()
    requested_path = (base_path / user_file).resolve()
    if not str(requested_path).startswith(str(base_path)):
        raise ValueError("Path traversal detectado")
    return requested_path


def safe_os_system(command):
    # No usar os.system
    return f"Comando recibido: {command}"


class SafeClass:
    def __init__(self):
        # No almacenar secretos hardcodeados
        self.secret_token = None

    def execute_code(self, code):
        # No usar exec
        return f"Código recibido: {code}"
