# Sistema de Detección de Vulnerabilidades con Machine Learning

**Escáner de vulnerabilidades basado en Machine Learning para código Python y JavaScript**

## Inicio Rápido

### 1. Entrenar el Modelo
```bash
# Abrir y ejecutar el notebook de entrenamiento:
train_detector.ipynb
```
Tiempo de entrenamiento: 30min a 1 hora utilizando 84,588 muestras reales CVE/CWE (Python + JavaScript)

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
train_detector.ipynb              Notebook de entrenamiento (5 celdas)
Dataset/
  ├── data_Python.csv             Vulnerabilidades Python (2,316 muestras)
  └── data_JavaScript.csv         Vulnerabilidades JavaScript (~42K muestras)
ml_model/
  ├── model.py                    Implementación Random Forest
  └── vulnerability_detector.pkl  Modelo entrenado
scripts/
  ├── code_analyzer.py            Extracción de características AST (27 características)
  ├── vulnerability_scanner.py    Motor principal de escaneo
  └── report_generator.py         Generación de reportes HTML
tests/
  ├── vulnerable_code_example.py  Casos de prueba Python
  ├── secure_code_example.py
  ├── vulnerable_code_js.js       Casos de prueba JavaScript
  └── secure_code_js.js
```

---

## Integración CI/CD

Flujo de trabajo de GitHub Actions incluido en `.github/workflows/security-scan.yml`

**Comportamiento**:
- Se ejecuta automáticamente en cada push/pull request
- Escanea todos los archivos Python y JavaScript
- Falla el pipeline si detecta vulnerabilidades con probabilidad >= 70%

---

## Ejemplos de Uso

### Escanear un Archivo Individual
```bash
python scripts/vulnerability_scanner.py tests/vulnerable_code_example.py
```

**Salida**:
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

### Escanear un Directorio
```bash
python scripts/vulnerability_scanner.py src/
```

**Salida**:
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

## Proceso de Entrenamiento

El pipeline de entrenamiento consiste en 5 pasos:

1. **Cargar Datasets**: Combina datos CVE/CWE de Python y JavaScript
2. **Extraer Características**: Analiza tanto código vulnerable como parches (código seguro)
3. **Entrenar Modelo**: Ajusta Random Forest con 84,588 muestras
4. **Validar**: Validación cruzada con 5 folds
5. **Guardar Modelo**: Persiste el modelo entrenado en `vulnerability_detector.pkl`

Ejecutar todas las celdas en `train_detector.ipynb` para reentrenar el modelo.

---

## Detalles Técnicos

**Extracción de Características**:
- Análisis AST (Abstract Syntax Tree)
- Análisis estático de código
- Coincidencia de patrones para vulnerabilidades conocidas
- Métricas de complejidad de código

**Evaluación de Riesgo**:
- CRÍTICO: >= 90% probabilidad
- ALTO: 70-89% probabilidad
- MEDIO: 40-69% probabilidad
- BAJO: < 40% probabilidad

**Umbral**: 70% de probabilidad (configurable mediante parámetro `--threshold`)

---

## Proyecto Académico

Laboratorio: Seguridad Informática y Modernización de Aplicaciones  
Enfoque: Machine Learning para Detección Automatizada de Vulnerabilidades  
Fuente de Dataset: Bases de datos reales CVE/CWE de vulnerabilidades
