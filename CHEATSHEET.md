# 🚀 Comandos Rápidos - Cheat Sheet

## Escaneo Local

### Básico
```bash
# Escanear archivos cambiados en último commit
python run_local.py scan

# Escanear directorio completo
python scripts/vulnerability_scanner.py src/

# Escanear archivo específico
python scripts/vulnerability_scanner.py tests/vulnerable_code_example.py
```

### Con Opciones
```bash
# Cambiar umbral a 80%
python scripts/vulnerability_scanner.py src/ --threshold 0.80

# Escanear lista de archivos
python scripts/get_changed_files.py --output files.json
python scripts/vulnerability_scanner.py --files-list files.json

# Comparar con rama específica
python scripts/get_changed_files.py --base origin/main --head HEAD --output changed.json
```

## Pipeline Completo Local

```bash
# Pipeline completo automático
python run_local.py full

# Con configuración personalizada
python run_local.py full --base origin/develop --threshold 0.75
```

## Testing

```bash
# Todos los tests
pytest tests/ -v

# Solo tests de integración CI/CD
pytest tests/test_cicd_integration.py -v

# Con coverage
pytest tests/ --cov=scripts --cov=ml_model --cov-report=html

# Test específico
pytest tests/test_cicd_integration.py::TestCICDPipeline::test_scanner_detects_vulnerable_code -v
```

## Docker

### Build
```bash
# Construir imagen
docker build -t vulnerability-scanner:latest .

# Construir sin cache
docker build --no-cache -t vulnerability-scanner:latest .
```

### Run
```bash
# Escanear directorio actual
docker run --rm \
  -v "$(pwd):/code:ro" \
  -v "$(pwd)/reports:/app/reports:rw" \
  vulnerability-scanner:latest \
  --target /code --output /app/reports/scan.json

# Escanear archivo específico
docker run --rm \
  -v "$(pwd):/code:ro" \
  vulnerability-scanner:latest \
  --files /code/tests/vulnerable_code_example.py

# Con Docker Compose
docker-compose run vulnerability-scanner

# Entrenar modelo en Docker
docker-compose run model-trainer
```

## Git & CI/CD

### Crear PR de Prueba
```bash
# Nueva rama
git checkout -b test-security-scan

# Modificar archivo
echo "# Test" >> tests/secure_code_example.py

# Commit y push
git add .
git commit -m "test: verificar pipeline de seguridad"
git push origin test-security-scan

# Crear PR desde GitHub UI
```

### Simular CI/CD Localmente
```bash
# Exactamente como en GitHub Actions
python scripts/get_changed_files.py \
  --base $(git rev-parse origin/main) \
  --head $(git rev-parse HEAD) \
  --output changed_files.json

python scripts/vulnerability_scanner.py \
  --files-list changed_files.json \
  --threshold 0.70 \
  --output reports/scan_results.json

python scripts/report_generator.py \
  reports/scan_results.json \
  reports/scan_results.html
```

## Modelo ML

### Entrenar/Re-entrenar
```bash
# Desde script
python ml_model/model.py

# Desde notebook
jupyter notebook train_detector.ipynb

# Ver métricas
python ml_model/model.py 2>&1 | grep -A 10 "Métricas"
```

### Verificar Modelo
```bash
# Ver info del modelo
python -c "
import pickle
with open('ml_model/vulnerability_detector.pkl', 'rb') as f:
    model = pickle.load(f)
    print(f'Model type: {type(model).__name__}')
    print(f'Features: {len(model.feature_names) if hasattr(model, 'feature_names') else 'N/A'}')
"
```

## Reportes

### Generar Reportes
```bash
# HTML desde JSON
python scripts/report_generator.py reports/scan_results.json reports/output.html

# Abrir reporte
start reports/scan_results.html  # Windows
open reports/scan_results.html   # macOS
xdg-open reports/scan_results.html  # Linux
```

### Ver Resultados JSON
```bash
# Ver resumen
cat reports/scan_results.json | jq '.total_files, .high_risk_count, .scan_passed'

# Ver archivos de alto riesgo
cat reports/scan_results.json | jq '.high_risk_files[]'

# Ver detalles de un archivo
cat reports/scan_results.json | jq '.details[] | select(.file == "tests/vulnerable_code_example.py")'
```

## Configuración

