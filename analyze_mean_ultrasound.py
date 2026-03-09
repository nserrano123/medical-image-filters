#!/usr/bin/env python

import itk
import numpy as np
import matplotlib.pyplot as plt

# Cargar imágenes
original = itk.array_from_image(itk.imread('Adaptative/US/USProstate_3.nii'))
img1 = itk.array_from_image(itk.imread('USProstate_mean_r1.nii'))
img2 = itk.array_from_image(itk.imread('USProstate_mean_r2.nii'))
img3 = itk.array_from_image(itk.imread('USProstate_mean_r5.nii'))

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
axes[0, 0].set_title('ORIGINAL (Ultrasonido sin filtro)', fontsize=13, fontweight='bold')
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
plt.savefig('ultrasound_mean_comparison.png', dpi=150, bbox_inches='tight')
print("✓ Comparación guardada en: ultrasound_mean_comparison.png")

# Análisis estadístico
print("\n" + "="*70)
print("ANÁLISIS DE FILTRO MEAN EN ULTRASONIDO (USProstate)")
print("="*70)

def analyze(img, name):
    print(f"\n{name}:")
    print(f"  Rango: [{img.min()}, {img.max()}]")
    print(f"  Media: {img.mean():.2f}")
    print(f"  Desviación estándar: {img.std():.2f}")
    print(f"  Contraste (std/mean): {(img.std()/img.mean()):.3f}")

analyze(orig_slice, "Original Ultrasonido")
analyze(slice1, "Mean radius=1")
analyze(slice2, "Mean radius=2")
analyze(slice3, "Mean radius=5")

print("\n" + "="*70)
print("EVALUACIÓN MEAN FILTER PARA ULTRASONIDO")
print("="*70)
print("""
QUÉ SE VE EN CADA CONFIGURACIÓN:

1. RADIUS=1 (ventana 3x3x3):
   - Reduce speckle ligeramente
   - Bordes relativamente preservados
   - Imagen más limpia pero similar a original
   - Buen punto de partida

2. RADIUS=2 (ventana 5x5x5):
   - Reducción notable del speckle
   - Bordes empiezan a suavizarse
   - Imagen más "limpia" visualmente
   - Balance aceptable

3. RADIUS=5 (ventana 11x11x11):
   - Speckle casi eliminado
   - Bordes muy difuminados
   - Pérdida de detalles anatómicos
   - Imagen demasiado borrosa

¿ES BUENO MEAN FILTER PARA ULTRASONIDO?

✓ MEJOR QUE ADAPTIVE para ultrasonido, porque:
1. SÍ reduce el ruido speckle (no lo amplifica)
2. Suaviza la imagen de forma uniforme
3. Hace la imagen más "limpia" visualmente

⚠ PERO tiene limitaciones:
1. Difumina bordes importantes
2. Pierde detalles anatómicos con radius alto
3. No es el filtro óptimo para speckle

COMPARACIÓN: ADAPTIVE vs MEAN para Ultrasonido
- ADAPTIVE: Amplifica speckle ✗✗✗
- MEAN: Reduce speckle pero difumina ✓✗

RECOMENDACIÓN PARA ULTRASONIDO:
- Mean Filter con radius=1-2 es ACEPTABLE
- Mejor usar Median Filter (preserva bordes mejor)
- Ideal: Filtros específicos anti-speckle (Lee, Frost, Kuan)

CONCLUSIÓN: Mean Filter es MEJOR que Adaptive para ultrasonido,
pero sigue sin ser la opción ideal. Usa radius pequeño (1-2) si
lo aplicas.
""")

plt.show()
