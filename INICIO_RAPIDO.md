# 🚀 GUÍA DE INICIO RÁPIDO

## ¿Qué hace este proyecto?
Sistema de detección de objetos en tiempo real con YOLOv8 para asistir a personas con discapacidad visual.
- Detecta 31 tipos de objetos (personas, escaleras, bancas, etc.)
- Notifica por voz los objetos detectados
- Funciona con la cámara web

---

## ⚡ INICIO RÁPIDO (3 pasos)

### 1️⃣ Activar entorno virtual
```powershell
.\venv\Scripts\Activate.ps1
```

Si da error de permisos:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Luego vuelve a intentar activar.

### 2️⃣ Instalar dependencias
```powershell
pip install -r requirements.txt
```
⏱️ Esto tomará varios minutos (descarga PyTorch, OpenCV, etc.)

### 3️⃣ Ejecutar el sistema
```powershell
python iniciar_deteccion.py
```

---

## 🎮 CONTROLES DEL SISTEMA

Cuando esté ejecutándose:
- **Q** = Salir
- **S** = Capturar imagen
- **V** = Activar/Desactivar voz

---

## 📊 OPCIONAL: Organizar dataset para re-entrenar

Si quieres entrenar el modelo desde cero:

```powershell
# 1. Organizar el dataset
python organizar_dataset.py

# 2. Entrenar modelo
cd src
python train.py
```

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### ❌ "No se pudo abrir la cámara"
- Verifica que tienes una cámara web conectada
- Cierra otras aplicaciones que usen la cámara
- Intenta cambiar `camera_id=0` a `camera_id=1` en el código

### ❌ "No se encontró el módulo 'ultralytics'"
```powershell
pip install ultralytics
```

### ❌ "No se encontró el modelo"
- El modelo ya está en `models/best.pt`
- Verifica que estás en la carpeta del proyecto

### ❌ Error de voz (pyttsx3)
```powershell
pip install pyttsx3
```

---

## 📝 ARCHIVOS PRINCIPALES

- `iniciar_deteccion.py` - **USAR ESTE** para probar el sistema
- `src/detect.py` - Versión avanzada con 2 cámaras (visión estéreo)
- `src/train.py` - Para entrenar el modelo
- `models/best.pt` - Modelo YOLOv8 ya entrenado

---

## 🎯 OBJETOS DETECTABLES (31 clases)

árbol, arbusto, bancas, banqueta, basurero, camino, caseta, cinta, 
edificio L, edificio c, entrada, **escaleras**, jardinera, letrero, 
llenado de agua, moto, pared, pasillo, **persona**, pilar, poste de luz, 
pupitres, rampa, salón, sillas, tronco, etc.

---

## 💡 TIPS

1. **Primera vez**: El sistema descargará el modelo base de YOLO (automático)
2. **Iluminación**: Funciona mejor con buena luz
3. **Distancia**: Coloca objetos a 1-3 metros de la cámara para mejor detección
4. **Rendimiento**: Si va lento, reduce la resolución de la cámara

---

## 📧 NECESITAS AYUDA?

1. Verifica que Python 3.13.7 esté instalado: `py --version`
2. Activa el entorno virtual: `.\venv\Scripts\Activate.ps1`
3. Instala dependencias: `pip install -r requirements.txt`
4. Ejecuta: `python iniciar_deteccion.py`
