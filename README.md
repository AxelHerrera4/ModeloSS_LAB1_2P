# Sistema de Detección de Vulnerabilidades con Machine Learning

**Escáner de vulnerabilidades basado en Machine Learning para código Python y JavaScript**

## Inicio Rápido

### 1. Entrenar el Modelo
```bash
# Abrir y ejecutar el notebook de entrenamiento:
train_detector.ipynb
```
Tiempo de entrenamiento: 8-10 minutos utilizando 84,588 muestras reales CVE/CWE (Python + JavaScript)

### 2. Escanear Código
```bash
# Escanear un archivo individual
python scripts/vulnerability_scanner.py <archivo.py|archivo.js>

# Escanear un directorio
python scripts/vulnerability_scanner.py <directorio>
```

### 3. Ver Reporte
```bash
# El reporte HTML se genera automáticamente
start reports/scan_results.html
```

---

## Capacidades de Detección

El sistema detecta los siguientes patrones de vulnerabilidades:

- Inyección de código (`eval`, `exec`)
- Inyección SQL (concatenación de strings en queries)
- Criptografía débil (MD5, SHA1, DES, RC4)
- Deserialización insegura (pickle, YAML)
- Credenciales y secretos hardcodeados
- Vulnerabilidades de path traversal
- Riesgos de inyección de comandos
- Ejecución insegura de subprocesos

---

## Arquitectura del Modelo

**Algoritmo**: Random Forest Classifier

**Configuración**:
- 200 árboles de decisión
- Profundidad máxima: 15 niveles
- Pesos de clase balanceados
- Procesamiento multi-núcleo habilitado

**Características**: 27 características del código basadas en AST extraídas del código fuente

**Dataset**: 84,588 muestras reales de vulnerabilidades
- Python: 2,316 muestras de la base de datos CVE/CWE
- JavaScript: ~42,000 muestras de la base de datos CVE/CWE
- Dataset balanceado: 50% vulnerable, 50% seguro (utilizando código patch)

**Métricas de Rendimiento**:
- Precisión de entrenamiento: 100%
- ROC-AUC: 1.0000
- Validación cruzada: 94.56% ± 9.81%

---

## Estructura del Proyecto

```
train_detector.ipynb              Training notebook (5 cells)
Dataset/
  ├── data_Python.csv             Python vulnerabilities (2,316 samples)
  └── data_JavaScript.csv         JavaScript vulnerabilities (~42K samples)
ml_model/
  ├── model.py                    Random Forest implementation
  └── vulnerability_detector.pkl  Trained model
scripts/
  ├── code_analyzer.py            AST feature extraction (27 features)
  ├── vulnerability_scanner.py    Main scanning engine
  └── report_generator.py         HTML report generation
tests/
  ├── vulnerable_code_example.py  Python test cases
  ├── secure_code_example.py
  ├── vulnerable_code_js.js       JavaScript test cases
  └── secure_code_js.js
```

---

## CI/CD Integration

GitHub Actions workflow included in `.github/workflows/security-scan.yml`

**Behavior**:
- Automatically runs on each push/pull request
- Scans all Python and JavaScript files
- Fails pipeline if vulnerabilities with probability >= 70% are detected

---

## Usage Examples

### Scanning a Single File
```bash
python scripts/vulnerability_scanner.py tests/vulnerable_code_example.py
```

**Output**:
```
ALERTA: tests/vulnerable_code_example.py
   Probabilidad: 99.00%
   Nivel: CRÍTICO
   Factores de riesgo detectados:
      - Uso de eval()
      - Uso de exec()
      - Secretos hardcodeados
      - subprocess con shell=True
```

### Scanning a Directory
```bash
python scripts/vulnerability_scanner.py src/
```

**Output**:
```
Escaneando directorio: src/
Archivos encontrados: 15
   Python (.py): 10
   JavaScript (.js): 5

Total de archivos analizados: 15
Vulnerabilidades detectadas: 3
Archivos de alto riesgo (>70%): 3
```

---

## Training Process

The training pipeline consists of 5 steps:

1. **Load Datasets**: Combines Python and JavaScript CVE/CWE data
2. **Extract Features**: Analyzes both vulnerable code and patches (secure code)
3. **Train Model**: Fits Random Forest with 84,588 samples
4. **Validate**: Cross-validation with 5 folds
5. **Save Model**: Persists trained model to `vulnerability_detector.pkl`

Run all cells in `train_detector.ipynb` to retrain the model.

---

## Technical Details

**Feature Extraction**:
- AST (Abstract Syntax Tree) parsing
- Static code analysis
- Pattern matching for known vulnerabilities
- Code complexity metrics

**Risk Assessment**:
- CRÍTICO: >= 90% probability
- ALTO: 70-89% probability
- MEDIO: 40-69% probability
- BAJO: < 40% probability

**Threshold**: 70% probability (configurable via `--threshold` parameter)

---

## Academic Project

Laboratory: Computer Security and Application Modernization  
Focus: Machine Learning for Automated Vulnerability Detection  
Dataset Source: Real CVE/CWE vulnerability databases
