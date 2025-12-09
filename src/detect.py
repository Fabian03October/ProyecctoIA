"""
Sistema de Detección con Visión Estéreo para Cálculo de Distancias
Usa 2 cámaras para calcular la distancia a los objetos detectados

Este módulo implementa:
1. Detección de objetos con YOLO
2. Cálculo de disparidad entre 2 cámaras
3. Estimación de distancia usando triangulación estéreo
4. Síntesis de voz para notificar al usuario
"""

import cv2
import numpy as np
from ultralytics import YOLO
import pyttsx3
import threading
from datetime import datetime

class SistemaVisionEstereo:
    """
    Sistema completo de detección y medición de distancia
    usando 2 cámaras (visión estéreo)
    """
    
    def __init__(self, model_path, focal_length=700, baseline=0.06):
        """
        Args:
            model_path: Ruta al modelo YOLO entrenado
            focal_length: Distancia focal de las cámaras (en píxeles)
            baseline: Separación entre cámaras (en metros) - típicamente 6cm
        """
        print("🚀 Inicializando Sistema de Visión Estéreo...")
        
        # Cargar modelo YOLO
        self.model = YOLO(model_path)
        print(f"✅ Modelo YOLO cargado: {model_path}")
        
        # Parámetros de cámaras estéreo
        self.focal_length = focal_length
        self.baseline = baseline
        
        # Sistema de síntesis de voz
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        
        # Control de notificaciones
        self.last_notification = {}
        self.notification_cooldown = 2.0  # segundos
        
        # Colores para visualización (BGR)
        self.colors = {
            'Persona': (0, 255, 0),
            'Silla': (255, 0, 0),
            'Mesa': (0, 0, 255),
            'Puerta': (255, 255, 0),
            'Escalera': (255, 0, 255),
            'Obstaculo': (0, 255, 255),
            'Pared': (128, 128, 128)
        }
        
        print("✅ Sistema inicializado correctamente")
    
    def calcular_distancia_estereo(self, disparity_map, x_center, y_center):
        """
        Calcula la distancia usando disparidad estéreo
        
        Fórmula: Z = (f × B) / d
        donde:
            Z = distancia al objeto
            f = distancia focal
            B = baseline (separación entre cámaras)
            d = disparidad
        
        Args:
            disparity_map: Mapa de disparidad
            x_center, y_center: Coordenadas del centro del objeto
        
        Returns:
            float: Distancia en metros
        """
        # Obtener disparidad en el punto central del objeto
        y, x = int(y_center), int(x_center)
        
        # Verificar límites
        if y >= disparity_map.shape[0] or x >= disparity_map.shape[1]:
            return None
        
        disparity = disparity_map[y, x]
        
        # Evitar división por cero
        if disparity <= 0:
            return None
        
        # Calcular distancia
        distance = (self.focal_length * self.baseline) / disparity
        
        return distance
    
    def calcular_mapa_disparidad(self, frame_left, frame_right):
        """
        Calcula el mapa de disparidad entre las dos imágenes
        
        Args:
            frame_left: Imagen de cámara izquierda
            frame_right: Imagen de cámara derecha
        
        Returns:
            np.array: Mapa de disparidad
        """
        # Convertir a escala de grises
        gray_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
        gray_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)
        
        # Crear objeto StereoSGBM
        stereo = cv2.StereoSGBM_create(
            minDisparity=0,
            numDisparities=64,  # Debe ser divisible por 16
            blockSize=11,
            P1=8 * 3 * 11**2,
            P2=32 * 3 * 11**2,
            disp12MaxDiff=1,
            uniquenessRatio=10,
            speckleWindowSize=100,
            speckleRange=32
        )
        
        # Calcular disparidad
        disparity = stereo.compute(gray_left, gray_right).astype(np.float32) / 16.0
        
        return disparity
    
    def notificar_voz(self, mensaje):
        """
        Notifica al usuario mediante síntesis de voz (en hilo separado)
        """
        def speak():
            self.engine.say(mensaje)
            self.engine.runAndWait()
        
        thread = threading.Thread(target=speak)
        thread.daemon = True
        thread.start()
    
    def debe_notificar(self, objeto_clase):
        """
        Determina si debe notificar sobre un objeto (evita spam)
        """
        now = datetime.now().timestamp()
        
        if objeto_clase not in self.last_notification:
            self.last_notification[objeto_clase] = now
            return True
        
        if now - self.last_notification[objeto_clase] > self.notification_cooldown:
            self.last_notification[objeto_clase] = now
            return True
        
        return False
    
    def procesar_detecciones(self, frame, results, disparity_map=None):
        """
        Procesa las detecciones y calcula distancias
        
        Args:
            frame: Frame de video
            results: Resultados de YOLO
            disparity_map: Mapa de disparidad (opcional)
        
        Returns:
            frame con anotaciones
        """
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                # Obtener información de la detección
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                
                # Calcular centro del objeto
                x_center = (x1 + x2) / 2
                y_center = (y1 + y2) / 2
                
                # Calcular distancia si hay mapa de disparidad
                distance = None
                if disparity_map is not None:
                    distance = self.calcular_distancia_estereo(
                        disparity_map, x_center, y_center
                    )
                
                # Preparar etiqueta
                label = f"{class_name}: {confidence:.2f}"
                if distance is not None and distance > 0:
                    label += f" - {distance:.2f}m"
                    
                    # Notificación de voz para objetos cercanos
                    if distance < 2.0 and self.debe_notificar(class_name):
                        mensaje = f"{class_name} a {distance:.1f} metros"
                        self.notificar_voz(mensaje)
                
                # Dibujar bounding box
                color = self.colors.get(class_name, (255, 255, 255))
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                # Dibujar etiqueta
                (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(frame, (x1, y1 - h - 10), (x1 + w, y1), color, -1)
                cv2.putText(frame, label, (x1, y1 - 5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                
                # Dibujar punto central
                cv2.circle(frame, (int(x_center), int(y_center)), 5, color, -1)
        
        return frame
    
    def ejecutar_deteccion_estereo(self, cam_left_id=0, cam_right_id=1):
        """
        Ejecuta el sistema completo con 2 cámaras
        
        Args:
            cam_left_id: ID de cámara izquierda
            cam_right_id: ID de cámara derecha
        """
        print(f"\n🎥 Iniciando cámaras...")
        print(f"   Cámara izquierda: {cam_left_id}")
        print(f"   Cámara derecha: {cam_right_id}")
        
        # Inicializar cámaras
        cap_left = cv2.VideoCapture(cam_left_id)
        cap_right = cv2.VideoCapture(cam_right_id)
        
        if not cap_left.isOpened() or not cap_right.isOpened():
            print("❌ Error: No se pudieron abrir las cámaras")
            return
        
        print("✅ Cámaras inicializadas")
        print("\n📌 Controles:")
        print("   - Presiona 'q' para salir")
        print("   - Presiona 's' para capturar pantalla")
        print("   - Presiona 'd' para activar/desactivar mapa de disparidad")
        print("\n🚀 Sistema activo...\n")
        
        show_disparity = True
        
        while True:
            # Capturar frames de ambas cámaras
            ret_left, frame_left = cap_left.read()
            ret_right, frame_right = cap_right.read()
            
            if not ret_left or not ret_right:
                print("❌ Error al capturar frames")
                break
            
            # Calcular mapa de disparidad
            disparity_map = self.calcular_mapa_disparidad(frame_left, frame_right)
            
            # Realizar detección (solo en cámara izquierda)
            results = self.model(frame_left, verbose=False)
            
            # Procesar detecciones
            frame_anotado = self.procesar_detecciones(
                frame_left.copy(), results, disparity_map
            )
            
            # Mostrar frames
            cv2.imshow('Sistema de Detección - Cámara Principal', frame_anotado)
            cv2.imshow('Cámara Derecha (Referencia)', frame_right)
            
            if show_disparity:
                # Normalizar mapa de disparidad para visualización
                disparity_normalized = cv2.normalize(
                    disparity_map, None, 0, 255, cv2.NORM_MINMAX
                )
                disparity_colored = cv2.applyColorMap(
                    disparity_normalized.astype(np.uint8), cv2.COLORMAP_JET
                )
                cv2.imshow('Mapa de Disparidad', disparity_colored)
            
            # Controles de teclado
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\n👋 Cerrando sistema...")
                break
            elif key == ord('s'):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                cv2.imwrite(f'captura_{timestamp}.jpg', frame_anotado)
                print(f"📸 Captura guardada: captura_{timestamp}.jpg")
            elif key == ord('d'):
                show_disparity = not show_disparity
                if not show_disparity:
                    cv2.destroyWindow('Mapa de Disparidad')
        
        # Liberar recursos
        cap_left.release()
        cap_right.release()
        cv2.destroyAllWindows()
        print("✅ Sistema cerrado correctamente")

def main():
    """
    Función principal
    """
    # Ruta al modelo entrenado (ajustar según tu experimento)
    MODEL_PATH = "../results/exp1_base/weights/best.pt"
    
    # Crear sistema
    sistema = SistemaVisionEstereo(
        model_path=MODEL_PATH,
        focal_length=700,    # Ajustar según calibración
        baseline=0.06        # 6 cm de separación entre cámaras
    )
    
    # Ejecutar con 2 cámaras
    # NOTA: Ajusta los IDs según tu configuración
    # Típicamente: 0 (cámara integrada), 1 y 2 (cámaras USB)
    sistema.ejecutar_deteccion_estereo(cam_left_id=0, cam_right_id=1)

if __name__ == "__main__":
    main()