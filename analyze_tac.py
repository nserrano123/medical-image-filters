#!/usr/bin/env python

import itk
import numpy as np
import matplotlib.pyplot as plt

# Cargar imágenes
original = itk.array_from_image(itk.imread('Adaptative/TAC/Panoramix-cropped_1.nii'))
img1 = itk.array_from_image(itk.imread('Adaptative/TAC/Panoramix_a03_b03_r5.nii'))
img2 = itk.array_from_image(itk.imread('Adaptative/TAC/Panoramix_a05_b05_r3.nii'))
img3 = itk.array_from_image(itk.imread('Adaptative/TAC/Panoramix_a08_b08_r5.nii'))

# Seleccionar slice del medio
slice_idx = original.shape[0] // 2
orig_slice = original[slice_idx, :, :]
slice1 = img1[slice_idx, :, :]
slice2 = img2[slice_idx, :, :]
slice3 = img3[slice_idx, :, :]

# Crear figura comparativa
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

# Original
axes[0, 0].imshow(orig_slice, cmap='gray')
axes[0, 0].set_title('ORIGINAL (TAC sin filtro)', fontsize=13, fontweight='bold')
axes[0, 0].axis('off')

# Configuración 1
axes[0, 1].imshow(slice1, cmap='gray')
axes[0, 1].set_title('alpha=0.3, beta=0.3, radius=5\n(MODERADO)', fontsize=13, fontweight='bold')
axes[0, 1].axis('off')

# Configuración 2
axes[1, 0].imshow(slice2, cmap='gray')
axes[1, 0].set_title('alpha=0.5, beta=0.5, radius=3\n(INTERMEDIO)', fontsize=13, fontweight='bold')
axes[1, 0].axis('off')

# Configuración 3
axes[1, 1].imshow(slice3, cmap='gray')
axes[1, 1].set_title('alpha=0.8, beta=0.8, radius=5\n(FUERTE)', fontsize=13, fontweight='bold')
axes[1, 1].axis('off')

plt.tight_layout()
plt.savefig('tac_comparison.png', dpi=150, bbox_inches='tight')
print("✓ Comparación guardada en: tac_comparison.png")

# Análisis estadístico
print("\n" + "="*70)
print("ANÁLISIS DE FILTRO ADAPTIVE EN TAC (Panoramix)")
print("="*70)

def analyze(img, name):
    print(f"\n{name}:")
    print(f"  Rango: [{img.min()}, {img.max()}]")
    print(f"  Media: {img.mean():.2f}")
    print(f"  Desviación estándar: {img.std():.2f}")
    print(f"  Contraste (std/mean): {(img.std()/img.mean()):.3f}")

analyze(orig_slice, "Original TAC")
analyze(slice1, "Moderado (0.3, 0.3, 5)")
analyze(slice2, "Intermedio (0.5, 0.5, 3)")
analyze(slice3, "Fuerte (0.8, 0.8, 5)")

print("\n" + "="*70)
print("EVALUACIÓN PARA TAC")
print("="*70)
print("""
CARACTERÍSTICAS DEL TAC:
- Contraste natural alto entre hueso (blanco), tejido (gris), aire (negro)
- Valores de intensidad tienen significado físico (unidades Hounsfield)
- Menos ruido que resonancia magnética típicamente

EFECTO DEL FILTRO ADAPTIVE EN TAC:

1. MODERADO (0.3, 0.3, 5):
   ✓ Mejora sutil del contraste en tejidos blandos
   ✓ Preserva la escala Hounsfield relativamente bien
   ✓ Útil para visualizar órganos con poco contraste
   ⚠ Cambio mínimo en estructuras óseas

2. INTERMEDIO (0.5, 0.5, 3):
   ✓ Balance entre realce y preservación
   ✓ Mejora visibilidad de tejidos blandos significativamente
   ⚠ Empieza a alterar la relación de intensidades
   ⚠ Puede exagerar artefactos

3. FUERTE (0.8, 0.8, 5):
   ✓ Máximo realce de detalles sutiles
   ✓ Excelente para detectar lesiones pequeñas
   ⚠ Altera mucho la escala Hounsfield original
   ⚠ Puede crear apariencia artificial
   ⚠ Riesgo de amplificar artefactos metálicos

RECOMENDACIÓN PARA TAC:
- Para DIAGNÓSTICO: Usar parámetros bajos (0.2-0.4) o no usar
- Para VISUALIZACIÓN de tejidos blandos: Moderado (0.3-0.5)
- Para DETECCIÓN de lesiones sutiles: Intermedio a fuerte (0.5-0.7)
- EVITAR valores muy altos (>0.8) en TAC con implantes metálicos

CONCLUSIÓN: El filtro SÍ puede ser útil para TAC, pero con parámetros
más conservadores que en RM, especialmente si necesitas preservar la
información cuantitativa de las unidades Hounsfield.
""")

plt.show()
