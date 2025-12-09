"""
Script para organizar el dataset automáticamente
"""
import os
import shutil
import random
from pathlib import Path

def organizar_dataset():
    """Organiza imágenes y etiquetas desde train/ hacia data/"""
    
    print("📂 Organizando dataset...")
    
    # Directorios origen
    source_images = Path("train/images")
    source_labels = Path("train/labels")
    
    # Directorios destino
    dest_root = Path("data")
    
    # Crear estructura
    for split in ['train', 'val', 'test']:
        (dest_root / 'images' / split).mkdir(parents=True, exist_ok=True)
        (dest_root / 'labels' / split).mkdir(parents=True, exist_ok=True)
    
    # Obtener lista de imágenes
    images = list(source_images.glob("*.jpg"))
    print(f"📊 Total de imágenes encontradas: {len(images)}")
    
    # Filtrar solo imágenes con etiqueta
    valid_images = []
    for img in images:
        label_path = source_labels / f"{img.stem}.txt"
        if label_path.exists():
            valid_images.append(img)
    
    print(f"✅ Imágenes con etiquetas: {len(valid_images)}")
    
    # Mezclar aleatoriamente
    random.shuffle(valid_images)
    
    # Dividir: 80% train, 10% val, 10% test
    total = len(valid_images)
    train_end = int(total * 0.8)
    val_end = train_end + int(total * 0.1)
    
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
            dest_img = dest_root / 'images' / split / img_path.name
            shutil.copy2(img_path, dest_img)
            
            # Copiar etiqueta
            label_src = source_labels / f"{img_path.stem}.txt"
            dest_label = dest_root / 'labels' / split / f"{img_path.stem}.txt"
            shutil.copy2(label_src, dest_label)
    
    print("\n✅ Dataset organizado correctamente!")
    print(f"\n📊 Resumen:")
    print(f"   - Train: {len(splits['train'])} imágenes")
    print(f"   - Val: {len(splits['val'])} imágenes")
    print(f"   - Test: {len(splits['test'])} imágenes")

if __name__ == "__main__":
    organizar_dataset()
