"""
Script Simple para Probar el Sistema de Detección
Usa el modelo ya entrenado en models/best.pt
"""

import cv2
from ultralytics import YOLO
import pyttsx3
import threading

class DetectorSimple:
    def __init__(self, model_path='models/best.pt'):
        print("🚀 Cargando modelo YOLO...")
        try:
            self.model = YOLO(model_path)
            print("✅ Modelo cargado correctamente")
            print(f"📊 Clases detectables: {len(self.model.names)}")
            
            # Sistema de voz
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            print("✅ Sistema de voz inicializado")
            
        except Exception as e:
            print(f"❌ Error al cargar el modelo: {e}")
            raise
    
    def notificar_voz(self, mensaje):
        """Notifica mediante voz en hilo separado"""
        def speak():
            try:
                self.engine.say(mensaje)
                self.engine.runAndWait()
            except:
                pass
        
        thread = threading.Thread(target=speak)
        thread.daemon = True
        thread.start()
    
    def ejecutar(self, camera_id=0):
        """
        Ejecuta detección en tiempo real
        """
        print(f"\n🎥 Abriendo cámara {camera_id}...")
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            print("❌ Error: No se pudo abrir la cámara")
            print("💡 Verifica que tienes una cámara conectada")
            return
        
        print("✅ Cámara activa")
        print("\n📌 CONTROLES:")
        print("   - Presiona 'q' para SALIR")
        print("   - Presiona 's' para CAPTURAR imagen")
        print("   - Presiona 'v' para activar/desactivar VOZ")
        print("\n🚀 Sistema activo...\n")
        
        frame_count = 0
        voz_activa = True
        objetos_notificados = set()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error al capturar frame")
                break
            
            # Hacer detección cada 5 frames (mejor rendimiento)
            if frame_count % 5 == 0:
                results = self.model(frame, verbose=False, conf=0.5)
                
                # Procesar resultados
                annotated_frame = results[0].plot()
                
                # Contar detecciones
                detecciones = {}
                for box in results[0].boxes:
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]
                    confidence = float(box.conf[0])
                    
                    if class_name not in detecciones:
                        detecciones[class_name] = 0
                    detecciones[class_name] += 1
                    
                    # Notificar por voz (solo una vez por objeto)
                    if voz_activa and class_name not in objetos_notificados:
                        mensaje = f"Detectado {class_name}"
                        self.notificar_voz(mensaje)
                        objetos_notificados.add(class_name)
                
                # Limpiar objetos notificados si no se detectan
                objetos_actuales = set(detecciones.keys())
                objetos_notificados = objetos_notificados.intersection(objetos_actuales)
                
                # Mostrar información en pantalla
                y_pos = 30
                for clase, cantidad in detecciones.items():
                    texto = f"{clase}: {cantidad}"
                    cv2.putText(annotated_frame, texto, (10, y_pos),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    y_pos += 30
                
                # Indicador de voz
                estado_voz = "VOZ: ON" if voz_activa else "VOZ: OFF"
                color_voz = (0, 255, 0) if voz_activa else (0, 0, 255)
                cv2.putText(annotated_frame, estado_voz, (10, frame.shape[0] - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_voz, 2)
            else:
                annotated_frame = frame
            
            # Mostrar frame
            cv2.imshow('Sistema de Deteccion - Asistencia Visual', annotated_frame)
            
            frame_count += 1
            
            # Controles de teclado
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\n👋 Cerrando sistema...")
                break
            elif key == ord('s'):
                filename = f'captura_{frame_count}.jpg'
                cv2.imwrite(filename, annotated_frame)
                print(f"📸 Captura guardada: {filename}")
            elif key == ord('v'):
                voz_activa = not voz_activa
                estado = "activada" if voz_activa else "desactivada"
                print(f"🔊 Voz {estado}")
        
        # Limpiar
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Sistema cerrado correctamente")

def main():
    """Función principal"""
    print("="*60)
    print("  SISTEMA DE ASISTENCIA VISUAL PARA PERSONAS")
    print("  CON DISCAPACIDAD VISUAL")
    print("="*60)
    print()
    
    try:
        # Crear detector (usando modelo base YOLOv8s)
        detector = DetectorSimple(model_path='yolov8s.pt')
        
        # Ejecutar
        detector.ejecutar(camera_id=0)
        
    except FileNotFoundError:
        print("\n❌ ERROR: No se encontró el modelo 'models/best.pt'")
        print("💡 Solución: Asegúrate de que el archivo existe")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("💡 Verifica que instalaste todas las dependencias:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
