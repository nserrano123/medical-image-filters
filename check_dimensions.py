#!/usr/bin/env python

import itk
import sys

def check_image_info(filename):
    image = itk.imread(filename)
    array = itk.array_from_image(image)
    
    print(f"\n{filename}:")
    print(f"  Dimensiones: {array.shape}")
    print(f"  Tipo: {'3D' if len(array.shape) == 3 else '2D'}")
    print(f"  Rango de valores: [{array.min()}, {array.max()}]")

if __name__ == "__main__":
    check_image_info("MRHead.nii")
    check_image_info("MRHead_filtered.nii")