### Ver Configuración
```bash
# Ver config completa
cat config.yml

# Ver umbral actual
cat config.yml | grep threshold

# Ver directorios excluidos
cat config.yml | grep -A 10 excluded_directories
```

### Editar Configuración
```bash
# Cambiar umbral (Linux/Mac)
sed -i 's/threshold: 0.70/threshold: 0.80/' config.yml

# Cambiar umbral (Windows PowerShell)
(Get-Content config.yml) -replace 'threshold: 0.70', 'threshold: 0.80' | Set-Content config.yml
```

## Troubleshooting

### Verificar Instalación
```bash
# Python version
python --version

# Dependencias instaladas
pip list | grep -E "scikit-learn|pandas|numpy"

# Modelo existe
ls -lh ml_model/vulnerability_detector.pkl

# Git funciona
git --version
```

### Limpiar y Reinstalar
```bash
# Limpiar cache de Python
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Reinstalar dependencias
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Limpiar reportes
rm -rf reports/*.html reports/*.json
```

### Ver Logs GitHub Actions
```bash
# Obtener última ejecución (requiere gh CLI)
gh run list --limit 1

# Ver logs de última ejecución
gh run view --log

# Descargar artifacts
gh run download
```

## Utilidades

### Estadísticas del Proyecto
```bash
# Contar líneas de código
find . -name "*.py" -not -path "./__pycache__/*" | xargs wc -l

# Contar archivos por tipo
find . -type f | grep -E "\.(py|js|yml|md)$" | sed 's/.*\.//' | sort | uniq -c

# Ver estructura
tree -I '__pycache__|node_modules|venv|.git' -L 3
```

### Benchmarking
```bash
# Tiempo de escaneo
time python scripts/vulnerability_scanner.py tests/

# Tiempo de pipeline completo
time python run_local.py full

# Memoria usada
/usr/bin/time -v python scripts/vulnerability_scanner.py tests/
```

## Desarrollo

### Pre-commit
```bash
# Instalar pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files
```

### Formateo
```bash
# Black (si instalado)
black scripts/ ml_model/ tests/

# isort (si instalado)
isort scripts/ ml_model/ tests/

# Linting
pylint scripts/vulnerability_scanner.py
```

## CI/CD Avanzado

### Forzar Re-run de Workflow
```bash
# Commit vacío
git commit --allow-empty -m "chore: trigger CI"
git push
```

### Ver Status de Checks
```bash
# Usando gh CLI
gh pr checks

# Ver detalles de un workflow
gh workflow view "Security Vulnerability Scanner CI/CD"
```

### Cancelar Workflow
```bash
# Cancelar última ejecución
gh run cancel $(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')
```

## Shortcuts Útiles

```bash
# Alias útiles (agregar a .bashrc o .zshrc)
alias scan="python scripts/vulnerability_scanner.py"
alias scan-local="python run_local.py scan"
alias scan-full="python run_local.py full"
alias scan-test="pytest tests/test_cicd_integration.py -v"
alias scan-report="open reports/scan_results.html"

# Windows PowerShell (agregar a $PROFILE)
function scan { python scripts/vulnerability_scanner.py $args }
function scan-local { python run_local.py scan $args }
function scan-full { python run_local.py full $args }
function scan-test { pytest tests/test_cicd_integration.py -v }
function scan-report { start reports/scan_results.html }
```

## Variables de Entorno Útiles

```bash
# Configurar umbral global
export SECURITY_THRESHOLD=0.80

# Deshabilitar colores en output
export NO_COLOR=1

# Verbose mode
export VERBOSE=1
```

---

## 💡 Tips Rápidos

- 🚀 Usa `run_local.py full` para simular CI/CD completo
- 🧪 Ejecuta tests antes de push: `pytest tests/ -v`
- 📊 Revisa reportes HTML para análisis detallado
- 🐳 Usa Docker para entorno reproducible
- ⚙️ Ajusta `config.yml` para personalizar comportamiento
- 📝 Usa PR template para checklist consistente
- 🔄 Mantén modelo actualizado: `python ml_model/model.py`

---

**Para más información, consulta:**
- 📖 [README.md](README.md) - Documentación completa
- 🚀 [SETUP_GUIDE.md](SETUP_GUIDE.md) - Guía de configuración
- ✅ [IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md) - Checklist
- 📋 [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Resumen
