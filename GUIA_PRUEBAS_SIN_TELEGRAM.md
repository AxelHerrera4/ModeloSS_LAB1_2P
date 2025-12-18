# 🧪 Guía de Pruebas - Sin Telegram (Para Testing Rápido)

## 🎯 Objetivo
Probar el pipeline CI/CD completo sin configurar Telegram primero.

---

## 📋 Pre-requisitos

```powershell
# Verificar Python instalado
python --version
# Debe mostrar Python 3.11 o superior

# Verificar Git instalado
git --version

# Verificar que estás en el directorio del proyecto
cd d:\ModeloSS_LAB1_2P
```

---

## PASO 1: Instalar Dependencias (2 minutos)

```powershell
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Si da error de permisos, ejecutar:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
pip list | Select-String "scikit-learn"
pip list | Select-String "pandas"
```

---

## PASO 2: Verificar el Modelo ML (1 minuto)

```powershell
# Opción A: Verificar si existe el modelo entrenado
Test-Path ml_model\vulnerability_detector.pkl

# Si dice "False", necesitas entrenar el modelo
# Si dice "True", ya está listo ✅

# Opción B: Test rápido del modelo
python -c "from ml_model.model import VulnerabilityPredictor; p = VulnerabilityPredictor('ml_model/vulnerability_detector.pkl'); print(f'Modelo cargado: {p.is_trained}')"
```

### Si necesitas entrenar el modelo:

```powershell
# Método 1: Jupyter Notebook (recomendado)
jupyter notebook train_detector.ipynb
# Ejecutar todas las celdas (Cell → Run All)
# Esperar 15-30 minutos

# Método 2: Script directo (más rápido)
python ml_model\model.py
# Esperar 5-10 minutos

# Verificar que se creó
Test-Path ml_model\vulnerability_detector.pkl
```

---

## PASO 3: Prueba Local del Scanner (3 minutos)

### 3.1 Escanear archivo de ejemplo vulnerable

```powershell
# Escanear archivo vulnerable de ejemplo
python scripts\vulnerability_scanner.py tests\vulnerable_code_example.py

# Deberías ver algo como:
# ❌ HIGH RISK - tests\vulnerable_code_example.py
# Vulnerability Type: Code Injection
# Probability: 95.3%
```

### 3.2 Escanear archivo seguro

```powershell
# Escanear archivo seguro
python scripts\vulnerability_scanner.py tests\secure_code_example.py

# Deberías ver:
# ✅ LOW RISK - tests\secure_code_example.py
# Vulnerability Type: None
# Probability: 12.1%
```

### 3.3 Ver reporte HTML

```powershell
# Generar reporte
python scripts\report_generator.py reports\scan_results.json reports\scan_results.html

# Abrir reporte en navegador
start reports\scan_results.html
```

---

## PASO 4: Ejecutar Tests Unitarios (2 minutos)

```powershell
# Ejecutar todos los tests
pytest tests\test_scanner.py -v

# Deberías ver algo como:
# tests/test_scanner.py::TestCodeAnalyzer::test_analyze_python_code_basic PASSED
# tests/test_scanner.py::TestCodeAnalyzer::test_detect_sql_injection_python PASSED
# ... más tests ...
# ======================== X passed in Y.XXs ========================

# Si algún test falla, no te preocupes por ahora
```

---

## PASO 5: Crear Archivos de Prueba (2 minutos)

### 5.1 Crear archivo vulnerable para testing

```powershell
# Crear archivo con SQL Injection
@"
import sqlite3

def get_user_by_id(user_id):
    # VULNERABLE: SQL Injection
    query = "SELECT * FROM users WHERE id = " + user_id
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def delete_user(user_id):
    # VULNERABLE: Sin validación
    query = f"DELETE FROM users WHERE id = {user_id}"
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
"@ | Out-File -FilePath "test_vulnerable.py" -Encoding UTF8

# Escanear
python scripts\vulnerability_scanner.py test_vulnerable.py
# Debería detectar vulnerabilidad con alta probabilidad
```

### 5.2 Crear archivo seguro para testing

```powershell
# Crear archivo seguro
@"
import sqlite3

def get_user_by_id(user_id: int):
    # SEGURO: Query parametrizada
    query = "SELECT * FROM users WHERE id = ?"
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

def delete_user(user_id: int):
    # SEGURO: Validación y query parametrizada
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("ID inválido")
    
    query = "DELETE FROM users WHERE id = ?"
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    conn.commit()
"@ | Out-File -FilePath "test_seguro.py" -Encoding UTF8

# Escanear
python scripts\vulnerability_scanner.py test_seguro.py
# Debería mostrar bajo riesgo
```

---

## PASO 6: Preparar Git y Ramas (3 minutos)

### 6.1 Verificar estado del repositorio

```powershell
# Ver rama actual
git branch

# Ver estado
git status
```

### 6.2 Crear ramas necesarias

