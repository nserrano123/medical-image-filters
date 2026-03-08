#!/usr/bin/env python

import itk
import numpy as np
import matplotlib.pyplot as plt
import sys

def view_nii(filename):
    # Leer la imagen
    image = itk.imread(filename)
    array = itk.array_from_image(image)
    
    # Si es 3D, mostrar el slice del medio
    if len(array.shape) == 3:
        slice_idx = array.shape[0] // 2
        img_slice = array[slice_idx, :, :]
        title = f"{filename} - Slice {slice_idx}/{array.shape[0]}"
    else:
        img_slice = array
        title = filename
    
    plt.figure(figsize=(10, 8))
    plt.imshow(img_slice, cmap='gray')
    plt.title(title)
    plt.colorbar()
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        view_nii(sys.argv[1])
    else:
        print("Uso: python view_images.py <imagen.nii>")
