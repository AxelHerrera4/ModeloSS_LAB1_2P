# 🚀 Guía Rápida: Cómo Probar el Sistema

## 📋 Tabla de Contenidos

1. [Prueba Local (Tu Proyecto)](#1-prueba-local-tu-proyecto)
2. [Prueba en GitHub (Tu Repositorio)](#2-prueba-en-github-tu-repositorio)
3. [Analizar Múltiples Proyectos Externos](#3-analizar-múltiples-proyectos-externos)
4. [Instalar en Otros Repositorios](#4-instalar-en-otros-repositorios)

---

## 1. Prueba Local (Tu Proyecto)

### Opción A: Script Automático

```bash
# Pipeline completo
python run_local.py full

# Ver reporte
start reports/scan_results.html
```

### Opción B: Manual Paso a Paso

```bash
# 1. Verifica que el modelo exista
dir ml_model\vulnerability_detector.pkl

# 2. Instala dependencias
pip install -r requirements.txt

# 3. Escanea archivos de prueba
python scripts\vulnerability_scanner.py tests\vulnerable_code_example.py

# 4. Deberías ver: "ALERTA" con 99%+ probabilidad

# 5. Escanea código seguro
python scripts\vulnerability_scanner.py tests\secure_code_example.py

# 6. Deberías ver: probabilidad baja (<70%)
```

### Opción C: Prueba con Cambios Simulados

```bash
# 1. Detectar archivos cambiados
python scripts\get_changed_files.py --base HEAD~1 --output changed.json

# 2. Escanear solo esos archivos
python scripts\vulnerability_scanner.py --files-list changed.json

# 3. Ver reporte
start reports\scan_results.html
```

---

## 2. Prueba en GitHub (Tu Repositorio)

### Paso 1: Verifica que Todo Esté Listo

```bash
# Lista de archivos necesarios
dir .github\workflows\security-scan.yml
dir config.yml
dir scripts\get_changed_files.py
dir ml_model\vulnerability_detector.pkl
```

### Paso 2: Haz Commit y Push

```powershell
# 1. Agrega todos los archivos
git add .

# 2. Commit
git commit -m "feat: implementar pipeline CI/CD de seguridad ML"

# 3. Push a GitHub
git push origin main
```

### Paso 3: Verifica GitHub Actions

1. Ve a tu repositorio en GitHub
2. Click en **"Actions"** (pestaña superior)
3. Deberías ver el workflow **"🛡️ Security Vulnerability Scanner CI/CD"**
4. Click en la ejecución más reciente para ver logs

### Paso 4: Crea una Pull Request de Prueba

```powershell
# 1. Crea nueva rama
git checkout -b test-security-pipeline

# 2. Modifica un archivo
echo "# Test change" >> tests\secure_code_example.py

# 3. Commit
git add tests\secure_code_example.py
git commit -m "test: verificar pipeline de seguridad"

# 4. Push
git push origin test-security-pipeline
```

5. Ve a GitHub y crea la Pull Request
6. El bot comentará automáticamente con resultados
7. Revisa el comentario con la tabla de vulnerabilidades

---

## 3. Analizar Múltiples Proyectos Externos

### ⭐ NUEVO: Análisis de Repositorios Externos

Ahora puedes analizar **cualquier repositorio de GitHub** sin instalarlo:

### Opción A: Analizar Un Repositorio

```bash
python scripts\analyze_github_repos.py https://github.com/usuario/repo
```

### Opción B: Analizar Múltiples Repositorios

```bash
python scripts\analyze_github_repos.py ^
  https://github.com/usuario/repo1 ^
  https://github.com/usuario/repo2 ^
  https://github.com/usuario/repo3
```

### Opción C: Desde Archivo de Lista

```bash
# 1. Edita repos_to_analyze.txt
notepad repos_to_analyze.txt

# 2. Agrega URLs (una por línea):
https://github.com/usuario/repo1
https://github.com/usuario/repo2

# 3. Ejecuta análisis
python scripts\analyze_github_repos.py --repos-file repos_to_analyze.txt
```

### Ver Resultados

```bash
# Ver reporte consolidado
type reports\multi_repo_summary.json

# Ver reportes individuales
dir reports\*_scan_results.json
dir reports\*_scan_results.html
```

### Ejemplo Completo

```powershell
# Analizar 3 repos de ejemplo
python scripts\analyze_github_repos.py ^
  https://github.com/django/django ^
  https://github.com/pallets/flask ^
  https://github.com/psf/requests

# Espera unos minutos...
# Ver resumen consolidado
start reports\multi_repo_summary.json

# Ver reportes individuales
start reports\django_scan_results.html
start reports\flask_scan_results.html
start reports\requests_scan_results.html
```

---

## 4. Instalar en Otros Repositorios

Si quieres que **otros repositorios** tengan el pipeline automático:

### Paso 1: Copia los Archivos Necesarios

Archivos mínimos necesarios:

```
otro-repo/
├── .github/
│   └── workflows/
│       └── security-scan.yml
├── ml_model/
│   └── vulnerability_detector.pkl
├── scripts/
│   ├── code_analyzer.py
│   ├── vulnerability_scanner.py
│   ├── report_generator.py
│   └── get_changed_files.py
├── config.yml
└── requirements.txt
```

### Paso 2: Copia con Script

```powershell
# Desde este proyecto, crea un paquete
$destino = "C:\ruta\a\otro-repo"

# Copia archivos necesarios
Copy-Item .github\workflows\security-scan.yml $destino\.github\workflows\ -Force
Copy-Item config.yml $destino\ -Force
Copy-Item requirements.txt $destino\ -Force
Copy-Item -Recurse scripts $destino\ -Force
Copy-Item -Recurse ml_model $destino\ -Force

# O usa el método manual
```

### Paso 3: Commit en el Otro Repo

```bash
cd otro-repo
git add .github scripts ml_model config.yml requirements.txt
git commit -m "feat: agregar pipeline de seguridad ML"
git push
```

---

## 5. Casos de Uso Comunes

### Caso 1: Analizar Proyecto de un Cliente

```bash
# Cliente te da acceso a su repo
python scripts\analyze_github_repos.py https://github.com/cliente/proyecto

# Generas reporte
start reports\proyecto_scan_results.html

# Envías el reporte al cliente
```

### Caso 2: Auditoría de Múltiples Proyectos

```bash
# Crea lista de proyectos
echo https://github.com/proyecto1 > proyectos.txt
echo https://github.com/proyecto2 >> proyectos.txt
echo https://github.com/proyecto3 >> proyectos.txt

# Analiza todos
python scripts\analyze_github_repos.py --repos-file proyectos.txt

# Revisa resumen
start reports\multi_repo_summary.json
```

### Caso 3: CI/CD en Tu Organización

```bash
# Instala en cada repo de la organización
# Cada repo tendrá análisis automático
# Centraliza reportes en un dashboard
```

---

## 📊 Qué Esperar

### Análisis Local
- ⏱️ **Tiempo:** 5-30 segundos por archivo
- 📁 **Reportes:** `reports/scan_results.html` y `.json`
- ✅ **Exit code 0** si no hay vulnerabilidades
- ❌ **Exit code 1** si hay vulnerabilidades

### Análisis de Repos Externos
- ⏱️ **Tiempo:** 2-10 minutos por repo (depende del tamaño)
- 📥 **Clone temporal:** Se elimina automáticamente
- 📊 **Reporte consolidado:** Todos los repos en un JSON
- 📑 **Reportes individuales:** HTML + JSON por repo

### GitHub Actions
- ⏱️ **Tiempo:** 2-5 minutos por PR
- 💬 **Comentario automático:** En la PR con resultados
- 🎫 **Issue automático:** Si >3 archivos críticos
- ⛔ **Bloqueo:** Impide merge si hay vulnerabilidades

---

## 🚨 Troubleshooting

### "Modelo no encontrado"

```bash
# Entrena el modelo
python ml_model\model.py

# O usa el notebook
jupyter notebook train_detector.ipynb
```

### "Git no instalado" (para repos externos)

```bash
# Instala Git
winget install Git.Git

# Verifica
git --version
```

### "Timeout clonando repositorio"

```bash
# Repos muy grandes pueden exceder timeout
# Intenta clonar manualmente primero
git clone --depth 1 https://github.com/user/repo temp_repo
python scripts\vulnerability_scanner.py temp_repo
```

### Workflow no se ejecuta en GitHub

```bash
# 1. Verifica que Actions esté habilitado
# GitHub > Settings > Actions > Allow all actions

# 2. Verifica el archivo
dir .github\workflows\security-scan.yml

# 3. Push a branch monitoreada (main/develop)
git push origin main
```

---

## ✅ Checklist de Verificación

Antes de considerar que funciona, verifica:

- [ ] Escaneo local funciona: `python run_local.py scan`
- [ ] Tests pasan: `pytest tests/test_cicd_integration.py -v`
- [ ] Detecta vulnerable: Alta probabilidad en `vulnerable_code_example.py`
- [ ] Detecta seguro: Baja probabilidad en `secure_code_example.py`
- [ ] GitHub Actions se ejecuta en push
- [ ] Bot comenta en PRs automáticamente
- [ ] Reportes HTML se generan correctamente
- [ ] Análisis de repos externos funciona

---

## 🎯 Resumen Rápido

```bash
# PRUEBA LOCAL
python run_local.py full

# PRUEBA EN GITHUB
git push origin main
# Crear PR de prueba

# ANALIZAR REPOS EXTERNOS
python scripts\analyze_github_repos.py https://github.com/user/repo

# INSTALAR EN OTRO REPO
# Copiar archivos y hacer push
```

---

**🎉 ¡Ahora tienes 3 formas de usar el sistema!**

1. **Análisis local** - Para desarrollo
2. **CI/CD automático** - Para tu repo
3. **Análisis externo** - Para cualquier repo de GitHub

¿Necesitas ayuda? Revisa [CHEATSHEET.md](CHEATSHEET.md) para más comandos.
