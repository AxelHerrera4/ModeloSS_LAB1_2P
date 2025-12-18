# 🚀 Guía Rápida - Comandos Esenciales

## ⚡ Setup Inicial (5 minutos)

### 1. Configurar Bot de Telegram

```bash
# 1. Abrir Telegram y buscar: @BotFather
# 2. Enviar: /newbot
# 3. Copiar el TOKEN que te da
# 4. Iniciar conversación con tu bot y enviar cualquier mensaje
# 5. Obtener tu Chat ID:
curl https://api.telegram.org/bot<TU_TOKEN>/getUpdates
# Buscar "chat":{"id":123456789}
```

### 2. Configurar GitHub Secrets

```bash
# Ir a: https://github.com/TU_USUARIO/TU_REPO/settings/secrets/actions
# Click: "New repository secret"
#
# Agregar estos 6 secrets:
# 1. TELEGRAM_BOT_TOKEN → tu token del paso 1
# 2. TELEGRAM_CHAT_ID → tu chat id del paso 1
# 3. DOCKER_USERNAME → tu usuario de Docker Hub
# 4. DOCKER_PASSWORD → tu password de Docker Hub
# 5. RAILWAY_TOKEN → token de Railway (opcional)
# 6. DEPLOYMENT_URL → URL donde se desplegará (ej: https://app.railway.app)
```

### 3. Crear Ramas Requeridas

```bash
# Clonar el repo
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO

# Crear y subir rama dev
git checkout -b dev
git push origin dev

# Crear y subir rama test
git checkout main
git checkout -b test
git push origin test

# Volver a main
git checkout main
```

### 4. Configurar Branch Protection

```bash
# Ir a: Settings → Branches → Add branch protection rule
#
# Para rama "test":
# ✅ Require pull request reviews before merging
# ✅ Require status checks to pass: "security-scan"
# Save
#
# Para rama "main":
# ✅ Require pull request reviews before merging
# ✅ Require status checks to pass: "security-scan", "merge-to-test"
# Save
```

---

## 🧪 Entrenar el Modelo (15-30 min)

```bash
# Opción 1: Jupyter Notebook (recomendado)
jupyter notebook train_detector.ipynb
# Ejecutar todas las celdas (Run All)
# Esperar a que termine el entrenamiento

# Opción 2: Script directo
python ml_model/model.py

# Verificar que se generó el modelo
ls -lh ml_model/vulnerability_detector.pkl

# Subir el modelo al repo
git add ml_model/vulnerability_detector.pkl
git commit -m "feat: agregar modelo entrenado"
git push origin main
```

---

## 🚀 Probar el Pipeline (2 minutos)

### Test Local de Telegram

```bash
# Exportar variables
export TELEGRAM_BOT_TOKEN="tu_token"
export TELEGRAM_CHAT_ID="tu_chat_id"

# Test de notificación
python scripts/telegram_notifier.py \
  --type scan_start \
  --repo "test-repo" \
  --branch "dev"

# Deberías recibir un mensaje en Telegram
```

### Test Completo del Pipeline

```bash
# 1. Ir a rama dev
git checkout dev

# 2. Crear archivo de prueba
cat > test_app.py << 'EOF'
def suma(a, b):
    """Función segura para sumar dos números"""
    return a + b

def multiplicar(x, y):
    """Función segura para multiplicar"""
    return x * y
EOF

# 3. Commit y push
git add test_app.py
git commit -m "test: probar pipeline CI/CD"
git push origin dev

# 4. Crear Pull Request en GitHub:
# - Base: test
# - Compare: dev
# - Title: "Test del pipeline"
# - Create pull request

# 5. Observar:
# ✅ GitHub Actions ejecutándose
# ✅ Notificaciones llegando a Telegram
# ✅ Comentarios automáticos en el PR
```

---

## 🔍 Escaneo Local (testing)

### Escanear un archivo

```bash
# Escanear archivo individual
python scripts/vulnerability_scanner.py tests/vulnerable_code_example.py

# Ver reporte
python -m http.server 8000
# Abrir: http://localhost:8000/reports/scan_results.html
```

### Escanear directorio

```bash
# Escanear todo el directorio scripts/
python scripts/vulnerability_scanner.py scripts/

# Con threshold personalizado
python scripts/vulnerability_scanner.py scripts/ --threshold 0.60
```

