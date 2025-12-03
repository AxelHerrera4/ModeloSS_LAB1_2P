# 🛡️ Detector de Vulnerabilidades ML

**Tu propio detector de vulnerabilidades usando Machine Learning**

## ⚡ Inicio Rápido

### 1. Entrenar modelo (una sola vez)
```bash
# Abre el notebook:
train_detector.ipynb
```
⏱️ Toma 3-4 minutos | Usa 2,316 muestras Python reales

### 2. Escanear código
```bash
python scripts/vulnerability_scanner.py archivo.py
```

### 3. Ver reporte
```bash
python scripts/report_generator.py reports/scan_results.json
start reports/scan_results.html
```

---

## 🎯 ¿Qué detecta?

- ✅ Inyección de código (`eval`, `exec`)
- ✅ Inyección SQL
- ✅ Criptografía débil (MD5, SHA1)
- ✅ Deserialización insegura
- ✅ Secretos hardcodeados
- ✅ Path traversal

---

## 🧠 Modelo

- **Algoritmo**: Random Forest (200 árboles)
- **Features**: 27 características del código AST
- **Dataset**: 2,316 muestras Python con CVE/CWE reales
- **Tiempo**: 3-4 minutos de entrenamiento
- **Accuracy**: ~85-90% (depende del balance del dataset)

---

## 📁 Archivos Importantes

```
train_detector.ipynb       ← ENTRENA EL MODELO (Jupyter Notebook)
Dataset/data_Python.csv    ← 2,316 vulnerabilidades reales
ml_model/model.py          ← Código del Random Forest
scripts/code_analyzer.py   ← Extrae 27 características
scripts/vulnerability_scanner.py  ← Escanea archivos
```

---

## 🚀 CI/CD

GitHub Actions incluido en `.github/workflows/security-scan.yml`
- Se ejecuta automáticamente en cada push
- Falla si detecta vulnerabilidades >= 70%

---

## 📊 Ejemplo de Resultado

```
🚨 VULNERABLE: tests/vulnerable_code_example.py
   Probabilidad: 89.34%
   Patrones detectados: eval(), exec(), input()
```

---

**Proyecto académico - Laboratorio de Seguridad**
