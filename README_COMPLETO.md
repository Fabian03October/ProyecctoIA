# 🤖 Sistema de Asistencia Visual con YOLOv8

## 📝 Descripción del Proyecto

Sistema de asistencia visual diseñado para ayudar a personas con discapacidad visual mediante detección de objetos en tiempo real utilizando inteligencia artificial. El sistema utiliza la cámara para detectar objetos y proporciona retroalimentación por voz en español.

## ✨ Características Principales

- 🎯 **Detección en Tiempo Real**: Procesa video de la cámara detectando objetos instantáneamente
- 🗣️ **Notificaciones por Voz**: Sistema de voz en español que anuncia los objetos detectados
- 📦 **80 Clases de Objetos**: Detecta personas, sillas, laptops, teléfonos, autos, bicicletas y más
- 🎨 **Visualización Clara**: Cuadros delimitadores y etiquetas en español
- ⚡ **Alto Rendimiento**: Modelo YOLOv8s optimizado para detección rápida
- 🔧 **Configurable**: Filtrado de objetos y umbrales de confianza ajustables

## 🛠️ Tecnologías Utilizadas

- **Python 3.13**: Lenguaje de programación principal
- **YOLOv8 (Ultralytics)**: Modelo de detección de objetos de última generación
- **OpenCV**: Procesamiento de video y visualización
- **pyttsx3**: Motor de síntesis de voz
- **Threading**: Procesamiento asíncrono de notificaciones de voz

## 📋 Requisitos Previos

- Python 3.8 o superior
- Cámara web funcional
- Windows, Linux o macOS

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Fabian03October/ProyecctoIA.git
cd ProyecctoIA
```

### 2. Crear Entorno Virtual (Recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` incluye:
- ultralytics (YOLOv8)
- opencv-python
- pyttsx3
- numpy

## 🎮 Uso

### Ejecución Básica

```bash
python iniciar_deteccion.py
```

### Controles Durante la Ejecución

- **ESC** o **Q**: Salir del programa
- La cámara se activa automáticamente
- Las detecciones aparecen con cuadros verdes y etiquetas en español
- El sistema anuncia por voz los objetos detectados

## 📁 Estructura del Proyecto

```
ProyecctoIA/
├── iniciar_deteccion.py         # Script principal de detección
├── iniciar_deteccion_COMENTADO.py  # Versión con comentarios detallados
├── requirements.txt              # Dependencias del proyecto
├── README_COMPLETO.md           # Este archivo
├── GUIA_COMPLETA.md             # Guía de desarrollo completa
├── .gitignore                   # Archivos excluidos de git
├── yolov8s.pt                   # Modelo pre-entrenado (descarga automática)
└── src/                         # Código fuente adicional
    ├── detect.py                # Funciones de detección
    ├── voice.py                 # Sistema de voz
    └── utils.py                 # Utilidades
```

## 🎯 Clases de Objetos Detectables

El sistema detecta 20 categorías principales de objetos:

- 👤 Personas
- 🪑 Sillas
- 💻 Laptops
- 📱 Teléfonos celulares
- 🚗 Autos
- 🚲 Bicicletas
- 🚪 Puertas
- 📚 Libros
- 🎒 Mochilas
- Y más...

## ⚙️ Configuración

### Ajustar Umbral de Confianza

En `iniciar_deteccion.py`, línea ~40:

```python
resultados = modelo(frame, conf=0.5)  # Cambiar 0.5 por el valor deseado (0-1)
```

### Modificar Objetos Detectables

En `iniciar_deteccion.py`, línea ~20:

```python
CLASES_IMPORTANTES = {
    0: 'persona',
    # Añadir o quitar clases según necesidad
}
```

## 🔧 Solución de Problemas

### La cámara no se activa

- Verificar que ningún otro programa esté usando la cámara
- Probar cambiar el índice de cámara: `cv2.VideoCapture(1)` en lugar de `cv2.VideoCapture(0)`

### El sistema no habla

- Verificar que pyttsx3 esté instalado correctamente
- En Windows, el motor de voz debe estar configurado

### Detecciones lentas

- Usar un modelo más ligero: `yolov8n.pt` en lugar de `yolov8s.pt`
- Reducir la resolución de la cámara

### Demasiadas detecciones falsas

- Aumentar el umbral de confianza a 0.6 o 0.7
- Filtrar más clases en `CLASES_IMPORTANTES`

## 📊 Rendimiento

- **FPS**: ~30 en hardware moderno
- **Latencia de detección**: < 50ms
- **Precisión**: 50% confianza mínima
- **Modelo**: YOLOv8s (22 MB)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu función (`git checkout -b feature/nueva-funcion`)
3. Commit tus cambios (`git commit -m 'Agregar nueva función'`)
4. Push a la rama (`git push origin feature/nueva-funcion`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

## 👨‍💻 Autor

**Fabian de Jesus**
- GitHub: [@Fabian03October](https://github.com/Fabian03October)
- Proyecto: Sistema de Asistencia Visual para personas con discapacidad visual

## 🙏 Agradecimientos

- **Ultralytics** por YOLOv8
- **OpenCV** por las herramientas de visión por computadora
- **pyttsx3** por el motor de síntesis de voz

## 📚 Referencias

- [Documentación de YOLOv8](https://docs.ultralytics.com/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Python pyttsx3](https://pyttsx3.readthedocs.io/)

---

**Nota**: Este es un proyecto educativo diseñado para demostrar el uso de inteligencia artificial en aplicaciones de accesibilidad. Para uso en producción, se recomienda realizar pruebas exhaustivas y optimizaciones adicionales.
