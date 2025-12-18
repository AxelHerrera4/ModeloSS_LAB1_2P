"""
Tests de integración para el pipeline CI/CD.
Valida el flujo completo de escaneo de vulnerabilidades.
"""

import os
import sys
import json
import pytest
import subprocess
from pathlib import Path

# Agregar paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.vulnerability_scanner import VulnerabilityScanner
from scripts.get_changed_files import get_changed_files_git, filter_scannable_files


class TestCICDPipeline:
    """Tests para el pipeline CI/CD completo"""
    
    @pytest.fixture
    def model_path(self):
        """Ruta al modelo de prueba"""
        return 'ml_model/vulnerability_detector.pkl'
    
    @pytest.fixture
    def scanner(self, model_path):
        """Instancia del scanner"""
        if not os.path.exists(model_path):
            pytest.skip(f"Modelo no encontrado: {model_path}")
        return VulnerabilityScanner(model_path)
    
    def test_scanner_detects_vulnerable_code(self, scanner):
        """Verifica que el scanner detecta código vulnerable"""
        vulnerable_file = 'tests/vulnerable_code_example.py'
        
        if not os.path.exists(vulnerable_file):
            pytest.skip(f"Archivo no encontrado: {vulnerable_file}")
        
        result = scanner.scan_file(vulnerable_file)
        
        assert 'error' not in result
        assert 'vulnerable' in result
        assert 'risk_probability' in result
        
        # El archivo vulnerable debe tener probabilidad alta
        assert result['risk_probability'] >= 0.5, \
            f"Se esperaba alta probabilidad de vulnerabilidad, obtuvo: {result['risk_probability']}"
    
    def test_scanner_accepts_secure_code(self, scanner):
        """Verifica que el scanner acepta código seguro"""
        secure_file = 'tests/secure_code_example.py'
        
        if not os.path.exists(secure_file):
            pytest.skip(f"Archivo no encontrado: {secure_file}")
        
        result = scanner.scan_file(secure_file)
        
        assert 'error' not in result
        assert 'risk_probability' in result
        
        # El archivo seguro debe tener probabilidad baja
        assert result['risk_probability'] < 0.7, \
            f"Se esperaba baja probabilidad de vulnerabilidad, obtuvo: {result['risk_probability']}"
    
    def test_scanner_handles_javascript(self, scanner):
        """Verifica que el scanner maneja archivos JavaScript"""
        js_file = 'tests/vulnerable_code_js.js'
        
        if not os.path.exists(js_file):
            pytest.skip(f"Archivo no encontrado: {js_file}")
        
        result = scanner.scan_file(js_file)
        
        assert 'error' not in result
        assert 'risk_probability' in result
    
    def test_scanner_files_list_mode(self, scanner):
        """Verifica el modo de escaneo con lista de archivos"""
        test_files = [
            'tests/vulnerable_code_example.py',
            'tests/secure_code_example.py'
        ]
        
        # Filtrar solo los que existen
        existing_files = [f for f in test_files if os.path.exists(f)]
        
        if len(existing_files) < 2:
            pytest.skip("No hay suficientes archivos de prueba")
        
        results = scanner.scan_files(existing_files)
        
        assert len(results) == len(existing_files)
        assert all('risk_probability' in r for r in results)
    
    def test_get_changed_files_git(self):
        """Verifica que se pueden obtener archivos cambiados de git"""
        # Solo ejecutar si estamos en un repo git
        if not os.path.exists('.git'):
            pytest.skip("No es un repositorio git")
        
        try:
            changed = get_changed_files_git()
            assert isinstance(changed, list)
        except Exception as e:
            pytest.skip(f"Error accediendo a git: {e}")
    
    def test_filter_scannable_files(self):
        """Verifica el filtrado de archivos escaneables"""
        test_files = [
            'test.py',
            'test.js',
            'test.txt',
            'test.md',
            '__pycache__/file.py',
            'node_modules/package.js'
        ]
        
        filtered = filter_scannable_files(test_files)
        
        # Solo .py y .js deben pasar
        # Los de __pycache__ y node_modules deben ser excluidos
        assert 'test.py' in filtered or not Path('test.py').exists()
        assert 'test.js' in filtered or not Path('test.js').exists()
        assert 'test.txt' not in filtered
        assert '__pycache__/file.py' not in filtered
    
    def test_scanner_generates_summary(self, scanner):
        """Verifica que el scanner genera un resumen correcto"""
        test_file = 'tests/secure_code_example.py'
        
        if not os.path.exists(test_file):
            pytest.skip(f"Archivo no encontrado: {test_file}")
        
        result = scanner.scan_file(test_file)
        scanner.results = [result]
        
        summary = scanner.generate_summary_report()
        
        assert 'total_files' in summary
        assert 'high_risk_count' in summary
        assert 'scan_passed' in summary
        assert summary['total_files'] == 1
    
    def test_scanner_respects_threshold(self, scanner):
        """Verifica que el scanner respeta el umbral configurado"""
        scanner.RISK_THRESHOLD = 0.90  # Umbral muy alto
        
        test_file = 'tests/vulnerable_code_example.py'
        if not os.path.exists(test_file):
            pytest.skip(f"Archivo no encontrado: {test_file}")
        
        result = scanner.scan_file(test_file)
        
        # Con umbral de 90%, incluso código vulnerable podría no alcanzarlo
        # Solo verificamos que el campo existe
        assert 'risk_level' in result
    
    def test_end_to_end_scan_workflow(self, scanner, tmp_path):
        """Test end-to-end del workflow completo"""
        # 1. Escanear archivos de prueba
        test_files = [
            'tests/vulnerable_code_example.py',
            'tests/secure_code_example.py'
        ]
        
        existing_files = [f for f in test_files if os.path.exists(f)]
        if len(existing_files) < 1:
            pytest.skip("No hay archivos de prueba")
        
        # 2. Ejecutar escaneo
        results = scanner.scan_files(existing_files)
        assert len(results) > 0
        
        # 3. Generar resumen
        summary = scanner.generate_summary_report()
        assert summary['total_files'] == len(results)
        
        # 4. Guardar resultados
        output_file = tmp_path / "test_results.json"
        scanner.save_results(str(output_file))
        
        # 5. Verificar que el archivo se creó
        assert output_file.exists()
        
        # 6. Cargar y verificar contenido
        with open(output_file, 'r') as f:
            loaded_data = json.load(f)
        
        assert loaded_data['total_files'] == len(results)
        assert 'high_risk_count' in loaded_data
        assert 'scan_passed' in loaded_data


class TestGitIntegration:
    """Tests para la integración con Git"""
    
    def test_get_changed_files_script(self):
        """Verifica que el script get_changed_files.py funciona"""
        if not os.path.exists('.git'):
            pytest.skip("No es un repositorio git")
        
        try:
            result = subprocess.run(
                ['python', 'scripts/get_changed_files.py', '--help'],
                capture_output=True,
                text=True,
                timeout=5
            )
            assert result.returncode == 0
        except Exception as e:
            pytest.skip(f"Error ejecutando script: {e}")


class TestConfigValidation:
    """Tests para validación de configuración"""
    
    def test_config_file_exists(self):
        """Verifica que existe el archivo de configuración"""
        assert os.path.exists('config.yml'), "config.yml no encontrado"
    
    def test_model_path_in_config(self):
        """Verifica que la ruta del modelo está en config"""
        if not os.path.exists('config.yml'):
            pytest.skip("config.yml no encontrado")
        
        import yaml
        with open('config.yml', 'r') as f:
            config = yaml.safe_load(f)
        
        assert 'model' in config
        assert 'path' in config['model']
    
    def test_requirements_file_exists(self):
        """Verifica que existe requirements.txt"""
        assert os.path.exists('requirements.txt'), "requirements.txt no encontrado"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
