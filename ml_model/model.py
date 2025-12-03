"""
Modelo predictivo de vulnerabilidades usando Random Forest.
Incluye entrenamiento, predicción y generación de datasets sintéticos.
"""

import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from typing import Dict, List, Tuple
import os


class VulnerabilityPredictor:
    """Predictor de vulnerabilidades basado en Random Forest"""
    
    def __init__(self, model_path: str = None):
        """
        Inicializa el predictor
        
        Args:
            model_path: Ruta al modelo pre-entrenado. Si es None, crea uno nuevo.
        """
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            self.model = RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                class_weight='balanced',
                n_jobs=-1
            )
            self.feature_names = []
            self.is_trained = False
    
    def prepare_features(self, features_dict: Dict) -> pd.DataFrame:
        """
        Prepara las características para el modelo
        
        Args:
            features_dict: Diccionario con características extraídas del código
            
        Returns:
            DataFrame con características preparadas
        """
        # Convertir booleanos a enteros
        features = features_dict.copy()
        for key, value in features.items():
            if isinstance(value, bool):
                features[key] = int(value)
        
        df = pd.DataFrame([features])
        
        # Si el modelo está entrenado, asegurar que las columnas coincidan
        if self.is_trained and self.feature_names:
            # Agregar columnas faltantes con valor 0
            for col in self.feature_names:
                if col not in df.columns:
                    df[col] = 0
            # Mantener solo las columnas del modelo
            df = df[self.feature_names]
        
        return df
    
    def train(self, X: pd.DataFrame, y: np.ndarray) -> Dict:
        """
        Entrena el modelo
        
        Args:
            X: DataFrame con características
            y: Array con etiquetas (0: seguro, 1: vulnerable)
            
        Returns:
            Diccionario con métricas de entrenamiento
        """
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Guardar nombres de características
        self.feature_names = list(X.columns)
        
        # Entrenar modelo
        print("Entrenando modelo Random Forest...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluar
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Calcular métricas
        metrics = {
            'accuracy': self.model.score(X_test, y_test),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'classification_report': classification_report(y_test, y_pred, output_dict=True),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'feature_importance': dict(zip(
                self.feature_names,
                self.model.feature_importances_.tolist()
            ))
        }
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X, y, cv=5, scoring='roc_auc')
        metrics['cv_mean'] = cv_scores.mean()
        metrics['cv_std'] = cv_scores.std()
        
        print(f"\nAccuracy: {metrics['accuracy']:.4f}")
        print(f"ROC-AUC: {metrics['roc_auc']:.4f}")
        print(f"Cross-validation: {metrics['cv_mean']:.4f} (+/- {metrics['cv_std']:.4f})")
        
        return metrics
    
    def predict(self, features: pd.DataFrame) -> Tuple[int, float]:
        """
        Predice si el código tiene vulnerabilidades
        
        Args:
            features: DataFrame con características del código
            
        Returns:
            Tupla (predicción, probabilidad) donde:
            - predicción: 0 (seguro) o 1 (vulnerable)
            - probabilidad: probabilidad de vulnerabilidad (0-1)
        """
        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado")
        
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0][1]
        
        return int(prediction), float(probability)
    
    def get_feature_importance(self, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Obtiene las características más importantes
        
        Args:
            top_n: Número de características principales a retornar
            
        Returns:
            Lista de tuplas (nombre_característica, importancia)
        """
        if not self.is_trained:
            return []
        
        importance = list(zip(self.feature_names, self.model.feature_importances_))
        importance.sort(key=lambda x: x[1], reverse=True)
        
        return importance[:top_n]
    
    def save_model(self, filepath: str):
        """Guarda el modelo entrenado"""
        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"Modelo guardado en: {filepath}")
    
    def load_model(self, filepath: str):
        """Carga un modelo pre-entrenado"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.feature_names = model_data['feature_names']
        self.is_trained = model_data['is_trained']
        
        print(f"Modelo cargado desde: {filepath}")


def generate_synthetic_dataset(n_samples: int = 1000) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Genera un dataset sintético para entrenamiento inicial
    
    En producción, esto debe reemplazarse con datos reales de vulnerabilidades.
    Puedes usar datasets como:
    - NIST NVD
    - GitHub Security Advisories
    - OWASP datasets
    - Análisis de código con herramientas como Bandit, SonarQube
    
    Args:
        n_samples: Número de muestras a generar
        
    Returns:
        Tupla (X, y) con características y etiquetas
    """
    np.random.seed(42)
    
    # Generar características
    data = {
        # Métricas básicas
        'total_lines': np.random.randint(10, 1000, n_samples),
        'code_lines': np.random.randint(5, 800, n_samples),
        'comment_lines': np.random.randint(0, 200, n_samples),
        
        # Complejidad
        'num_functions': np.random.randint(0, 50, n_samples),
        'num_classes': np.random.randint(0, 20, n_samples),
        'max_function_complexity': np.random.randint(1, 30, n_samples),
        'avg_function_complexity': np.random.uniform(1, 15, n_samples),
        
        # Patrones de riesgo (más probable en código vulnerable)
        'has_eval': np.random.binomial(1, 0.1, n_samples),
        'has_exec': np.random.binomial(1, 0.08, n_samples),
        'has_input_direct': np.random.binomial(1, 0.15, n_samples),
        'has_sql_concat': np.random.binomial(1, 0.2, n_samples),
        'has_pickle_load': np.random.binomial(1, 0.12, n_samples),
        'has_yaml_unsafe': np.random.binomial(1, 0.05, n_samples),
        
        # Imports peligrosos
        'uses_os_system': np.random.binomial(1, 0.1, n_samples),
        'uses_subprocess_shell': np.random.binomial(1, 0.15, n_samples),
        'uses_deprecated_libs': np.random.binomial(1, 0.1, n_samples),
        
        # Manejo de errores
        'has_bare_except': np.random.binomial(1, 0.2, n_samples),
        'exception_handling_ratio': np.random.uniform(0, 1, n_samples),
        
        # Seguridad web
        'has_hardcoded_secrets': np.random.binomial(1, 0.15, n_samples),
        'has_flask_debug': np.random.binomial(1, 0.05, n_samples),
        'has_unsafe_deserialization': np.random.binomial(1, 0.1, n_samples),
        
        # Patrones de inyección
        'has_format_string_vuln': np.random.binomial(1, 0.1, n_samples),
        'has_command_injection_risk': np.random.binomial(1, 0.12, n_samples),
        'has_path_traversal_risk': np.random.binomial(1, 0.08, n_samples),
        
        # Criptografía
        'uses_weak_crypto': np.random.binomial(1, 0.1, n_samples),
        'uses_hardcoded_key': np.random.binomial(1, 0.08, n_samples),
    }
    
    X = pd.DataFrame(data)
    
    # Generar etiquetas basadas en patrones de riesgo
    # Código es vulnerable si tiene múltiples factores de riesgo
    risk_score = (
        X['has_eval'] * 0.15 +
        X['has_exec'] * 0.15 +
        X['has_sql_concat'] * 0.12 +
        X['has_command_injection_risk'] * 0.12 +
        X['has_hardcoded_secrets'] * 0.1 +
        X['uses_subprocess_shell'] * 0.1 +
        X['has_pickle_load'] * 0.08 +
        X['has_unsafe_deserialization'] * 0.08 +
        X['has_bare_except'] * 0.05 +
        X['uses_weak_crypto'] * 0.05
    )
    
    # Agregar complejidad como factor
    risk_score += (X['max_function_complexity'] / 30) * 0.1
    
    # Convertir a etiquetas binarias con umbral
    threshold = 0.3
    y = (risk_score > threshold).astype(int).values
    
    # Agregar algo de ruido
    noise_indices = np.random.choice(n_samples, size=int(n_samples * 0.05), replace=False)
    y[noise_indices] = 1 - y[noise_indices]
    
    print(f"Dataset generado: {n_samples} muestras")
    print(f"Vulnerables: {y.sum()} ({y.sum()/n_samples*100:.1f}%)")
    print(f"Seguros: {(1-y).sum()} ({(1-y).sum()/n_samples*100:.1f}%)")
    
    return X, y


if __name__ == '__main__':
    # Ejemplo de uso: entrenar modelo con datos sintéticos
    print("Generando dataset sintético...")
    X, y = generate_synthetic_dataset(n_samples=2000)
    
    # Entrenar modelo
    predictor = VulnerabilityPredictor()
    metrics = predictor.train(X, y)
    
    # Guardar modelo
    model_path = os.path.join('ml_model', 'vulnerability_model.pkl')
    predictor.save_model(model_path)
    
    # Mostrar características importantes
    print("\nCaracterísticas más importantes:")
    for feature, importance in predictor.get_feature_importance(top_n=10):
        print(f"  {feature}: {importance:.4f}")