### Escanear solo archivos modificados

```bash
# Simular detección de cambios
python scripts/get_changed_files.py \
  --base origin/main \
  --head HEAD \
  --output changed.json

# Escanear solo esos archivos
python scripts/vulnerability_scanner.py --files-list changed.json
```

---

## 🐳 Docker Local

### Build y Run

```bash
# Build de la imagen
docker build -t vulnerability-scanner .

# Ejecutar contenedor
docker run -p 8080:8080 vulnerability-scanner

# Test de la API
curl http://localhost:8080/health

# Escanear código vía API
curl -X POST http://localhost:8080/scan \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def suma(a, b): return a + b",
    "language": "python"
  }'
```

### Docker Compose

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

---

## 🚀 Despliegue a Producción

### Railway

```bash
# Instalar CLI
npm install -g @railway/cli

# Login
railway login

# Inicializar proyecto
railway init

# Obtener token
railway whoami --token
# Copiar el token y agregarlo como RAILWAY_TOKEN en GitHub Secrets

# Deploy manual (opcional)
railway up
```

### Render

```bash
# 1. Ir a https://render.com
# 2. New → Web Service
# 3. Connect repository
# 4. Configuración:
#    - Environment: Docker
#    - Branch: main
#    - Dockerfile path: ./Dockerfile
# 5. Create Web Service
# 6. Copiar API Key:
#    - Account Settings → API Keys → Create
#    - Agregar como RENDER_API_KEY en GitHub Secrets
```

### Fly.io

```bash
# Instalar flyctl
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch
fly launch --config fly.toml

# Deploy
fly deploy

# Ver app
fly open
```

---

## 🧪 Tests

### Ejecutar todos los tests

```bash
# Instalar pytest
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=scripts --cov=ml_model --cov-report=html

# Abrir reporte de cobertura
open htmlcov/index.html  # Mac
start htmlcov/index.html # Windows
```

### Test específico

```bash
# Test individual
pytest tests/test_scanner.py::TestCodeAnalyzer::test_detect_sql_injection_python -v

# Tests de una clase
pytest tests/test_scanner.py::TestCodeAnalyzer -v
```

---

## 📊 Ver Resultados del Modelo

```bash
# Abrir notebook
jupyter notebook train_detector.ipynb

# O ver directamente en el código
python -c "
import pickle
with open('ml_model/vulnerability_detector.pkl', 'rb') as f:
    model = pickle.load(f)
    print(f'Features: {len(model.feature_names)}')
    print(f'Entrenado: {model.is_trained}')
"
```

---

## 🔧 Debugging

### Ver logs de GitHub Actions

```bash
# En GitHub:
# Actions → Seleccionar workflow → Seleccionar job → Ver logs

# O instalar GitHub CLI:
gh auth login
gh run list
gh run view <RUN_ID>
```

### Ver logs locales

```bash
# Logs detallados del scanner
python scripts/vulnerability_scanner.py tests/ --verbose

# Debug del modelo
python -c "
from ml_model.model import VulnerabilityPredictor
predictor = VulnerabilityPredictor('ml_model/vulnerability_detector.pkl')
print(f'Modelo cargado: {predictor.is_trained}')
print(f'Features: {predictor.feature_names}')
"
```

### Test de Telegram

```bash
# Test directo con curl
curl -X POST "https://api.telegram.org/bot<TU_TOKEN>/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "<TU_CHAT_ID>",
    "text": "Test desde curl"
  }'
```

---

## 📝 Comandos Git Comunes

### Flujo normal de desarrollo

```bash
# Actualizar dev
git checkout dev
git pull origin dev

# Crear feature
# ... hacer cambios ...
git add .
git commit -m "feat: descripción del cambio"
git push origin dev

# Crear PR en GitHub: dev → test
```

### Corregir vulnerabilidad detectada

```bash
# El PR fue rechazado por vulnerabilidad
git checkout dev

# Corregir el código
# ... editar archivos ...

git add .
git commit -m "fix: corregir vulnerabilidad SQL injection"
git push origin dev

# El pipeline se ejecuta automáticamente de nuevo
```

### Sincronizar ramas

```bash
# Traer cambios de test a dev
git checkout dev
git merge origin/test
git push origin dev

# Traer cambios de main a test
git checkout test
git merge origin/main
git push origin test
```

