# 📱 Guía de Configuración del Bot de Telegram

## Paso 1: Crear tu Bot de Telegram

### 1.1 Hablar con BotFather

1. Abre Telegram y busca: **@BotFather**
2. Inicia conversación con `/start`
3. Crea un nuevo bot: `/newbot`
4. Proporciona un nombre: `Vulnerability Scanner Bot`
5. Proporciona un username único: `mi_proyecto_cicd_bot` (debe terminar en `_bot`)

### 1.2 Obtener el Token

Después de crear el bot, BotFather te dará un **token** como este:

```
123456789:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890
```

**⚠️ GUARDA ESTE TOKEN - LO NECESITARÁS MÁS ADELANTE**

### 1.3 Configurar tu Bot

Envía estos comandos a BotFather para configurar tu bot:

```
/setdescription
# Descripción: Bot para notificaciones del pipeline CI/CD de seguridad

/setabouttext
# About: Sistema automatizado de detección de vulnerabilidades con ML

/setuserpic
# Opcional: Sube una imagen para tu bot
```

---

## Paso 2: Obtener tu Chat ID

### 2.1 Iniciar conversación con tu bot

1. Busca tu bot en Telegram usando el username que creaste
2. Presiona **START** o envía `/start`
3. Envía cualquier mensaje, por ejemplo: `Hola`

### 2.2 Obtener el Chat ID

Método 1 - Usando API de Telegram:
```bash
# Reemplaza <TU_TOKEN> con el token de tu bot
curl https://api.telegram.org/bot<TU_TOKEN>/getUpdates
```

Busca en la respuesta JSON el campo `"chat":{"id":123456789}`

Método 2 - Usando bot auxiliar:
1. Busca en Telegram: **@userinfobot**
2. Envía `/start`
3. Te mostrará tu Chat ID

### 2.3 Para Canal o Grupo (opcional)

Si quieres notificaciones en un grupo:

1. Crea un grupo en Telegram
2. Agrega tu bot al grupo como administrador
3. Usa el método del curl para obtener el Chat ID del grupo
4. El Chat ID de grupos empieza con `-` (ejemplo: `-1001234567890`)

---

## Paso 3: Configurar GitHub Secrets

### 3.1 Ir a Configuración del Repositorio

1. Ve a tu repositorio en GitHub
2. Click en **Settings** (Configuración)
3. En el menú izquierdo: **Secrets and variables** → **Actions**
4. Click en **New repository secret**

### 3.2 Agregar TELEGRAM_BOT_TOKEN

```
Name: TELEGRAM_BOT_TOKEN
Value: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890
```

Click en **Add secret**

### 3.3 Agregar TELEGRAM_CHAT_ID

```
Name: TELEGRAM_CHAT_ID
Value: 123456789
```

(o `-1001234567890` si es un grupo)

Click en **Add secret**

---

## Paso 4: Configurar Secrets Adicionales para Despliegue

### 4.1 Docker Hub (requerido para despliegue)

```
Name: DOCKER_USERNAME
Value: tu_usuario_dockerhub

Name: DOCKER_PASSWORD
Value: tu_password_o_access_token_dockerhub
```

### 4.2 Railway (si usas Railway para despliegue)

```
Name: RAILWAY_TOKEN
Value: tu_token_de_railway

Name: DEPLOYMENT_URL
Value: https://tu-app.railway.app
```

Obtener token de Railway:
1. Ve a https://railway.app
2. Click en tu perfil → Account Settings
3. Tokens → Create New Token
4. Copia el token

### 4.3 Render (alternativa a Railway)

```
Name: RENDER_API_KEY
Value: tu_api_key_de_render

Name: RENDER_SERVICE_ID
Value: srv-xxxxxxxxxxxxx

Name: DEPLOYMENT_URL
Value: https://tu-app.onrender.com
```

Obtener API Key de Render:
1. Ve a https://render.com
2. Dashboard → Account Settings
3. API Keys → Create API Key

---

## Paso 5: Crear Ramas Requeridas

### 5.1 Crear ramas obligatorias

```bash
# Asegúrate de estar en main
git checkout main

# Crear rama dev
git checkout -b dev
git push origin dev

# Crear rama test
git checkout -b test
git push origin test

# Volver a main
git checkout main
```

### 5.2 Configurar Branch Protection Rules

#### Para rama `test`:

1. Settings → Branches → Add branch protection rule
2. Branch name pattern: `test`
3. ✅ Require pull request reviews before merging
4. ✅ Require status checks to pass before merging
   - Buscar y agregar: `security-scan`
5. Save changes

#### Para rama `main`:

1. Add branch protection rule
2. Branch name pattern: `main`
3. ✅ Require pull request reviews before merging
4. ✅ Require status checks to pass before merging
   - Agregar: `security-scan`, `merge-to-test`, `deploy-to-production`
5. Save changes

---

## Paso 6: Probar las Notificaciones

### 6.1 Test Local

