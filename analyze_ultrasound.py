#!/usr/bin/env python

import itk
import numpy as np
import matplotlib.pyplot as plt

# Cargar imágenes
original = itk.array_from_image(itk.imread('Adaptative/US/USProstate_3.nii'))
img1 = itk.array_from_image(itk.imread('Adaptative/US/USProstate_a03_b03_r5.nii'))
img2 = itk.array_from_image(itk.imread('Adaptative/US/USProstate_a05_b05_r3.nii'))
img3 = itk.array_from_image(itk.imread('Adaptative/US/USProstate_a08_b08_r5.nii'))

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
plt.savefig('ultrasound_comparison.png', dpi=150, bbox_inches='tight')
print("✓ Comparación guardada en: ultrasound_comparison.png")

# Análisis estadístico
print("\n" + "="*70)
print("ANÁLISIS DE FILTRO ADAPTIVE EN ULTRASONIDO (USProstate)")
print("="*70)

def analyze(img, name):
    print(f"\n{name}:")
    print(f"  Rango: [{img.min()}, {img.max()}]")
    print(f"  Media: {img.mean():.2f}")
    print(f"  Desviación estándar: {img.std():.2f}")
    print(f"  Contraste (std/mean): {(img.std()/img.mean()):.3f}")

analyze(orig_slice, "Original Ultrasonido")
analyze(slice1, "Moderado (0.3, 0.3, 5)")
analyze(slice2, "Intermedio (0.5, 0.5, 3)")
analyze(slice3, "Fuerte (0.8, 0.8, 5)")

print("\n" + "="*70)
print("EVALUACIÓN PARA ULTRASONIDO")
print("="*70)
print("""
CARACTERÍSTICAS DEL ULTRASONIDO:
- MUCHO ruido speckle (granulado característico)
- Contraste variable según profundidad y tejido
- Artefactos de sombra acústica y reverberación
- Calidad depende del operador y configuración del equipo

EFECTO DEL FILTRO ADAPTIVE EN ULTRASONIDO:

1. MODERADO (0.3, 0.3, 5):
   ✓ Mejora contraste sin amplificar mucho el speckle
   ✓ Estructuras anatómicas más visibles
   ✓ Balance razonable para visualización
   ⚠ El speckle sigue presente

2. INTERMEDIO (0.5, 0.5, 3):
   ✓ Mayor realce de bordes y estructuras
   ✓ Mejor diferenciación de tejidos
   ⚠ Empieza a amplificar el ruido speckle
   ⚠ Puede crear textura artificial

3. FUERTE (0.8, 0.8, 5):
   ✓ Máximo contraste local
   ✓ Estructuras muy definidas
   ⚠⚠ AMPLIFICA MUCHO el ruido speckle
   ⚠⚠ Puede crear artefactos visuales
   ⚠⚠ Imagen puede verse muy "ruidosa"

PROBLEMA PRINCIPAL: RUIDO SPECKLE
El ultrasonido tiene ruido multiplicativo (speckle) que es diferente
al ruido aditivo de RM/TAC. El filtro Adaptive puede AMPLIFICAR este
ruido en lugar de mejorarlo.

RECOMENDACIÓN PARA ULTRASONIDO:
❌ El filtro Adaptive NO es ideal para ultrasonido
✓ Mejor usar filtros específicos para speckle:
  - Median Filter (preserva bordes, reduce speckle)
  - Anisotropic Diffusion
  - Filtros específicos: Lee, Frost, Kuan

Si DEBES usar Adaptive en ultrasonido:
- Usa parámetros MUY bajos: alpha=0.2-0.3, beta=0.2-0.3
- Radius moderado: 3-5
- Combínalo con filtro de reducción de speckle primero

CONCLUSIÓN: Para ultrasonido, el filtro Adaptive puede empeorar
la calidad de imagen al amplificar el ruido speckle. Es mejor usar
filtros diseñados específicamente para este tipo de imágenes.
""")

plt.show()
