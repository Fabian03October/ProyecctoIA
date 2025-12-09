"""
Utilidades para preparación del Dataset
Organiza imágenes y etiquetas en train/val/test
"""

import os
import shutil
import random
from pathlib import Path

def organizar_dataset(
    source_images_dir,
    source_labels_dir,
    dest_root,
    train_ratio=0.8,
    val_ratio=0.1,
    test_ratio=0.1
):
    """
    Organiza imágenes y etiquetas en carpetas train/val/test
    
    Args:
        source_images_dir: Directorio con todas las imágenes
        source_labels_dir: Directorio con todas las etiquetas (.txt)
        dest_root: Directorio raíz de destino
        train_ratio: Proporción para entrenamiento (default: 0.8)
        val_ratio: Proporción para validación (default: 0.1)
        test_ratio: Proporción para prueba (default: 0.1)
    """
    
    print("📂 Organizando dataset...")
    print(f"   Origen imágenes: {source_images_dir}")
    print(f"   Origen etiquetas: {source_labels_dir}")
    print(f"   Destino: {dest_root}")
    print(f"   División: Train {train_ratio*100}% | Val {val_ratio*100}% | Test {test_ratio*100}%")
    
    # Crear estructura de directorios
    for split in ['train', 'val', 'test']:
        Path(dest_root) / 'images' / split).mkdir(parents=True, exist_ok=True)
        (Path(dest_root) / 'labels' / split).mkdir(parents=True, exist_ok=True)
    
    # Obtener lista de imágenes
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    images = []
    
    for ext in image_extensions:
        images.extend(list(Path(source_images_dir).glob(f'*{ext}')))
        images.extend(list(Path(source_images_dir).glob(f'*{ext.upper()}')))
    
    print(f"\n📊 Total de imágenes encontradas: {len(images)}")
    
    if len(images) == 0:
        print("❌ No se encontraron imágenes")
        return
    
    # Filtrar solo imágenes que tengan etiqueta correspondiente
    valid_images = []
    for img in images:
        label_path = Path(source_labels_dir) / f"{img.stem}.txt"
        if label_path.exists():
            valid_images.append(img)
    
    print(f"✅ Imágenes con etiquetas: {len(valid_images)}")
    
    if len(valid_images) < len(images):
        print(f"⚠️  {len(images) - len(valid_images)} imágenes sin etiqueta (serán ignoradas)")
    
    # Mezclar aleatoriamente
    random.shuffle(valid_images)
    
    # Calcular índices de división
    total = len(valid_images)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)
    
    splits = {
        'train': valid_images[:train_end],
        'val': valid_images[train_end:val_end],
        'test': valid_images[val_end:]
    }
    
    # Copiar archivos
    for split, images_list in splits.items():
        print(f"\n📁 Copiando {split}: {len(images_list)} imágenes")
        
        for img_path in images_list:
            # Copiar imagen
            dest_img = Path(dest_root) / 'images' / split / img_path.name
            shutil.copy2(img_path, dest_img)
            
            # Copiar etiqueta
            label_src = Path(source_labels_dir) / f"{img_path.stem}.txt"
            dest_label = Path(dest_root) / 'labels' / split / f"{img_path.stem}.txt"
            shutil.copy2(label_src, dest_label)
    
    print("\n✅ Dataset organizado correctamente")
    print(f"\n📊 Resumen:")
    print(f"   - Train: {len(splits['train'])} imágenes")
    print(f"   - Val: {len(splits['val'])} imágenes")
    print(f"   - Test: {len(splits['test'])} imágenes")
    print(f"   - Total: {sum(len(v) for v in splits.values())} imágenes")

def verificar_dataset(data_root):
    """
    Verifica que el dataset esté correctamente organizado
    """
    print("\n🔍 Verificando dataset...")
    
    issues = []
    
    for split in ['train', 'val', 'test']:
        img_dir = Path(data_root) / 'images' / split
        label_dir = Path(data_root) / 'labels' / split
        
        if not img_dir.exists():
            issues.append(f"❌ No existe: {img_dir}")
            continue
        
        if not label_dir.exists():
            issues.append(f"❌ No existe: {label_dir}")
            continue
        
        # Contar archivos
        images = list(img_dir.glob('*.[jp][pn][g]')) + list(img_dir.glob('*.jpeg'))
        labels = list(label_dir.glob('*.txt'))
        
        print(f"\n📁 {split.upper()}:")
        print(f"   Imágenes: {len(images)}")
        print(f"   Etiquetas: {len(labels)}")
        
        # Verificar correspondencia
        for img in images:
            label_path = label_dir / f"{img.stem}.txt"
            if not label_path.exists():
                issues.append(f"⚠️  Falta etiqueta para: {img.name}")
    
    if issues:
        print(f"\n⚠️  Se encontraron {len(issues)} problemas:")
        for issue in issues[:10]:  # Mostrar solo los primeros 10
            print(f"   {issue}")
        if len(issues) > 10:
            print(f"   ... y {len(issues) - 10} más")
    else:
        print("\n✅ Dataset verificado - Sin problemas detectados")

def contar_clases(labels_dir):
    """
    Cuenta la distribución de clases en las etiquetas
    """
    print("\n📊 Analizando distribución de clases...")
    
    class_counts = {}
    total_objects = 0
    
    for label_file in Path(labels_dir).rglob('*.txt'):
        with open(label_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 5:  # Formato YOLO válido
                    class_id = int(parts[0])
                    class_counts[class_id] = class_counts.get(class_id, 0) + 1
                    total_objects += 1
    
    # Nombres de clases
    class_names = {
        0: 'Persona',
        1: 'Silla',
        2: 'Mesa',
        3: 'Puerta',
        4: 'Escalera',
        5: 'Obstaculo',
        6: 'Pared'
    }
    
    print(f"\n📈 Total de objetos etiquetados: {total_objects}")
    print("\n🏷️  Distribución por clase:")
    
    for class_id in sorted(class_counts.keys()):
        count = class_counts[class_id]
        percentage = (count / total_objects) * 100
        class_name = class_names.get(class_id, f'Clase {class_id}')
        print(f"   {class_name}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    # Ejemplo de uso
    print("="*60)
    print("UTILIDADES PARA PREPARACIÓN DE DATASET")
    print("="*60)
    
    # Ajusta estas rutas según tu configuración
    SOURCE_IMAGES = "/ruta/a/tus/imagenes"
    SOURCE_LABELS = "/ruta/a/tus/etiquetas"
    DEST_ROOT = "/home/claude/proyecto_vision_asistiva/data"
    
    # Descomentar para ejecutar:
    # organizar_dataset(SOURCE_IMAGES, SOURCE_LABELS, DEST_ROOT)
    # verificar_dataset(DEST_ROOT)
    # contar_clases(Path(DEST_ROOT) / 'labels')
    
    print("\n💡 Instrucciones:")
    print("   1. Edita SOURCE_IMAGES y SOURCE_LABELS con tus rutas")
    print("   2. Descomenta las funciones que necesites")
    print("   3. Ejecuta: python utils.py")