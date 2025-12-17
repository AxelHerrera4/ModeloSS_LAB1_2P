# 🚀 Guía Rápida de Configuración del Pipeline CI/CD

## Configuración Inicial (5 minutos)

### 1. Verificar Requisitos

```bash
# Python 3.11+
python --version

# Git instalado
git --version
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Verificar o Entrenar el Modelo

```bash
# Opción A: Si ya tienes el modelo
ls -lh ml_model/vulnerability_detector.pkl

# Opción B: Entrenar nuevo modelo (30-60 min)
python ml_model/model.py
```

### 4. Probar Localmente

```bash
# Test rápido
python scripts/vulnerability_scanner.py tests/vulnerable_code_example.py

# Debe mostrar: ALERTA con 99%+ probabilidad
```

---

## Activar Pipeline en GitHub (2 minutos)

### Paso 1: Push al Repositorio

```bash
git add .
git commit -m "feat: configurar pipeline CI/CD de seguridad"
git push origin main
```

### Paso 2: Verificar GitHub Actions

1. Ve a tu repositorio en GitHub
2. Click en la pestaña **Actions**
3. Verifica que el workflow `🛡️ Security Vulnerability Scanner CI/CD` aparece
4. El workflow se ejecutará automáticamente en el próximo push/PR

### Paso 3: Crear una Pull Request de Prueba

```bash
# Crear rama de prueba
git checkout -b test-security-scan

# Modificar un archivo
echo "# Test change" >> tests/secure_code_example.py

# Commit y push
git add tests/secure_code_example.py
git commit -m "test: verificar pipeline de seguridad"
git push origin test-security-scan

# Crear PR desde GitHub UI
```

El pipeline ejecutará automáticamente y:
- ✅ Detectará el archivo modificado
- ✅ Lo escaneará con el modelo ML
- ✅ Comentará los resultados en la PR
- ✅ Aprobará o rechazará según las vulnerabilidades

---

## Configuración del Modelo (Si No Existe)

### Opción 1: Subir Modelo Pre-entrenado

Si tienes el modelo `.pkl`:

```bash
# Copiar modelo al directorio correcto
cp /ruta/al/vulnerability_detector.pkl ml_model/

# Añadir al repositorio
git add ml_model/vulnerability_detector.pkl
git commit -m "chore: agregar modelo ML entrenado"
git push
```

### Opción 2: Entrenar en CI/CD

El workflow ya incluye un paso que entrena automáticamente si el modelo no existe. Solo asegúrate de que los datasets estén presentes:

```bash
ls -lh Dataset/
# Debe mostrar:
# data_Python.csv
# data_JavaScript.csv
```

### Opción 3: Git LFS (Archivos Grandes)

Si el modelo es muy grande (>100MB):

```bash
# Instalar Git LFS
git lfs install

# Trackear archivos .pkl
git lfs track "*.pkl"

# Commit
git add .gitattributes ml_model/vulnerability_detector.pkl
git commit -m "chore: configurar Git LFS para modelo ML"
git push
```

---

## Verificación del Pipeline

### Checklist de Configuración

- [ ] Python 3.11+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Modelo ML existe (`ml_model/vulnerability_detector.pkl`)
- [ ] Tests pasan localmente (`pytest tests/`)
- [ ] Workflow existe (`.github/workflows/security-scan.yml`)
- [ ] Repositorio pusheado a GitHub
- [ ] Actions habilitado en GitHub (Settings > Actions > Allow all actions)

### Test Manual del Pipeline

```bash
# 1. Simular detección de archivos cambiados
python scripts/get_changed_files.py --base HEAD~1 --output changed.json

# 2. Escanear archivos
python scripts/vulnerability_scanner.py --files-list changed.json

# 3. Verificar reporte
cat reports/scan_results.json
open reports/scan_results.html
```

Si los 3 pasos funcionan, el pipeline está listo.

---

## Configuración Avanzada (Opcional)

### Ajustar Umbrales

Editar `config.yml`:

```yaml
model:
  threshold: 0.70  # Cambiar a 0.80 para ser más estricto
```

O en el workflow (`.github/workflows/security-scan.yml`):

```yaml
env:
  RISK_THRESHOLD: '0.80'
```

### Agregar Más Branches

Editar `.github/workflows/security-scan.yml`:

```yaml
on:
  push:
    branches: [ main, develop, staging, production ]
  pull_request:
    branches: [ main, develop, staging, production ]
```

### Excluir Directorios

Editar `config.yml`:

```yaml
scanner:
  excluded_directories:
    - "__pycache__"
    - "node_modules"
    - "venv"
    - "tests"  # Agregar para excluir tests
```

---

## Solución Rápida de Problemas

### Error: "Modelo no encontrado"

```bash
# Entrenar el modelo
python ml_model/model.py

# O descargar desde releases
wget https://github.com/tu-repo/releases/download/v1.0/vulnerability_detector.pkl -O ml_model/vulnerability_detector.pkl
```

### Error: "No module named 'sklearn'"

```bash
pip install -r requirements.txt
```

### El workflow no se ejecuta

1. Verifica que Actions esté habilitado: `Repo > Settings > Actions`
2. Verifica que el workflow esté en `.github/workflows/security-scan.yml`
3. Push a una rama monitoreada (`main`, `develop`)

### Falsos positivos

```bash
# Aumentar umbral temporalmente
python scripts/vulnerability_scanner.py archivo.py --threshold 0.90
```

---

## Próximos Pasos

1. **Revisar resultados**: Check las PRs y Issues automáticos
2. **Ajustar configuración**: Modifica umbrales según tu proyecto
3. **Entrenar con datos propios**: Agrega ejemplos específicos de tu codebase
4. **Integrar con otros tools**: Combina con linters, SAST, etc.

---

## Recursos Útiles

- 📖 [README completo](README.md)
- 🔧 [Configuración](config.yml)
- 🧪 [Tests](tests/test_cicd_integration.py)
- 🐳 [Docker](Dockerfile)

---

**¿Necesitas ayuda?** Revisa los logs en GitHub Actions o ejecuta los tests localmente.

✅ **¡Pipeline configurado! Ahora cada commit será analizado automáticamente.** 🎉
