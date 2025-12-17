"""
Script para obtener los archivos modificados en un commit o PR.
Se utiliza en el pipeline CI/CD para analizar solo los cambios.
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import List, Set


def get_changed_files_git(base_ref: str = None, head_ref: str = None) -> List[str]:
    """
    Obtiene la lista de archivos modificados usando git diff
    
    Args:
        base_ref: Referencia base (ej: main, HEAD~1)
        head_ref: Referencia head (ej: HEAD, branch-name)
        
    Returns:
        Lista de rutas de archivos modificados
    """
    try:
        if base_ref and head_ref:
            # Comparar dos referencias específicas (útil para PRs)
            cmd = ['git', 'diff', '--name-only', base_ref, head_ref]
        elif base_ref:
            # Comparar con una referencia base
            cmd = ['git', 'diff', '--name-only', base_ref]
        else:
            # Obtener archivos modificados en el último commit
            cmd = ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD']
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        files = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        return files
    
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando git diff: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        return []


def get_changed_files_github_env() -> List[str]:
    """
    Obtiene archivos modificados desde variables de entorno de GitHub Actions
    
    Returns:
        Lista de archivos modificados
    """
    import os
    
    # GitHub Actions proporciona estas variables
    github_event_name = os.getenv('GITHUB_EVENT_NAME', '')
    github_event_path = os.getenv('GITHUB_EVENT_PATH', '')
    
    if github_event_name == 'pull_request' and github_event_path:
        try:
            with open(github_event_path, 'r') as f:
                event_data = json.load(f)
            
            base_sha = event_data['pull_request']['base']['sha']
            head_sha = event_data['pull_request']['head']['sha']
            
            return get_changed_files_git(base_sha, head_sha)
        except Exception as e:
            print(f"Error leyendo evento de GitHub: {e}", file=sys.stderr)
    
    # Fallback: usar último commit
    return get_changed_files_git()


def filter_scannable_files(files: List[str], extensions: Set[str] = None) -> List[str]:
    """
    Filtra archivos para quedarse solo con los que se pueden escanear
    
    Args:
        files: Lista de archivos
        extensions: Set de extensiones permitidas (ej: {'.py', '.js'})
        
    Returns:
        Lista filtrada de archivos
    """
    if extensions is None:
        extensions = {'.py', '.js'}  # Por defecto Python y JavaScript
    
    scannable = []
    
    for file in files:
        path = Path(file)
        
        # Verificar extensión
        if path.suffix not in extensions:
            continue
        
        # Verificar que el archivo existe
        if not path.exists():
            continue
        
        # Excluir ciertos directorios
        excluded_dirs = {
            '__pycache__',
            'node_modules',
            '.git',
            'venv',
            'env',
            '.venv',
            'build',
            'dist',
            '.pytest_cache'
        }
        
        if any(excluded in path.parts for excluded in excluded_dirs):
            continue
        
        scannable.append(str(path))
    
    return scannable


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Obtiene los archivos modificados para análisis de seguridad'
    )
    parser.add_argument(
        '--base',
        help='Referencia base para comparación (ej: main, HEAD~1)'
    )
    parser.add_argument(
        '--head',
        help='Referencia head para comparación (ej: HEAD, branch-name)'
    )
    parser.add_argument(
        '--output',
        help='Archivo de salida JSON (opcional)'
    )
    parser.add_argument(
        '--extensions',
        nargs='+',
        default=['.py', '.js'],
        help='Extensiones de archivo a incluir (default: .py .js)'
    )
    parser.add_argument(
        '--github',
        action='store_true',
        help='Usar variables de entorno de GitHub Actions'
    )
    
    args = parser.parse_args()
    
    # Obtener archivos modificados
    if args.github:
        changed_files = get_changed_files_github_env()
    else:
        changed_files = get_changed_files_git(args.base, args.head)
    
    if not changed_files:
        print("No se encontraron archivos modificados", file=sys.stderr)
        sys.exit(0)
    
    # Filtrar archivos escaneables
    extensions = set(args.extensions)
    scannable_files = filter_scannable_files(changed_files, extensions)
    
    # Resultados
    result = {
        'total_changed': len(changed_files),
        'scannable': len(scannable_files),
        'files': scannable_files
    }
    
    # Output
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Resultados guardados en: {args.output}")
    else:
        # Imprimir uno por línea para uso en scripts
        for file in scannable_files:
            print(file)
    
    print(f"\nArchivos modificados: {len(changed_files)}", file=sys.stderr)
    print(f"Archivos a escanear: {len(scannable_files)}", file=sys.stderr)


if __name__ == '__main__':
    main()
