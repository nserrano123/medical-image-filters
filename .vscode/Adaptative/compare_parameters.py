#!/usr/bin/env python

import itk
import numpy as np
import matplotlib.pyplot as plt

# Cargar imágenes
original = itk.array_from_image(itk.imread('MRHead.nii'))
img1 = itk.array_from_image(itk.imread('MRHead_a03_b03_r5.nii'))  # alpha=0.3, beta=0.3, radius=5
img2 = itk.array_from_image(itk.imread('MRHead_a08_b08_r5.nii'))  # alpha=0.8, beta=0.8, radius=5
img3 = itk.array_from_image(itk.imread('MRHead_a08_b08_r2.nii'))  # alpha=0.8, beta=0.8, radius=2

# Seleccionar slice del medio
slice_idx = original.shape[0] // 2
orig_slice = original[slice_idx, :, :]
slice1 = img1[slice_idx, :, :]
slice2 = img2[slice_idx, :, :]
slice3 = img3[slice_idx, :, :]

# Crear figura comparativa
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Original
axes[0, 0].imshow(orig_slice, cmap='gray')
axes[0, 0].set_title('Original\n(sin filtro)', fontsize=12, fontweight='bold')
axes[0, 0].axis('off')

# Configuración 1
axes[0, 1].imshow(slice1, cmap='gray')
axes[0, 1].set_title('alpha=0.3, beta=0.3, radius=5\n(Efecto MODERADO)', fontsize=12, fontweight='bold')
axes[0, 1].axis('off')

# Configuración 2
axes[1, 0].imshow(slice2, cmap='gray')
axes[1, 0].set_title('alpha=0.8, beta=0.8, radius=5\n(Efecto FUERTE, ventana MEDIA)', fontsize=12, fontweight='bold')
axes[1, 0].axis('off')

# Configuración 3
axes[1, 1].imshow(slice3, cmap='gray')
axes[1, 1].set_title('alpha=0.8, beta=0.8, radius=2\n(Efecto FUERTE, ventana PEQUEÑA)', fontsize=12, fontweight='bold')
axes[1, 1].axis('off')

plt.tight_layout()
plt.savefig('comparison.png', dpi=150, bbox_inches='tight')
print("✓ Comparación guardada en: comparison.png")

# Análisis estadístico
print("\n" + "="*60)
print("ANÁLISIS DE PARÁMETROS")
print("="*60)

def analyze(img, name):
    print(f"\n{name}:")
    print(f"  Rango: [{img.min()}, {img.max()}]")
    print(f"  Media: {img.mean():.2f}")
    print(f"  Desviación estándar: {img.std():.2f}")
    print(f"  Contraste (std/mean): {(img.std()/img.mean()):.3f}")

analyze(orig_slice, "Original")
analyze(slice1, "alpha=0.3, beta=0.3, radius=5")
analyze(slice2, "alpha=0.8, beta=0.8, radius=5")
analyze(slice3, "alpha=0.8, beta=0.8, radius=2")

print("\n" + "="*60)
print("INTERPRETACIÓN")
print("="*60)
print("""
1. ALPHA y BETA (0.3 vs 0.8):
   - Valores BAJOS (0.3): Efecto suave, preserva más la imagen original
   - Valores ALTOS (0.8): Efecto fuerte, mayor realce de contraste local
   
2. RADIUS (2 vs 5):
   - PEQUEÑO (2): Ventana local pequeña, realza detalles finos
   - GRANDE (5): Ventana local más grande, realce más suave y uniforme
   
3. COMBINACIONES:
   - (0.3, 0.3, 5): Balance entre preservación y realce
   - (0.8, 0.8, 5): Máximo contraste con transiciones suaves
   - (0.8, 0.8, 2): Máximo contraste con detalles muy finos
""")

plt.show()