```bash
# Exportar variables de entorno
export TELEGRAM_BOT_TOKEN="tu_token"
export TELEGRAM_CHAT_ID="tu_chat_id"

# Probar notificación de escaneo
python scripts/telegram_notifier.py --type scan_start --repo "test-repo" --branch "dev"

# Probar notificación de vulnerabilidad
python scripts/telegram_notifier.py --type vulnerable --repo "test-repo" --branch "dev" --pr 1

# Probar notificación de código seguro
python scripts/telegram_notifier.py --type secure --repo "test-repo" --branch "dev" --pr 1

# Probar notificación de despliegue exitoso
python scripts/telegram_notifier.py --type deploy_success --repo "test-repo" --url "https://app.com"
```

Deberías recibir mensajes en Telegram para cada comando.

### 6.2 Test en GitHub Actions

1. Crea una rama de prueba:
```bash
git checkout dev
echo "# Test" >> test_file.py
git add test_file.py
git commit -m "test: probar notificaciones Telegram"
git push origin dev
```

2. Crea un Pull Request de `dev` → `test`

3. Observa:
   - Los mensajes de Telegram
   - Los comentarios en el PR
   - Los jobs del workflow en GitHub Actions

---

## Paso 7: Entrenar el Modelo (IMPORTANTE)

### 7.1 Entrenar el modelo localmente

```bash
# Opción 1: Usar Jupyter Notebook (recomendado)
jupyter notebook train_detector.ipynb
# Ejecuta todas las celdas

# Opción 2: Desde línea de comandos
python ml_model/model.py
```

Esto generará: `ml_model/vulnerability_detector.pkl`

### 7.2 Subir el modelo al repositorio

```bash
git add ml_model/vulnerability_detector.pkl
git commit -m "feat: agregar modelo entrenado"
git push origin main
```

**⚠️ El pipeline NO FUNCIONARÁ sin el modelo entrenado**

---

## Paso 8: Flujo de Trabajo Completo

### 8.1 Desarrollo Normal

```bash
# 1. Trabajar en rama dev
git checkout dev
# ... hacer cambios ...
git add .
git commit -m "feat: nueva funcionalidad"
git push origin dev

# 2. Crear Pull Request: dev → test
# Ve a GitHub y crea el PR

# 3. El pipeline se activa automáticamente:
#    ✅ Etapa 1: Revisión de seguridad ML
#    ✅ Etapa 2: Merge a test + Pruebas
#    ✅ Etapa 3: Merge a main + Despliegue

# 4. Recibir notificaciones en Telegram en cada etapa
```

### 8.2 Si se detecta vulnerabilidad

```bash
# 1. Recibirás notificación Telegram: "VULNERABILIDAD DETECTADA"
# 2. El PR se marcará como rechazado
# 3. Se agregará etiqueta "fixing-required"
# 4. Se creará una issue automática

# 5. Corregir el código vulnerable
git checkout dev
# ... corregir código ...
git add .
git commit -m "fix: corregir vulnerabilidad SQL injection"
git push origin dev

# 6. El pipeline se ejecuta automáticamente de nuevo
```

---

## 📸 Capturas para el README

Toma las siguientes capturas de pantalla:

1. **Bot de Telegram**:
   - Conversación con BotFather mostrando el bot creado
   - Mensajes de notificación en acción

2. **GitHub Secrets**:
   - Lista de secrets configurados (sin mostrar valores)

3. **Pull Request**:
   - PR con código vulnerable rechazado
   - PR con código seguro aprobado
   - Comentarios automáticos del bot

4. **Workflow ejecutándose**:
   - Las 3 etapas en ejecución
   - Checks completados exitosamente

5. **Aplicación desplegada**:
   - Captura de la app en producción
   - URL funcionando

---

## ❓ Troubleshooting

### Error: "TELEGRAM_BOT_TOKEN no configurado"

- Verifica que agregaste el secret en GitHub
- El nombre debe ser exactamente: `TELEGRAM_BOT_TOKEN`

### Error: "Chat not found"

- Asegúrate de haber enviado al menos 1 mensaje al bot
- Verifica que el Chat ID sea correcto
- Si es grupo, asegúrate de que el bot sea administrador

### Error: "Modelo no encontrado"

- Entrena el modelo: `jupyter notebook train_detector.ipynb`
- Sube el .pkl al repositorio
- Verifica la ruta: `ml_model/vulnerability_detector.pkl`

### No recibo notificaciones

```bash
# Test manual
curl "https://api.telegram.org/bot<TU_TOKEN>/sendMessage?chat_id=<TU_CHAT_ID>&text=Test"
```

Si este comando funciona, el problema está en GitHub Secrets.

---

## 📚 Referencias

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Railway Deployment](https://railway.app/docs)
- [Render Deployment](https://render.com/docs)

---

## ✅ Checklist Final

- [ ] Bot de Telegram creado
- [ ] Token del bot obtenido
- [ ] Chat ID obtenido
- [ ] Secrets configurados en GitHub
- [ ] Ramas dev, test, main creadas
- [ ] Branch protection rules configuradas
- [ ] Modelo ML entrenado y subido
- [ ] Test local de notificaciones exitoso
- [ ] PR de prueba ejecutado correctamente
- [ ] Aplicación desplegada en producción
- [ ] Capturas de pantalla tomadas
- [ ] README actualizado con enlaces

¡Tu pipeline CI/CD está listo! 🚀
