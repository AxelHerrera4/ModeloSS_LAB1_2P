"""
Ejemplo de código seguro para demostración.
Este archivo sigue las mejores prácticas de seguridad.
"""

import hashlib
import sqlite3
import subprocess
from typing import Any, Dict


def safe_input_validation(user_input: str) -> str:
    """Validación segura de entrada de usuario"""
    # Validación y sanitización
    if not isinstance(user_input, str):
        raise ValueError("Input debe ser string")
    
    # Limitar longitud
    if len(user_input) > 100:
        raise ValueError("Input demasiado largo")
    
    # Whitelist de caracteres permitidos
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ')
    if not all(c in allowed_chars for c in user_input):
        raise ValueError("Caracteres no permitidos")
    
    return user_input


def safe_sql_query(username: str) -> list:
    """Query SQL seguro usando parámetros"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # SEGURO: Uso de parámetros preparados
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    
    results = cursor.fetchall()
    conn.close()
    
    return results


def safe_subprocess_call(filename: str) -> str:
    """Ejecución segura de subproceso"""
    # SEGURO: Sin shell=True y con lista de argumentos
    result = subprocess.run(
        ['cat', filename],
        capture_output=True,
        text=True,
        timeout=5,
        check=True
    )
    
    return result.stdout


def secure_password_hashing(password: str) -> str:
    """Hash seguro de contraseñas"""
    import secrets
    
    # SEGURO: Usar algoritmo fuerte con salt
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt.encode(),
        100000
    )
    
    return f"{salt}:{hashed.hex()}"


def safe_file_access(filename: str, base_dir: str = '/uploads/') -> str:
    """Acceso seguro a archivos"""
    import os
    from pathlib import Path
    
    # SEGURO: Validar path y prevenir traversal
    base_path = Path(base_dir).resolve()
    requested_path = (base_path / filename).resolve()
    
    # Verificar que el archivo esté dentro del directorio permitido
    if not str(requested_path).startswith(str(base_path)):
        raise ValueError("Path traversal detectado")
    
    # Verificar que existe y es archivo
    if not requested_path.exists() or not requested_path.is_file():
        raise FileNotFoundError("Archivo no encontrado")
    
    with open(requested_path, 'r') as f:
        return f.read()


def proper_exception_handling():
    """Manejo correcto de excepciones"""
    try:
        risky_operation()
    except ValueError as e:
        # SEGURO: Capturar excepciones específicas
        print(f"Error de validación: {e}")
        raise
    except IOError as e:
        # SEGURO: Manejo específico
        print(f"Error de I/O: {e}")
        raise
    except Exception as e:
        # Log del error
        print(f"Error inesperado: {e}")
        raise


def load_config_safely() -> Dict[str, Any]:
    """Carga segura de configuración"""
    import os
    import json
    
    # SEGURO: Usar variables de entorno para secretos
    config = {
        'api_key': os.environ.get('API_KEY'),
        'database_url': os.environ.get('DATABASE_URL'),
        'debug': os.environ.get('DEBUG', 'false').lower() == 'true'
    }
    
    # Validar que las variables críticas existen
    if not config['api_key']:
        raise ValueError("API_KEY no configurada")
    
    return config


def secure_serialization(data: Dict) -> str:
    """Serialización segura de datos"""
    import json
    
    # SEGURO: Usar JSON en lugar de pickle para datos no confiables
    return json.dumps(data)


def secure_deserialization(data: str) -> Dict:
    """Deserialización segura"""
    import json
    
    # SEGURO: JSON es más seguro que pickle
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        print(f"Error de deserialización: {e}")
        return {}


class SecureClass:
    """Clase con buenas prácticas de seguridad"""
    
    def __init__(self):
        # SEGURO: No almacenar secretos, usar variables de entorno
        import os
        self._token = os.environ.get('AUTH_TOKEN')
    
    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Procesamiento seguro de datos"""
        # Validación de entrada
        if not isinstance(data, dict):
            raise TypeError("Se esperaba un diccionario")
        
        # Sanitización
        sanitized = {
            k: self._sanitize_value(v)
            for k, v in data.items()
            if self._is_valid_key(k)
        }
        
        return sanitized
    
    def _sanitize_value(self, value: Any) -> Any:
        """Sanitiza valores individuales"""
        if isinstance(value, str):
            # Remover caracteres peligrosos
            return value.replace('<', '').replace('>', '')
        return value
    
    def _is_valid_key(self, key: str) -> bool:
        """Valida claves permitidas"""
        allowed_keys = {'name', 'email', 'age', 'city'}
        return key in allowed_keys


def main():
    """Función principal segura"""
    try:
        # Cargar configuración de forma segura
        config = load_config_safely()
        
        # Procesar datos
        processor = SecureClass()
        
        # Las operaciones siguen las mejores prácticas
        print("Aplicación ejecutándose de forma segura")
        
    except Exception as e:
        # Log y manejo apropiado de errores
        print(f"Error en la aplicación: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