```powershell
# Asegurarte de estar en main
git checkout main

# Crear rama dev
git checkout -b dev
git push origin dev

# Crear rama test
git checkout -b test
git push origin test

# Volver a main
git checkout main

# Verificar que se crearon
git branch -a
# Deberías ver: main, dev, test
```

---

## PASO 7: Modificar Workflow para Funcionar Sin Telegram (2 minutos)

El workflow ya está configurado con `continue-on-error: true` en las notificaciones Telegram, así que funcionará sin problemas. Pero vamos a verificar:

```powershell
# Ver el workflow
Get-Content .github\workflows\complete-pipeline.yml | Select-String "continue-on-error"

# Deberías ver varias líneas con "continue-on-error: true"
# Esto significa que si Telegram no está configurado, no falla el pipeline
```

---

## PASO 8: Prueba Local del Workflow (5 minutos)

### 8.1 Simular detección de archivos cambiados

```powershell
# Ir a rama dev
git checkout dev

# Hacer un cambio de prueba
echo "# Test" >> README.md
git add README.md
git commit -m "test: cambio de prueba"

# Obtener los archivos cambiados
python scripts\get_changed_files.py --base origin/main --head HEAD --output changed_files.json

# Ver qué archivos detectó
Get-Content changed_files.json | ConvertFrom-Json

# Debería mostrar:
# files: [lista de archivos]
# scannable: número de archivos Python/JS
```

### 8.2 Escanear solo archivos cambiados

```powershell
# Escanear los archivos del diff
python scripts\vulnerability_scanner.py --files-list changed_files.json

# Ver reporte
start reports\scan_results.html
```

---

## PASO 9: Probar en GitHub Actions (SIN Telegram) (10 minutos)

### 9.1 Hacer commit de archivos de prueba

```powershell
# Asegúrate de estar en dev
git checkout dev

# Agregar el archivo vulnerable que creamos
git add test_vulnerable.py
git commit -m "test: agregar código vulnerable para prueba"
git push origin dev
```

### 9.2 Crear Pull Request en GitHub

1. Ve a tu repositorio en GitHub
2. Click en **"Pull requests"**
3. Click en **"New pull request"**
4. Configurar:
   - **Base**: `test`
   - **Compare**: `dev`
5. Click **"Create pull request"**
6. Título: `Test del pipeline con código vulnerable`
7. Click **"Create pull request"**

### 9.3 Observar el Pipeline Ejecutándose

1. Ve a la pestaña **"Actions"** en tu repositorio
2. Verás el workflow **"🚀 CI/CD Pipeline Completo"** ejecutándose
3. Click en el workflow para ver detalles
4. Observa:
   - ✅ **Etapa 1: Security Scan** debería ejecutarse
   - ❌ Debería **detectar la vulnerabilidad** y **FALLAR**
   - 📝 Debería crear un **comentario en el PR**
   - 🏷️ Debería agregar **etiquetas** al PR

**Nota**: Las notificaciones de Telegram NO se enviarán (porque no están configuradas), pero el resto del pipeline funcionará perfectamente.

### 9.4 Ver Resultados

1. Vuelve al Pull Request
2. Deberías ver:
   - ❌ Check **"security-scan"** en rojo (failed)
   - 💬 Comentario automático con detalles de la vulnerabilidad
   - 🏷️ Etiquetas: `fixing-required`, `security-vulnerability`
   - 📋 Una issue automática creada

---

## PASO 10: Probar con Código Seguro (5 minutos)

### 10.1 Corregir el código vulnerable

```powershell
# Estar en dev
git checkout dev

# Reemplazar con código seguro
Remove-Item test_vulnerable.py

# Agregar el código seguro
git add test_seguro.py
git commit -m "fix: reemplazar código vulnerable con versión segura"
git push origin dev
```

### 10.2 Observar el Pipeline de Nuevo

1. El pipeline se ejecutará automáticamente en el mismo PR
2. Esta vez debería:
   - ✅ **Etapa 1: Security Scan** - PASAR
   - ✅ **Etapa 2: Merge a test** - EJECUTARSE
   - ✅ **Etapa 3: Tests** - EJECUTARSE
   - ✅ Todo en verde

### 10.3 Ver el Merge Automático

Si todo pasa:
- El código se mergeará automáticamente a `test`
- Luego a `main`
- El despliegue intentará ejecutarse (fallará si no hay secrets de Docker/Railway configurados, pero eso es OK por ahora)

---

## PASO 11: Verificar Resultados Completos (2 minutos)

### 11.1 Ver artifacts generados

1. En GitHub Actions, click en el workflow completado
2. Scroll hasta abajo
3. En **"Artifacts"** deberías ver:
   - `security-scan-reports` - Descárgalo
4. Descomprimir y abrir `scan_results.html`

### 11.2 Ver cambios en las ramas

