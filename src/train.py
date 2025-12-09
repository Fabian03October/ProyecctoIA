"""
Sistema de Detección y Localización 3D para Asistencia Visual
Fase II: Entrenamiento del Modelo YOLO

Autor: Equipo de Desarrollo
Descripción: Sistema de detección de objetos usando YOLOv8 con capacidad de
            estimación de distancia mediante visión estéreo (2 cámaras)
"""

from ultralytics import YOLO
import torch
import os
from pathlib import Path

# Verificar disponibilidad de GPU
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"🖥️  Dispositivo de entrenamiento: {device}")

# Configuración de rutas
PROJECT_ROOT = Path(__file__).parent.parent
DATA_YAML = PROJECT_ROOT / "data.yaml"
MODELS_DIR = PROJECT_ROOT / "models"
RESULTS_DIR = PROJECT_ROOT / "results"

# Crear directorios si no existen
MODELS_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

def train_yolo_model(
    model_size='n',  # opciones: 'n' (nano), 's' (small), 'm' (medium), 'l' (large)
    epochs=50,
    batch_size=16,
    img_size=640,
    learning_rate=0.01,
    experiment_name='exp1'
):
    """
    Entrena un modelo YOLOv8 usando Transfer Learning
    
    Args:
        model_size: Tamaño del modelo ('n', 's', 'm', 'l')
        epochs: Número de épocas de entrenamiento
        batch_size: Tamaño del batch
        img_size: Tamaño de imagen de entrada
        learning_rate: Tasa de aprendizaje
        experiment_name: Nombre del experimento
    """
    
    print(f"\n{'='*60}")
    print(f"🚀 Iniciando entrenamiento: {experiment_name}")
    print(f"{'='*60}")
    print(f"📊 Configuración:")
    print(f"   - Modelo: YOLOv8{model_size}")
    print(f"   - Épocas: {epochs}")
    print(f"   - Batch size: {batch_size}")
    print(f"   - Tamaño imagen: {img_size}")
    print(f"   - Learning rate: {learning_rate}")
    print(f"{'='*60}\n")
    
    # Cargar modelo pre-entrenado (Transfer Learning)
    model = YOLO(f'yolov8{model_size}.pt')
    
    # Entrenar modelo
    results = model.train(
        data=str(DATA_YAML),
        epochs=epochs,
        imgsz=img_size,
        batch=batch_size,
        lr0=learning_rate,
        device=device,
        project=str(RESULTS_DIR),
        name=experiment_name,
        patience=20,  # Early stopping
        save=True,
        save_period=10,  # Guardar checkpoint cada 10 épocas
        plots=True,  # Generar gráficas de entrenamiento
        verbose=True,
        workers=4,
        amp=True,  # Automatic Mixed Precision
    )
    
    print(f"\n✅ Entrenamiento completado: {experiment_name}")
    print(f"📁 Resultados guardados en: {RESULTS_DIR / experiment_name}")
    
    return results

def validate_model(model_path, experiment_name='validation'):
    """
    Valida el modelo entrenado
    """
    print(f"\n🔍 Validando modelo: {model_path}")
    
    model = YOLO(model_path)
    metrics = model.val(
        data=str(DATA_YAML),
        project=str(RESULTS_DIR),
        name=experiment_name
    )
    
    print(f"\n📈 Métricas de Validación:")
    print(f"   - mAP50: {metrics.box.map50:.4f}")
    print(f"   - mAP50-95: {metrics.box.map:.4f}")
    print(f"   - Precision: {metrics.box.mp:.4f}")
    print(f"   - Recall: {metrics.box.mr:.4f}")
    
    return metrics

if __name__ == "__main__":
    
    # EXPERIMENTO 1: Modelo pequeño, configuración estándar
    print("\n" + "="*60)
    print("EXPERIMENTO 1: Configuración Base")
    print("="*60)
    
    results_exp1 = train_yolo_model(
        model_size='s',      # Small model
        epochs=50,
        batch_size=16,
        img_size=640,
        learning_rate=0.01,
        experiment_name='exp1_base'
    )
    
    # EXPERIMENTO 2: Ajuste de hiperparámetros
    print("\n" + "="*60)
    print("EXPERIMENTO 2: Learning Rate Reducido")
    print("="*60)
    
    results_exp2 = train_yolo_model(
        model_size='s',
        epochs=50,
        batch_size=16,
        img_size=640,
        learning_rate=0.005,  # Learning rate más bajo
        experiment_name='exp2_lr_bajo'
    )
    
    # EXPERIMENTO 3 (OPCIONAL): Modelo más grande
    print("\n" + "="*60)
    print("EXPERIMENTO 3: Modelo Medium (Opcional)")
    print("="*60)
    
    try:
        results_exp3 = train_yolo_model(
            model_size='m',      # Medium model
            epochs=50,
            batch_size=8,        # Batch más pequeño para modelo más grande
            img_size=640,
            learning_rate=0.01,
            experiment_name='exp3_medium'
        )
    except Exception as e:
        print(f"⚠️  Experimento 3 omitido: {e}")
    
    print("\n" + "="*60)
    print("✅ TODOS LOS EXPERIMENTOS COMPLETADOS")
    print("="*60)
    print(f"\n📊 Revisa los resultados en: {RESULTS_DIR}")
    print("📈 Compara las métricas mAP50 y mAP50-95 para seleccionar el mejor modelo")