"""
API REST simple para el escáner de vulnerabilidades
Se puede ejecutar localmente o desplegar en Railway/Render/Fly.io
"""

from flask import Flask, jsonify, request
import os
import sys
from pathlib import Path

# Agregar paths
sys.path.insert(0, str(Path(__file__).parent))

from scripts.code_analyzer import CodeAnalyzer
from ml_model.model import VulnerabilityPredictor

app = Flask(__name__)

# Inicializar modelo
MODEL_PATH = os.getenv('MODEL_PATH', 'ml_model/vulnerability_detector.pkl')
predictor = None

if os.path.exists(MODEL_PATH):
    predictor = VulnerabilityPredictor(MODEL_PATH)
    print(f"✅ Modelo cargado: {MODEL_PATH}")
else:
    print(f"⚠️ Modelo no encontrado en {MODEL_PATH}")


@app.route('/')
def home():
    """Página principal"""
    return jsonify({
        'name': 'Vulnerability Scanner ML',
        'version': '1.0.0',
        'status': 'running',
        'model_loaded': predictor is not None,
        'endpoints': {
            '/': 'Info de la API',
            '/health': 'Health check',
            '/scan': 'POST - Escanear código',
            '/stats': 'Estadísticas del modelo'
        }
    })


@app.route('/health')
def health():
    """Health check para Railway/Render/Fly.io"""
    status = {
        'status': 'healthy',
        'model_loaded': predictor is not None
    }
    
    if predictor is None:
        status['status'] = 'unhealthy'
        status['error'] = 'Modelo no cargado'
        return jsonify(status), 503
    
    return jsonify(status), 200


@app.route('/scan', methods=['POST'])
def scan_code():
    """
    Escanea código enviado por POST
    
    Body JSON:
    {
        "code": "código fuente",
        "language": "python" o "javascript",
        "filename": "opcional"
    }
    """
    if predictor is None:
        return jsonify({'error': 'Modelo no disponible'}), 503
    
    data = request.get_json()
    
    if not data or 'code' not in data:
        return jsonify({'error': 'Falta campo "code"'}), 400
    
    code = data['code']
    language = data.get('language', 'python')
    filename = data.get('filename', f'code.{language}')
    
    try:
        # Analizar código
        analyzer = CodeAnalyzer()
        
        if language == 'python':
            features = analyzer.analyze_python_code(code, filename)
        elif language in ['javascript', 'js']:
            features = analyzer.analyze_javascript_code(code, filename)
        else:
            return jsonify({'error': f'Lenguaje no soportado: {language}'}), 400
        
        # Predecir vulnerabilidad
        df = predictor.prepare_features(features)
        is_vulnerable, probability = predictor.predict(df)
        vuln_type = predictor.get_vulnerability_type(features)
        
        # Respuesta
        result = {
            'filename': filename,
            'language': language,
            'is_vulnerable': bool(is_vulnerable),
            'vulnerability_probability': float(probability),
            'vulnerability_type': vuln_type,
            'risk_level': 'HIGH' if probability > 0.7 else 'MEDIUM' if probability > 0.4 else 'LOW',
            'features': {
                'lines_of_code': features.get('loc', 0),
                'functions': features.get('num_functions', 0),
                'uses_eval': features.get('uses_eval', False),
                'uses_exec': features.get('uses_exec', False),
                'has_sql_concat': features.get('has_sql_concat', False)
            }
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/stats')
def stats():
    """Estadísticas del modelo"""
    if predictor is None:
        return jsonify({'error': 'Modelo no disponible'}), 503
    
    return jsonify({
        'model_type': 'Random Forest Classifier',
        'features_count': len(predictor.feature_names),
        'threshold': 0.70,
        'supported_languages': ['python', 'javascript']
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Iniciando API en puerto {port}")
    print(f"🔍 Modelo: {'Cargado ✅' if predictor else 'No disponible ❌'}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