```powershell
# Ver commits en test
git checkout test
git pull origin test
git log --oneline -5

# Ver commits en main
git checkout main
git pull origin main
git log --oneline -5

# Deberías ver los merges automáticos
```

---

## ✅ Checklist de Verificación

Marca lo que has completado:

- [ ] Dependencias instaladas
- [ ] Modelo ML verificado/entrenado
- [ ] Escaneo local funciona (vulnerable detectado)
- [ ] Escaneo local funciona (seguro detectado)
- [ ] Reportes HTML se generan correctamente
- [ ] Tests unitarios pasan
- [ ] Ramas dev, test, main creadas
- [ ] Archivos de prueba creados
- [ ] PR con código vulnerable detecta vulnerabilidad
- [ ] PR con código seguro pasa todas las etapas
- [ ] Comentarios automáticos en PR funcionan
- [ ] Etiquetas automáticas se aplican
- [ ] Issues automáticas se crean
- [ ] Merge automático a test funciona
- [ ] Tests se ejecutan en Etapa 2

---

## 🐛 Solución de Problemas Comunes

### Error: "Modelo no encontrado"

```powershell
# Verificar ubicación
Test-Path ml_model\vulnerability_detector.pkl

# Si no existe, entrenar
python ml_model\model.py
```

### Error: "ModuleNotFoundError: No module named 'sklearn'"

```powershell
# Instalar dependencias
pip install -r requirements.txt
```

### Error: "pytest: command not found"

```powershell
# Instalar pytest
pip install pytest pytest-cov
```

### Error: GitHub Actions falla en "Install dependencies"

- Verificar que `requirements.txt` está en el repositorio
- Verificar que los nombres de paquetes son correctos

### Error: No se crean comentarios en el PR

- Verificar que el workflow tiene permisos:
  - Settings → Actions → General
  - Workflow permissions: "Read and write permissions"

---

## 📊 Qué Esperar en Cada Paso

### Código Vulnerable:
```
🔍 Scanning: test_vulnerable.py
❌ HIGH RISK
   Probability: 95.3%
   Type: SQL Injection
   Recommendation: Use parameterized queries
```

### Código Seguro:
```
🔍 Scanning: test_seguro.py
✅ LOW RISK
   Probability: 12.1%
   Type: None
   Status: Safe
```

### En GitHub Actions:
```
Etapa 1: 🔍 Revisión de Seguridad ML
  ├── ✅ Checkout code
  ├── ✅ Setup Python
  ├── ✅ Install dependencies
  ├── ✅ Get changed files
  ├── ✅ Run ML scan
  └── ❌ Code VULNERABLE → BLOCK

(Si vulnerable se detiene aquí)

(Si seguro continúa:)
Etapa 2: 🔀 Merge a Test + Pruebas
  ├── ✅ Merge dev → test
  ├── ✅ Run tests
  └── ✅ All tests passed

Etapa 3: 🚀 Deploy
  ├── ✅ Merge test → main
  ├── ⚠️ Build Docker (puede fallar sin secrets)
  └── ⚠️ Deploy (puede fallar sin secrets)
```

---

## 🎯 Próximos Pasos (Opcional)

Una vez que hayas verificado que todo funciona:

1. **Configurar Telegram** (10 min):
   - Ver `TELEGRAM_SETUP.md`
   - Agregar secrets en GitHub

2. **Configurar Despliegue** (10 min):
   - Crear cuenta en Railway/Render
   - Agregar secrets de deployment

3. **Tomar Capturas** (5 min):
   - PR rechazado por vulnerabilidad
   - PR aprobado con código seguro
   - Pipeline completo ejecutándose
   - App desplegada

---

## 📝 Resumen

**Lo que funciona SIN Telegram**:
- ✅ Detección de vulnerabilidades con ML
- ✅ Escaneo de código local
- ✅ Escaneo en GitHub Actions
- ✅ Comentarios automáticos en PRs
- ✅ Creación de issues automáticas
- ✅ Etiquetas automáticas
- ✅ Merge automático
- ✅ Ejecución de tests
- ✅ Generación de reportes

**Lo que NO funciona sin Telegram**:
- ❌ Notificaciones en Telegram (obvio)

**Lo que puede fallar sin otros secrets**:
- ⚠️ Despliegue a producción (necesita DOCKER_USERNAME, RAILWAY_TOKEN, etc.)

Pero el **core del proyecto funciona al 100%** sin Telegram! 🎉

---

## 🆘 ¿Necesitas Ayuda?

Si algo no funciona:

1. Verificar logs en GitHub Actions
2. Revisar que las ramas existen
3. Confirmar que el modelo está entrenado
4. Verificar permisos del workflow en GitHub

**Comando útil para debug**:
```powershell
# Ver logs detallados
python scripts\vulnerability_scanner.py test_vulnerable.py --verbose
```

---

¡Listo! Ahora puedes probar todo el pipeline sin necesidad de configurar Telegram. 🚀
