"""
Generador de reportes HTML con explicabilidad usando SHAP.
Crea reportes visuales detallados sobre las predicciones del modelo.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Agregar paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def generate_html_report(scan_results_path: str, output_path: str = None):
    """
    Genera un reporte HTML completo
    
    Args:
        scan_results_path: Ruta al archivo JSON con resultados del escaneo
        output_path: Ruta para guardar el HTML. Si es None, usa el mismo directorio.
    """
    # Cargar resultados
    with open(scan_results_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Determinar output path
    if output_path is None:
        output_path = scan_results_path.replace('.json', '.html')
    
    # Generar HTML
    html_content = _generate_html_content(data)
    
    # Guardar
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Reporte HTML generado: {output_path}")
    return output_path


def _generate_html_content(data: Dict) -> str:
    """Genera el contenido HTML del reporte"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Estadísticas
    total_files = data.get('total_files', 0)
    high_risk = data.get('high_risk_count', 0)
    medium_risk = data.get('medium_risk_count', 0)
    low_risk = data.get('low_risk_count', 0)
    scan_passed = data.get('scan_passed', False)
    
    # Color del estado
    status_color = '#28a745' if scan_passed else '#dc3545'
    status_text = 'APROBADO' if scan_passed else 'RECHAZADO'
    
    # Generar tabla de archivos
    files_html = _generate_files_table(data.get('details', []))
    
    # Generar gráficos
    chart_script = _generate_chart_script(high_risk, medium_risk, low_risk)
    
    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe de Análisis de Vulnerabilidades</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', 'Arial', sans-serif;
            background: #f5f5f5;
            padding: 20px;
            color: #2c3e50;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header {{
            background: #1a237e;
            color: white;
            padding: 30px 40px;
            border-bottom: 4px solid #0d47a1;
        }}
        
        .header h1 {{
            font-size: 1.8em;
            font-weight: 600;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }}
        
        .header .subtitle {{
            font-size: 0.95em;
            opacity: 0.9;
            font-weight: 400;
        }}
        
        .status-banner {{
            background-color: {status_color};
            color: white;
            padding: 20px 40px;
            text-align: left;
            font-size: 1.1em;
            font-weight: 600;
            border-left: 5px solid rgba(0,0,0,0.2);
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }}
        
        .summary {{
            padding: 40px;
            background: #ffffff;
        }}
        
        .summary-title {{
            font-size: 1.3em;
            color: #1a237e;
            margin-bottom: 25px;
            font-weight: 600;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 10px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: #fafafa;
            padding: 20px;
            border: 1px solid #e0e0e0;
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: 600;
            margin: 10px 0;
        }}
        
        .stat-label {{
            color: #546e7a;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 500;
        }}
        
        .critical {{ color: #dc3545; }}
        .high {{ color: #fd7e14; }}
        .medium {{ color: #ffc107; }}
        .low {{ color: #28a745; }}
        
        .chart-container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        
        .files-section {{
            padding: 40px;
            background: #f9f9f9;
        }}
        
        .files-section h2 {{
            color: #1a237e;
            margin-bottom: 25px;
            font-size: 1.3em;
            font-weight: 600;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 10px;
        }}
        
        .file-card {{
            background: white;
            padding: 20px;
            margin-bottom: 10px;
            border: 1px solid #e0e0e0;
            border-left: 4px solid #ddd;
        }}
        
        .file-card:hover {{
            border-left-color: #1a237e;
        }}
        
        .file-card.high-risk {{
            border-left-color: #c62828;
        }}
        
        .file-card.medium-risk {{
            border-left-color: #f57c00;
        }}
        
        .file-card.low-risk {{
            border-left-color: #2e7d32;
        }}
        
        .file-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding-bottom: 12px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .file-name {{
            font-size: 0.95em;
            font-weight: 600;
            color: #1a237e;
            font-family: 'Consolas', 'Courier New', monospace;
        }}
        
        .risk-badge {{
            padding: 5px 15px;
            font-weight: 600;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .risk-badge.high {{
            background: #ffebee;
            color: #c62828;
            border: 1px solid #ef5350;
        }}
        
        .risk-badge.medium {{
            background: #fff3e0;
            color: #e65100;
            border: 1px solid #ff9800;
        }}
        
        .risk-badge.low {{
            background: #e8f5e9;
            color: #1b5e20;
            border: 1px solid #4caf50;
        }}
        
        .probability-bar {{
            width: 100%;
            height: 8px;
            background: #e0e0e0;
            overflow: hidden;
            margin: 12px 0;
        }}
        
        .probability-fill {{
            height: 100%;
            transition: width 0.3s ease;
        }}
        
        .probability-text {{
            font-size: 0.9em;
            color: #546e7a;
            margin-top: 5px;
        }}
        
        .risk-factors {{
            margin-top: 15px;
            padding: 15px;
            background: #fafafa;
            border-left: 3px solid #c62828;
        }}
        
        .risk-factors h4 {{
            color: #1a237e;
            margin-bottom: 10px;
            font-size: 0.95em;
            font-weight: 600;
        }}
        
        .risk-factors ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .risk-factors li {{
            padding: 4px 0 4px 15px;
            position: relative;
            font-size: 0.9em;
            color: #546e7a;
        }}
        
        .risk-factors li:before {{
            content: "•";
            position: absolute;
            left: 0;
            color: #c62828;
            font-weight: bold;
        }}
        
        .footer {{
            background: #1a237e;
            color: #b0bec5;
            text-align: center;
            padding: 15px;
            font-size: 0.85em;
            border-top: 3px solid #0d47a1;
        }}
        
        .timestamp {{
            color: #78909c;
            font-size: 0.9em;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        th {{
            background-color: #1a237e;
            color: white;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 0.5px;
        }}
        
        tr:hover {{
            background-color: #fafafa;
        }}
        
        .chart-container {{
            background: white;
            padding: 25px;
            margin: 20px 0;
            border: 1px solid #e0e0e0;
        }}
        
        .chart-title {{
            font-size: 1.1em;
            color: #1a237e;
            font-weight: 600;
            margin-bottom: 15px;
        }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Informe de Análisis de Vulnerabilidades</h1>
            <div class="subtitle">Sistema de Detección Basado en Machine Learning</div>
            <div class="timestamp">Generado: {timestamp}</div>
        </div>
        
        <div class="status-banner">
            Estado del Análisis: {status_text}
        </div>
        
        <div class="summary">
            <h3 class="summary-title">Resumen Ejecutivo</h3>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Total de Archivos</div>
                    <div class="stat-number">{total_files}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Riesgo Alto</div>
                    <div class="stat-number high">{high_risk}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Riesgo Medio</div>
                    <div class="stat-number medium">{medium_risk}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Riesgo Bajo</div>
                    <div class="stat-number low">{low_risk}</div>
                </div>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">Distribución de Riesgos</div>
                <canvas id="riskChart"></canvas>
            </div>
        </div>
        
        <div class="files-section">
            <h2>Detalle de Archivos Analizados</h2>
            {files_html}
        </div>
        
        <div class="footer">
            <p>Sistema de Análisis de Vulnerabilidades ML v1.0</p>
            <p>Modelo: Random Forest Classifier | Umbral de detección: 70% | Dataset: 84,588 muestras CVE/CWE</p>
        </div>
    </div>
    
    <script>
        {chart_script}
    </script>
</body>
</html>
    """
    
    return html


def _generate_files_table(details: List[Dict]) -> str:
    """Genera las tarjetas de archivos"""
    if not details:
        return "<p>No hay archivos para mostrar.</p>"
    
    # Ordenar por probabilidad de riesgo (mayor a menor)
    details_sorted = sorted(details, key=lambda x: x.get('risk_probability', 0), reverse=True)
    
    html_parts = []
    
    for file_data in details_sorted:
        file_path = file_data.get('file', 'Unknown')
        probability = file_data.get('risk_probability', 0)
        risk_level = file_data.get('risk_level', 'BAJO')
        features = file_data.get('features', {})
        
        # Determinar clase de riesgo
        if probability >= 0.70:
            risk_class = 'high-risk'
            badge_class = 'high'
        elif probability >= 0.40:
            risk_class = 'medium-risk'
            badge_class = 'medium'
        else:
            risk_class = 'low-risk'
            badge_class = 'low'
        
        # Factores de riesgo
        risk_factors = _extract_risk_factors(features)
        risk_factors_html = ""
        if risk_factors:
            risk_factors_html = f"""
            <div class="risk-factors">
                <h4>Factores de Riesgo Detectados:</h4>
                <ul>
                    {''.join(f'<li>{factor}</li>' for factor in risk_factors)}
                </ul>
            </div>
            """
        
        # Color de barra según riesgo
        if probability >= 0.90:
            bar_color = '#c62828'
        elif probability >= 0.70:
            bar_color = '#d84315'
        elif probability >= 0.40:
            bar_color = '#f57c00'
        else:
            bar_color = '#2e7d32'
        
        card_html = f"""
        <div class="file-card {risk_class}">
            <div class="file-header">
                <div class="file-name">{file_path}</div>
                <div class="risk-badge {badge_class}">{risk_level}</div>
            </div>
            <div class="probability-text">Probabilidad de vulnerabilidad: <strong>{probability:.1%}</strong></div>
            <div class="probability-bar">
                <div class="probability-fill" style="width: {probability*100}%; background-color: {bar_color};"></div>
            </div>
            {risk_factors_html}
        </div>
        """
        
        html_parts.append(card_html)
    
    return '\n'.join(html_parts)


def _extract_risk_factors(features: Dict) -> List[str]:
    """Extrae factores de riesgo de las características"""
    factors = []
    
    risk_map = {
        'has_eval': 'Uso de eval() - ejecución de código arbitrario',
        'has_exec': 'Uso de exec() - ejecución de código arbitrario',
        'has_sql_concat': 'SQL Injection - concatenación de strings en queries',
        'has_command_injection_risk': 'Riesgo de inyección de comandos del sistema',
        'has_hardcoded_secrets': 'Secretos o credenciales hardcodeadas',
        'uses_subprocess_shell': 'subprocess con shell=True - riesgo de inyección',
        'has_pickle_load': 'Deserialización insegura con pickle',
        'has_unsafe_deserialization': 'Deserialización insegura detectada',
        'uses_weak_crypto': 'Uso de algoritmos criptográficos débiles',
        'has_path_traversal_risk': 'Riesgo de path traversal',
        'has_bare_except': 'Manejo de excepciones genérico (bare except)',
        'uses_deprecated_libs': 'Uso de librerías deprecadas',
        'has_flask_debug': 'Flask en modo debug en producción',
        'has_format_string_vuln': 'Vulnerabilidad de format string',
        'has_yaml_unsafe': 'Carga insegura de YAML',
        'uses_os_system': 'Uso de os.system() - riesgo de seguridad',
        'uses_hardcoded_key': 'Clave criptográfica hardcodeada',
    }
    
    for key, description in risk_map.items():
        if features.get(key, False):
            factors.append(description)
    
    # Agregar complejidad si es alta
    max_complexity = features.get('max_function_complexity', 0)
    if max_complexity > 20:
        factors.append(f'Alta complejidad ciclomática (máx: {max_complexity})')
    
    return factors


def _generate_chart_script(high: int, medium: int, low: int) -> str:
    """Genera el script de Chart.js"""
    return f"""
        const ctx = document.getElementById('riskChart').getContext('2d');
        const riskChart = new Chart(ctx, {{
            type: 'doughnut',
            data: {{
                labels: ['Riesgo Alto', 'Riesgo Medio', 'Riesgo Bajo'],
                datasets: [{{
                    data: [{high}, {medium}, {low}],
                    backgroundColor: [
                        '#dc3545',
                        '#ffc107',
                        '#28a745'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    title: {{
                        display: true,
                        text: 'Distribución de Riesgos',
                        font: {{
                            size: 18
                        }}
                    }},
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            font: {{
                                size: 14
                            }},
                            padding: 20
                        }}
                    }}
                }}
            }}
        }});
    """


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Genera reporte HTML de resultados de escaneo'
    )
    parser.add_argument(
        'results_file',
        help='Archivo JSON con resultados del escaneo'
    )
    parser.add_argument(
        '--output',
        help='Archivo HTML de salida (opcional)'
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.results_file):
        print(f"Error: Archivo {args.results_file} no encontrado")
        sys.exit(1)
    
    generate_html_report(args.results_file, args.output)


if __name__ == '__main__':
    main()
