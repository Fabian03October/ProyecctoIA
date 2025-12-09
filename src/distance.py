# distance.py
#
# Fórmula:
# distancia = (ancho_real * distancia_focal) / ancho_en_pixeles
#
# Primero debes calibrar el sistema con un objeto cuyo ancho conozcas.

DISTANCIA_FOCAL = 650  # Valor aproximado, ajustar después de calibración

def calcular_distancia(ancho_real_cm, ancho_bbox_px):
    """
    Calcula la distancia aproximada del objeto a la cámara.
    ancho_real_cm: ancho real del objeto (en cm)
    ancho_bbox_px: ancho en píxeles del bounding box detectado
    """
    if ancho_bbox_px <= 0:
        return None

    distancia_cm = (ancho_real_cm * DISTANCIA_FOCAL) / ancho_bbox_px
    return distancia_cm
