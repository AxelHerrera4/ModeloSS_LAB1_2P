#!/usr/bin/env python3
"""
Analizador de repositorios GitHub externos.
Permite analizar múltiples proyectos de GitHub desde un lugar centralizado.
"""

import os
import sys
import json
import shutil
import tempfile
import subprocess
import argparse
from pathlib import Path
from typing import List, Dict, Optional


class GitHubRepoAnalyzer:
    """Analiza repositorios de GitHub externos"""
    
    def __init__(self, model_path: str = "ml_model/vulnerability_detector.pkl"):
        self.model_path = model_path
        self.results = []
    
    def clone_repo(self, repo_url: str, temp_dir: str) -> Optional[str]:
        """
        Clona un repositorio de GitHub
        
        Args:
            repo_url: URL del repositorio (https://github.com/user/repo)
            temp_dir: Directorio temporal para clonar
            
        Returns:
            Path al repositorio clonado o None si falla
        """
        print(f"\n📥 Clonando repositorio: {repo_url}")
        
        try:
            # Extraer nombre del repo
            repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
            clone_path = os.path.join(temp_dir, repo_name)
            
            # Clonar con profundidad 1 (más rápido)
            cmd = ['git', 'clone', '--depth', '1', repo_url, clone_path]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos timeout
            )
            
            if result.returncode != 0:
                print(f"❌ Error clonando: {result.stderr}")
                return None
            
            print(f"✅ Repositorio clonado en: {clone_path}")
            return clone_path
            
        except subprocess.TimeoutExpired:
            print("❌ Timeout clonando repositorio (>5 min)")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def analyze_repo(self, repo_path: str, repo_url: str) -> Dict:
        """
        Analiza un repositorio clonado
        
        Args:
            repo_path: Path al repositorio local
            repo_url: URL original del repositorio
            
        Returns:
            Diccionario con resultados del análisis
        """
        print(f"\n🔍 Analizando repositorio: {os.path.basename(repo_path)}")
        
        # Ejecutar scanner
        output_file = f"reports/{os.path.basename(repo_path)}_scan_results.json"
        os.makedirs("reports", exist_ok=True)
        
        cmd = [
            sys.executable,
            "scripts/vulnerability_scanner.py",
            repo_path,
            "--model", self.model_path,
            "--output", output_file,
            "--threshold", "0.70"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutos timeout
            )
            
            # Cargar resultados
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    scan_results = json.load(f)
                
                return {
                    'repo_url': repo_url,
                    'repo_name': os.path.basename(repo_path),
                    'status': 'success',
                    'scan_results': scan_results,
                    'output_file': output_file
                }
            else:
                return {
                    'repo_url': repo_url,
                    'repo_name': os.path.basename(repo_path),
                    'status': 'error',
                    'error': 'No se generó archivo de resultados'
                }
                
        except subprocess.TimeoutExpired:
            return {
                'repo_url': repo_url,
                'repo_name': os.path.basename(repo_path),
                'status': 'timeout',
                'error': 'Análisis excedió tiempo máximo (10 min)'
            }
        except Exception as e:
            return {
                'repo_url': repo_url,
                'repo_name': os.path.basename(repo_path),
                'status': 'error',
                'error': str(e)
            }
    
    def analyze_multiple_repos(self, repo_urls: List[str]) -> List[Dict]:
        """
        Analiza múltiples repositorios
        
        Args:
            repo_urls: Lista de URLs de repositorios
            
        Returns:
            Lista de resultados
        """
        print("\n" + "="*70)
        print(f"🔍 ANÁLISIS DE MÚLTIPLES REPOSITORIOS")
        print(f"   Total de repositorios: {len(repo_urls)}")
        print("="*70)
        
        results = []
        temp_base = tempfile.mkdtemp(prefix='github_analysis_')
        
        try:
            for idx, repo_url in enumerate(repo_urls, 1):
                print(f"\n[{idx}/{len(repo_urls)}] Procesando: {repo_url}")
                print("-" * 70)
                
                # Clonar repositorio
                repo_path = self.clone_repo(repo_url, temp_base)
                
                if repo_path:
                    # Analizar
                    result = self.analyze_repo(repo_path, repo_url)
                    results.append(result)
                    
                    # Mostrar resumen
                    if result['status'] == 'success':
                        scan = result['scan_results']
                        print(f"\n📊 Resultados:")
                        print(f"   Archivos analizados: {scan.get('total_files', 0)}")
                        print(f"   🔴 Alto riesgo: {scan.get('high_risk_count', 0)}")
                        print(f"   🟡 Medio riesgo: {scan.get('medium_risk_count', 0)}")
                        print(f"   🟢 Bajo riesgo: {scan.get('low_risk_count', 0)}")
                        print(f"   Estado: {'✅ APROBADO' if scan.get('scan_passed') else '❌ RECHAZADO'}")
                    else:
                        print(f"\n❌ Error: {result.get('error', 'Unknown')}")
                else:
                    results.append({
                        'repo_url': repo_url,
                        'repo_name': repo_url.split('/')[-1],
                        'status': 'clone_failed',
                        'error': 'No se pudo clonar el repositorio'
                    })
        
        finally:
            # Limpiar directorios temporales
            print(f"\n🧹 Limpiando archivos temporales...")
            try:
                shutil.rmtree(temp_base)
                print("✅ Limpieza completada")
            except Exception as e:
                print(f"⚠️  Error limpiando: {e}")
        
        return results
    
    def generate_summary_report(self, results: List[Dict], output_file: str):
        """
        Genera reporte consolidado de múltiples repositorios
        
        Args:
            results: Lista de resultados de análisis
            output_file: Archivo de salida
        """
        print(f"\n📊 Generando reporte consolidado...")
        
        summary = {
            'total_repos': len(results),
            'successful_scans': sum(1 for r in results if r['status'] == 'success'),
            'failed_scans': sum(1 for r in results if r['status'] != 'success'),
            'total_vulnerabilities': 0,
            'repos_with_high_risk': 0,
            'repositories': []
        }
        
        for result in results:
            if result['status'] == 'success':
                scan = result['scan_results']
                high_risk = scan.get('high_risk_count', 0)
                
                summary['total_vulnerabilities'] += high_risk
                if high_risk > 0:
                    summary['repos_with_high_risk'] += 1
                
                summary['repositories'].append({
                    'name': result['repo_name'],
                    'url': result['repo_url'],
                    'status': 'success',
                    'total_files': scan.get('total_files', 0),
                    'high_risk': high_risk,
                    'medium_risk': scan.get('medium_risk_count', 0),
                    'low_risk': scan.get('low_risk_count', 0),
                    'passed': scan.get('scan_passed', False),
                    'report': result.get('output_file', '')
                })
            else:
                summary['repositories'].append({
                    'name': result['repo_name'],
                    'url': result['repo_url'],
                    'status': result['status'],
                    'error': result.get('error', 'Unknown error')
                })
        
        # Guardar JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Reporte guardado: {output_file}")
        
        # Imprimir resumen
        print("\n" + "="*70)
        print("📊 RESUMEN CONSOLIDADO")
        print("="*70)
        print(f"Total de repositorios analizados: {summary['total_repos']}")
        print(f"✅ Exitosos: {summary['successful_scans']}")
        print(f"❌ Fallidos: {summary['failed_scans']}")
        print(f"🔴 Repositorios con vulnerabilidades: {summary['repos_with_high_risk']}")
        print(f"🚨 Total de vulnerabilidades de alto riesgo: {summary['total_vulnerabilities']}")
        print("="*70)
        
        # Listar repos con vulnerabilidades
        if summary['repos_with_high_risk'] > 0:
            print("\n🚨 Repositorios con vulnerabilidades críticas:")
            for repo in summary['repositories']:
                if repo.get('status') == 'success' and repo.get('high_risk', 0) > 0:
                    print(f"   • {repo['name']}: {repo['high_risk']} archivos de alto riesgo")
                    print(f"     URL: {repo['url']}")
                    print(f"     Reporte: {repo.get('report', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(
        description='🔍 Analiza múltiples repositorios de GitHub',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:

  # Analizar un repositorio
  python scripts/analyze_github_repos.py https://github.com/user/repo

  # Analizar múltiples repositorios
  python scripts/analyze_github_repos.py \\
    https://github.com/user/repo1 \\
    https://github.com/user/repo2

  # Desde archivo con lista de URLs
  python scripts/analyze_github_repos.py --repos-file repos.txt

  # Con threshold personalizado
  python scripts/analyze_github_repos.py \\
    https://github.com/user/repo \\
    --threshold 0.80

Formato de repos.txt (una URL por línea):
  https://github.com/user/repo1
  https://github.com/user/repo2
  https://github.com/user/repo3
        """
    )
    
    parser.add_argument(
        'repos',
        nargs='*',
        help='URLs de repositorios de GitHub'
    )
    parser.add_argument(
        '--repos-file',
        help='Archivo con lista de URLs (una por línea)'
    )
    parser.add_argument(
        '--model',
        default='ml_model/vulnerability_detector.pkl',
        help='Ruta al modelo ML'
    )
    parser.add_argument(
        '--output',
        default='reports/multi_repo_summary.json',
        help='Archivo de salida para resumen consolidado'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.70,
        help='Umbral de vulnerabilidad'
    )
    
    args = parser.parse_args()
    
    # Recopilar URLs
    repo_urls = []
    
    if args.repos:
        repo_urls.extend(args.repos)
    
    if args.repos_file:
        try:
            with open(args.repos_file, 'r') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                repo_urls.extend(urls)
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {args.repos_file}")
            return 1
    
    if not repo_urls:
        print("❌ No se especificaron repositorios")
        print("Uso: python scripts/analyze_github_repos.py <URL1> <URL2> ...")
        print("  o: python scripts/analyze_github_repos.py --repos-file repos.txt")
        return 1
    
    # Verificar modelo
    if not os.path.exists(args.model):
        print(f"❌ Modelo no encontrado: {args.model}")
        print("Ejecuta primero: python ml_model/model.py")
        return 1
    
    # Crear analizador
    analyzer = GitHubRepoAnalyzer(args.model)
    
    # Analizar repositorios
    results = analyzer.analyze_multiple_repos(repo_urls)
    
    # Generar reporte consolidado
    analyzer.generate_summary_report(results, args.output)
    
    # Exit code basado en resultados
    failed = sum(1 for r in results if r['status'] != 'success')
    if failed > 0:
        print(f"\n⚠️  {failed} repositorio(s) no pudieron ser analizados")
        return 1
    
    vulnerabilities = sum(
        r['scan_results'].get('high_risk_count', 0)
        for r in results
        if r['status'] == 'success'
    )
    
    if vulnerabilities > 0:
        print(f"\n❌ Se encontraron {vulnerabilities} vulnerabilidades críticas en total")
        return 1
    
    print("\n✅ Todos los repositorios pasaron el análisis de seguridad")
    return 0


if __name__ == '__main__':
    sys.exit(main())
