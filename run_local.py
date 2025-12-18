#!/usr/bin/env python3
"""
Script de utilidad para ejecutar el pipeline localmente.
Simula el comportamiento del CI/CD en tu máquina local.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def print_banner():
    """Imprime banner del scanner"""
    print("\n" + "="*70)
    print("🛡️  ML SECURITY VULNERABILITY SCANNER - LOCAL MODE")
    print("="*70 + "\n")


def check_requirements():
    """Verifica que los requisitos estén instalados"""
    print("🔍 Verificando requisitos...")
    
    # Verificar Python
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ requerido")
        return False
    
    print("✅ Python version OK")
    
    # Verificar modelo
    model_path = Path("ml_model/vulnerability_detector.pkl")
    if not model_path.exists():
        print("⚠️  Modelo no encontrado en ml_model/vulnerability_detector.pkl")
        print("   Ejecuta: python ml_model/model.py")
        return False
    
    print("✅ Modelo ML encontrado")
    
    # Verificar dependencias
    try:
        import sklearn
        import pandas
        import numpy
        print("✅ Dependencias instaladas")
    except ImportError as e:
        print(f"❌ Falta dependencia: {e.name}")
        print("   Ejecuta: pip install -r requirements.txt")
        return False
    
    return True


def get_changed_files(base="HEAD~1", head="HEAD"):
    """Obtiene archivos cambiados"""
    print(f"\n📂 Detectando archivos cambiados ({base}..{head})...")
    
    cmd = [
        sys.executable,
        "scripts/get_changed_files.py",
        "--base", base,
        "--head", head,
        "--output", "changed_files.json"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error detectando archivos: {result.stderr}")
        return False
    
    print(result.stderr.strip())  # Imprimir estadísticas
    return True


def run_scanner(mode="changed", target=None, threshold=0.70):
    """Ejecuta el scanner"""
    print(f"\n🔍 Ejecutando scanner ML (umbral: {threshold*100}%)...")
    
    if mode == "changed":
        cmd = [
            sys.executable,
            "scripts/vulnerability_scanner.py",
            "--files-list", "changed_files.json",
            "--threshold", str(threshold),
            "--output", "reports/scan_results.json"
        ]
    elif mode == "directory":
        cmd = [
            sys.executable,
            "scripts/vulnerability_scanner.py",
            target or ".",
            "--threshold", str(threshold),
            "--output", "reports/scan_results.json"
        ]
    elif mode == "file":
        cmd = [
            sys.executable,
            "scripts/vulnerability_scanner.py",
            target,
            "--threshold", str(threshold),
            "--output", "reports/scan_results.json"
        ]
    else:
        print(f"❌ Modo no soportado: {mode}")
        return False
    
    result = subprocess.run(cmd)
    return result.returncode == 0


def open_report():
    """Abre el reporte HTML"""
    report_path = Path("reports/scan_results.html")
    
    if not report_path.exists():
        print("⚠️  Reporte HTML no encontrado")
        return
    
    print(f"\n📊 Abriendo reporte: {report_path}")
    
    # Detectar sistema operativo y abrir
    if sys.platform == "win32":
        os.startfile(report_path)
    elif sys.platform == "darwin":
        subprocess.run(["open", report_path])
    else:
        subprocess.run(["xdg-open", report_path])


def run_tests():
    """Ejecuta los tests"""
    print("\n🧪 Ejecutando tests...")
    
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v"]
    result = subprocess.run(cmd)
    
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(
        description="🛡️  Ejecuta el pipeline de seguridad localmente",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Escanear archivos modificados en último commit
  python run_local.py scan
  
  # Escanear directorio específico
  python run_local.py scan --directory src/
  
  # Escanear archivo específico
  python run_local.py scan --file tests/vulnerable_code_example.py
  
  # Ejecutar tests
  python run_local.py test
  
  # Pipeline completo (cambios + scan + reporte)
  python run_local.py full
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comando a ejecutar')
    
    # Comando: scan
    scan_parser = subparsers.add_parser('scan', help='Escanear código')
    scan_parser.add_argument('--directory', help='Directorio a escanear')
    scan_parser.add_argument('--file', help='Archivo a escanear')
    scan_parser.add_argument('--base', default='HEAD~1', help='Base para git diff')
    scan_parser.add_argument('--head', default='HEAD', help='Head para git diff')
    scan_parser.add_argument('--threshold', type=float, default=0.70, 
                           help='Umbral de vulnerabilidad (0.0-1.0)')
    scan_parser.add_argument('--no-report', action='store_true',
                           help='No abrir reporte HTML')
    
    # Comando: test
    test_parser = subparsers.add_parser('test', help='Ejecutar tests')
    
    # Comando: full
    full_parser = subparsers.add_parser('full', 
                                       help='Pipeline completo: cambios + scan + reporte')
    full_parser.add_argument('--base', default='HEAD~1', help='Base para git diff')
    full_parser.add_argument('--head', default='HEAD', help='Head para git diff')
    full_parser.add_argument('--threshold', type=float, default=0.70,
                           help='Umbral de vulnerabilidad (0.0-1.0)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    print_banner()
    
    # Verificar requisitos
    if not check_requirements():
        return 1
    
    # Ejecutar comando
    if args.command == 'test':
        success = run_tests()
        return 0 if success else 1
    
    elif args.command == 'scan':
        if args.file:
            success = run_scanner('file', args.file, args.threshold)
        elif args.directory:
            success = run_scanner('directory', args.directory, args.threshold)
        else:
            # Primero obtener archivos cambiados
            if not get_changed_files(args.base, args.head):
                return 1
            success = run_scanner('changed', threshold=args.threshold)
        
        if success and not args.no_report:
            open_report()
        
        return 0 if success else 1
    
    elif args.command == 'full':
        # Pipeline completo
        print("\n🚀 Ejecutando pipeline completo...\n")
        
        # 1. Detectar cambios
        if not get_changed_files(args.base, args.head):
            return 1
        
        # 2. Ejecutar scanner
        success = run_scanner('changed', threshold=args.threshold)
        
        # 3. Abrir reporte
        if success:
            print("\n✅ Pipeline completado exitosamente!")
            open_report()
            return 0
        else:
            print("\n❌ Pipeline falló - vulnerabilidades detectadas")
            open_report()
            return 1


if __name__ == '__main__':
    sys.exit(main())