---

## 🎯 Checklist Pre-Demostración

```bash
# 1. Verificar modelo entrenado
ls -lh ml_model/vulnerability_detector.pkl

# 2. Verificar secrets configurados
# GitHub → Settings → Secrets → Actions
# Debe haber: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, DOCKER_USERNAME, etc.

# 3. Test local Telegram
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_CHAT_ID="..."
python scripts/telegram_notifier.py --type scan_start --repo "test" --branch "dev"

# 4. Test del modelo
python scripts/vulnerability_scanner.py tests/vulnerable_code_example.py

# 5. Crear PR de prueba
git checkout dev
echo "# Test" >> test.py
git add test.py
git commit -m "test: demo"
git push origin dev
# Crear PR: dev → test

# 6. Verificar despliegue
curl https://tu-app.railway.app/health
```

---

## 🆘 Comandos de Emergencia

### Resetear rama

```bash
# Si algo salió mal en dev
git checkout dev
git reset --hard origin/main
git push origin dev --force
```

### Limpiar workflow fallido

```bash
# En GitHub Actions, cancelar workflow en ejecución
# O esperar que termine y crear nuevo PR
```

### Re-entrenar modelo rápido

```bash
# Script de entrenamiento rápido
python ml_model/model.py

# Verificar
ls -lh ml_model/vulnerability_detector.pkl

# Subir
git add ml_model/vulnerability_detector.pkl
git commit -m "chore: re-entrenar modelo"
git push origin main
```

---

## 📚 Enlaces Útiles

```bash
# Repositorio
https://github.com/TU_USUARIO/TU_REPO

# Actions
https://github.com/TU_USUARIO/TU_REPO/actions

# Settings → Secrets
https://github.com/TU_USUARIO/TU_REPO/settings/secrets/actions

# Railway Dashboard
https://railway.app/dashboard

# Docker Hub
https://hub.docker.com/

# Telegram Bot API
https://api.telegram.org/bot<TU_TOKEN>/getUpdates
```

---

## ⏱️ Tiempos Estimados

| Tarea | Tiempo |
|-------|--------|
| Setup inicial completo | 10 min |
| Entrenar modelo | 15-30 min |
| Primer test del pipeline | 2 min |
| Deploy a Railway | 5 min |
| Tomar capturas | 5 min |
| **TOTAL** | **~40 min** |

---

## 🎤 Para la Exposición (8-12 min)

### Demostración 1: Código Vulnerable (4 min)

```bash
# 1. Crear archivo vulnerable
cat > demo_vuln.py << 'EOF'
import sqlite3
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()
EOF

# 2. Push
git checkout dev
git add demo_vuln.py
git commit -m "demo: código vulnerable"
git push origin dev

# 3. Crear PR: dev → test

# 4. Mostrar en pantalla:
# ✅ GitHub Actions ejecutándose
# ✅ Notificación Telegram: "VULNERABILIDAD DETECTADA"
# ✅ PR rechazado con comentario
# ✅ Issue creada automáticamente
# ✅ Etiqueta "fixing-required"
```

### Demostración 2: Código Seguro (6 min)

```bash
# 1. Corregir el código
cat > demo_safe.py << 'EOF'
import sqlite3
def get_user(user_id: int):
    query = "SELECT * FROM users WHERE id = ?"
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    return cursor.fetchall()
EOF

# 2. Push
git add demo_safe.py
git rm demo_vuln.py
git commit -m "fix: usar query parametrizada"
git push origin dev

# 3. Observar pipeline completo:
# ✅ Etapa 1: Seguridad ML → APROBADO
# ✅ Etapa 2: Merge a test → Pruebas EXITOSAS
# ✅ Etapa 3: Merge a main → Despliegue EXITOSO
# ✅ Notificaciones Telegram en cada etapa
# ✅ Aplicación en producción

# 4. Abrir app desplegada
curl https://tu-app.railway.app/health
```

### Mostrar (2 min)

1. ✅ Modelo entrenado con 94.56% accuracy
2. ✅ Dataset de 84,588 muestras
3. ✅ 27 features extraídas
4. ✅ Notificaciones Telegram funcionando
5. ✅ App desplegada en producción
6. ✅ Branch protection configurado

---

**¡Listo para la demo! 🚀**
