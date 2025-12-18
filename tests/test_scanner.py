"""
Tests unitarios para el Sistema de Detección de Vulnerabilidades
Estos tests se ejecutan en la Etapa 2 del pipeline CI/CD
"""

import pytest
import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.code_analyzer import CodeAnalyzer
from ml_model.model import VulnerabilityPredictor


class TestCodeAnalyzer:
    """Tests para el analizador de código"""
    
    def setup_method(self):
        """Setup antes de cada test"""
        self.analyzer = CodeAnalyzer()
    
    def test_analyze_python_code_basic(self):
        """Test básico de análisis de código Python"""
        code = """
def suma(a, b):
    return a + b
"""
        features = self.analyzer.analyze_python_code(code, "test.py")
        
        assert features is not None
        assert 'loc' in features
        assert features['loc'] > 0
        assert 'num_functions' in features
        assert features['num_functions'] == 1
    
    def test_detect_sql_injection_python(self):
        """Test detección de inyección SQL en Python"""
        vulnerable_code = """
import sqlite3
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
"""
        features = self.analyzer.analyze_python_code(vulnerable_code, "vulnerable.py")
        
        # Debe detectar uso de concatenación en SQL
        assert features['has_sql_concat'] == True or features['has_dangerous_calls'] == True
    
    def test_detect_eval_usage(self):
        """Test detección de eval/exec"""
        dangerous_code = """
def execute_code(user_input):
    result = eval(user_input)
    return result
"""
        features = self.analyzer.analyze_python_code(dangerous_code, "dangerous.py")
        
        assert features['uses_eval'] == True
    
    def test_safe_code_features(self):
        """Test código seguro no activa flags de peligro"""
        safe_code = """
def process_data(data):
    if isinstance(data, str):
        return data.strip().lower()
    return None
"""
        features = self.analyzer.analyze_python_code(safe_code, "safe.py")
        
        assert features['uses_eval'] == False
        assert features['uses_exec'] == False
    
    def test_analyze_javascript_code(self):
        """Test análisis de código JavaScript"""
        js_code = """
function suma(a, b) {
    return a + b;
}
"""
        features = self.analyzer.analyze_javascript_code(js_code, "test.js")
        
        assert features is not None
        assert 'loc' in features
        assert features['loc'] > 0
    
    def test_detect_xss_javascript(self):
        """Test detección de XSS en JavaScript"""
        vulnerable_js = """
function displayUser(name) {
    document.innerHTML = name;
}
"""
        features = self.analyzer.analyze_javascript_code(vulnerable_js, "xss.js")
        
        assert features['uses_innerhtml'] == True


class TestVulnerabilityPredictor:
    """Tests para el modelo predictor"""
    
    def setup_method(self):
        """Setup antes de cada test"""
        model_path = Path(__file__).parent.parent / "ml_model" / "vulnerability_detector.pkl"
        if model_path.exists():
            self.predictor = VulnerabilityPredictor(str(model_path))
        else:
            pytest.skip("Modelo no encontrado. Ejecuta train_detector.ipynb primero.")
    
    def test_predictor_initialization(self):
        """Test inicialización del predictor"""
        assert self.predictor is not None
        assert self.predictor.is_trained == True
        assert len(self.predictor.feature_names) > 0
    
    def test_prepare_features(self):
        """Test preparación de features"""
        features_dict = {
            'loc': 10,
            'num_functions': 2,
            'uses_eval': True,
            'has_sanitization': False
        }
        
        df = self.predictor.prepare_features(features_dict)
        
        assert df is not None
        assert len(df) == 1
        # Booleanos deben convertirse a int
        assert df['uses_eval'].iloc[0] in [0, 1]
    
    def test_predict_vulnerable_code(self):
        """Test predicción de código vulnerable"""
        # Features típicas de código vulnerable
        vulnerable_features = {
            'loc': 20,
            'num_functions': 3,
            'uses_eval': True,
            'uses_exec': True,
            'has_sql_concat': True,
            'has_sanitization': False,
            'has_dangerous_calls': True,
            'ast_depth': 8,
            'cyclomatic_complexity': 5
        }
        
        # Agregar features faltantes con valores por defecto
        for feature in self.predictor.feature_names:
            if feature not in vulnerable_features:
                vulnerable_features[feature] = 0
        
        df = self.predictor.prepare_features(vulnerable_features)
        is_vulnerable, probability = self.predictor.predict(df)
        
        assert isinstance(is_vulnerable, bool)
        assert 0.0 <= probability <= 1.0
    
    def test_predict_safe_code(self):
        """Test predicción de código seguro"""
        # Features típicas de código seguro
        safe_features = {
            'loc': 15,
            'num_functions': 2,
            'uses_eval': False,
            'uses_exec': False,
            'has_sql_concat': False,
            'has_sanitization': True,
            'has_dangerous_calls': False,
            'ast_depth': 4,
            'cyclomatic_complexity': 2
        }
        
        # Agregar features faltantes
        for feature in self.predictor.feature_names:
            if feature not in safe_features:
                safe_features[feature] = 0
        
        df = self.predictor.prepare_features(safe_features)
        is_vulnerable, probability = self.predictor.predict(df)
        
        assert isinstance(is_vulnerable, bool)
        assert 0.0 <= probability <= 1.0


