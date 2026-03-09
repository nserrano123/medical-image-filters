#!/usr/bin/env python

import itk
import numpy as np
import matplotlib.pyplot as plt

# Cargar imágenes
original = itk.array_from_image(itk.imread('Adaptative/TAC/Panoramix-cropped_1.nii'))
img1 = itk.array_from_image(itk.imread('Panoramix_mean_r1.nii'))
img2 = itk.array_from_image(itk.imread('Panoramix_mean_r2.nii'))
img3 = itk.array_from_image(itk.imread('Panoramix_mean_r5.nii'))

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
axes[0, 1].set_title('Mean Filter - radius=1\n(Suavizado MÍNIMO)', fontsize=13, fontweight='bold')
axes[0, 1].axis('off')

# Configuración 2
axes[1, 0].imshow(slice2, cmap='gray')
axes[1, 0].set_title('Mean Filter - radius=2\n(Suavizado MODERADO)', fontsize=13, fontweight='bold')
axes[1, 0].axis('off')

# Configuración 3
axes[1, 1].imshow(slice3, cmap='gray')
axes[1, 1].set_title('Mean Filter - radius=5\n(Suavizado FUERTE)', fontsize=13, fontweight='bold')
axes[1, 1].axis('off')

plt.tight_layout()
plt.savefig('tac_mean_comparison.png', dpi=150, bbox_inches='tight')
print("✓ Comparación guardada en: tac_mean_comparison.png")

# Análisis estadístico
print("\n" + "="*70)
print("ANÁLISIS DE FILTRO MEAN EN TAC (Panoramix)")
print("="*70)

def analyze(img, name):
    print(f"\n{name}:")
    print(f"  Rango: [{img.min()}, {img.max()}]")
    print(f"  Media: {img.mean():.2f}")
    print(f"  Desviación estándar: {img.std():.2f}")
    print(f"  Contraste (std/mean): {(img.std()/img.mean()):.3f}")

analyze(orig_slice, "Original TAC")
analyze(slice1, "Mean radius=1")
analyze(slice2, "Mean radius=2")
analyze(slice3, "Mean radius=5")

print("\n" + "="*70)
print("EVALUACIÓN MEAN FILTER PARA TAC")
print("="*70)
print("""
QUÉ SE VE EN CADA CONFIGURACIÓN:

1. RADIUS=1 (ventana 3x3x3):
   - Reducción mínima de ruido
   - Bordes casi intactos
   - Imagen muy similar a la original
   - Útil para ruido de alta frecuencia muy leve

2. RADIUS=2 (ventana 5x5x5):
   - Suavizado moderado
   - Bordes empiezan a difuminarse
   - Reduce ruido visible
   - Pérdida moderada de detalles finos

3. RADIUS=5 (ventana 11x11x11):
   - Suavizado muy agresivo
   - Bordes muy borrosos
   - Pérdida significativa de detalles anatómicos
   - Imagen "pastosa" o "borrosa"

¿ES BUENO MEAN FILTER PARA TAC?

❌ GENERALMENTE NO, por estas razones:

1. Los TAC ya tienen buen contraste natural
2. Difumina bordes críticos (hueso-tejido, lesiones)
3. Pierde detalles anatómicos importantes
4. Hace la imagen menos útil para diagnóstico

✓ CASOS ESPECÍFICOS donde SÍ puede ser útil:
- Pre-procesamiento para segmentación automática
- Reducir ruido antes de reconstrucción 3D
- Suavizar artefactos de movimiento leves
- SOLO con radius muy pequeño (1-2)

COMPARACIÓN: ADAPTIVE vs MEAN para TAC
- ADAPTIVE: Mejora contraste, preserva bordes ✓✓✓
- MEAN: Reduce ruido, difumina todo ✗✗

RECOMENDACIÓN: Para TAC, usa Adaptive Histogram Equalization
en lugar de Mean Filter.
""")

plt.show()
