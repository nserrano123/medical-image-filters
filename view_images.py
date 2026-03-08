#!/usr/bin/env python

import itk
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse

def get_slice(array, slice_idx=None):
    """Obtiene un slice de una imagen 3D o devuelve la imagen 2D"""
    if len(array.shape) == 3:
        if slice_idx is None:
            slice_idx = array.shape[0] // 2
        return array[slice_idx, :, :], slice_idx
    else:
        return array, None

def view_single(filename, slice_idx=None):
    """Visualiza una sola imagen"""
    image = itk.imread(filename)
    array = itk.array_from_image(image)
    
    img_slice, actual_slice = get_slice(array, slice_idx)
    
    if actual_slice is not None:
        title = f"{filename}\nSlice {actual_slice}/{array.shape[0]-1}"
    else:
        title = filename
    
    plt.figure(figsize=(10, 8))
    plt.imshow(img_slice, cmap='gray')
    plt.title(title, fontsize=12, fontweight='bold')
    plt.colorbar(label='Intensidad')
    plt.axis('off')
    
    # Estadísticas
    stats = f"Min: {img_slice.min()}, Max: {img_slice.max()}, Media: {img_slice.mean():.1f}"
    plt.text(0.5, -0.05, stats, transform=plt.gca().transAxes, 
             ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.show()

def view_compare(filenames, slice_idx=None):
    """Compara múltiples imágenes lado a lado"""
    n_images = len(filenames)
    cols = min(3, n_images)
    rows = (n_images + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(6*cols, 5*rows))
    if n_images == 1:
        axes = [axes]
    else:
        axes = axes.flatten() if n_images > 1 else [axes]
    
    for idx, filename in enumerate(filenames):
        image = itk.imread(filename)
        array = itk.array_from_image(image)
        img_slice, actual_slice = get_slice(array, slice_idx)
        
        axes[idx].imshow(img_slice, cmap='gray')
        
        if actual_slice is not None:
            title = f"{filename}\nSlice {actual_slice}/{array.shape[0]-1}"
        else:
            title = filename
        
        axes[idx].set_title(title, fontsize=10, fontweight='bold')
        axes[idx].axis('off')
        
        # Estadísticas
        stats = f"Rango: [{img_slice.min()}, {img_slice.max()}]\nMedia: {img_slice.mean():.1f}"
        axes[idx].text(0.5, -0.05, stats, transform=axes[idx].transAxes,
                      ha='center', fontsize=8, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    # Ocultar ejes sobrantes
    for idx in range(n_images, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Visualizador de imágenes médicas .nii",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python view_images.py imagen.nii                    # Ver una imagen
  python view_images.py imagen.nii --slice 50         # Ver slice específico
  python view_images.py img1.nii img2.nii img3.nii    # Comparar múltiples
        """
    )
    parser.add_argument("images", nargs='+', help="Imagen(es) .nii a visualizar")
    parser.add_argument("--slice", type=int, default=None, help="Número de slice a mostrar (para imágenes 3D)")
    
    args = parser.parse_args()
    
    if len(args.images) == 1:
        view_single(args.images[0], args.slice)
    else:
        view_compare(args.images, args.slice)