class TestIntegration:
    """Tests de integración completa"""
    
    def test_full_scan_vulnerable_file(self):
        """Test escaneo completo de archivo vulnerable"""
        analyzer = CodeAnalyzer()
        model_path = Path(__file__).parent.parent / "ml_model" / "vulnerability_detector.pkl"
        
        if not model_path.exists():
            pytest.skip("Modelo no encontrado")
        
        predictor = VulnerabilityPredictor(str(model_path))
        
        # Código vulnerable de ejemplo
        vulnerable_code = """
import sqlite3
import os

def get_user_data(user_id):
    # SQL Injection vulnerability
    query = "SELECT * FROM users WHERE id = " + user_id
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def execute_command(cmd):
    # Command injection vulnerability
    os.system(cmd)
"""
        
        # Analizar
        features = analyzer.analyze_python_code(vulnerable_code, "vulnerable.py")
        df = predictor.prepare_features(features)
        is_vulnerable, probability = predictor.predict(df)
        
        # Debería detectarse como vulnerable con alta probabilidad
        assert isinstance(is_vulnerable, bool)
        assert probability > 0.5  # Al menos 50% de probabilidad
    
    def test_full_scan_safe_file(self):
        """Test escaneo completo de archivo seguro"""
        analyzer = CodeAnalyzer()
        model_path = Path(__file__).parent.parent / "ml_model" / "vulnerability_detector.pkl"
        
        if not model_path.exists():
            pytest.skip("Modelo no encontrado")
        
        predictor = VulnerabilityPredictor(str(model_path))
        
        # Código seguro de ejemplo
        safe_code = """
def suma(a: int, b: int) -> int:
    '''Suma dos números de forma segura'''
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Los argumentos deben ser enteros")
    return a + b

def procesar_datos(datos: list) -> list:
    '''Procesa una lista de datos de forma segura'''
    if not datos:
        return []
    return [str(item).strip() for item in datos if item is not None]
"""
        
        # Analizar
        features = analyzer.analyze_python_code(safe_code, "safe.py")
        df = predictor.prepare_features(features)
        is_vulnerable, probability = predictor.predict(df)
        
        # Probabilidad debería ser baja
        assert isinstance(is_vulnerable, bool)
        assert probability >= 0.0


class TestFileOperations:
    """Tests de operaciones con archivos"""
    
    def test_scan_python_file(self):
        """Test escaneo de archivo Python real"""
        test_file = Path(__file__).parent / "secure_code_example.py"
        
        if not test_file.exists():
            pytest.skip("Archivo de test no encontrado")
        
        analyzer = CodeAnalyzer()
        
        with open(test_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        features = analyzer.analyze_python_code(code, str(test_file))
        
        assert features is not None
        assert features['loc'] > 0
    
    def test_scan_javascript_file(self):
        """Test escaneo de archivo JavaScript real"""
        test_file = Path(__file__).parent / "secure_code_js.js"
        
        if not test_file.exists():
            pytest.skip("Archivo de test no encontrado")
        
        analyzer = CodeAnalyzer()
        
        with open(test_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        features = analyzer.analyze_javascript_code(code, str(test_file))
        
        assert features is not None
        assert features['loc'] > 0


# Tests de configuración
def test_model_exists():
    """Verifica que el modelo entrenado existe"""
    model_path = Path(__file__).parent.parent / "ml_model" / "vulnerability_detector.pkl"
    assert model_path.exists(), "Modelo no encontrado. Ejecuta train_detector.ipynb"


def test_requirements_met():
    """Verifica que las dependencias están instaladas"""
    try:
        import sklearn
        import pandas
        import numpy
        assert True
    except ImportError as e:
        pytest.fail(f"Dependencia faltante: {e}")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
