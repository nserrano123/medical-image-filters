"""
Generates PNG comparison images for all segmentation results.
Shows axial, coronal, and sagital slices at the seed point (132, 142, 96)
with the segmentation overlaid in red on the original MRI.
"""
import itk
import numpy as np
import matplotlib
matplotlib.use("Agg")  # no GUI needed
import matplotlib.pyplot as plt
import os

INPUT_PATH = "../A1_grayT1.nii.gz"
SEED = (132, 142, 96)  # x, y, z

# Output folder
OUT_DIR = "../resultados_png"
os.makedirs(OUT_DIR, exist_ok=True)

# Load original
PixelType = itk.US
Dimension = 3
ImageType = itk.Image[PixelType, Dimension]
reader = itk.ImageFileReader[ImageType].New()
reader.SetFileName(INPUT_PATH)
reader.Update()
orig = itk.GetArrayFromImage(reader.GetOutput())  # (Z, Y, X)

# Segmentation files to process
seg_files = {
    # ConnectedThreshold
    "CT_narrow_80_140": ("../CT_narrow_80_140.nii.gz", "ConnectedThreshold\nLower=80, Upper=140"),
    "CT_default_100_170": ("../CT_default_100_170.nii.gz", "ConnectedThreshold\nLower=100, Upper=170"),
    "CT_wide_60_200": ("../CT_wide_60_200.nii.gz", "ConnectedThreshold\nLower=60, Upper=200"),
    "CT_verywide_50_250": ("../CT_verywide_50_250.nii.gz", "ConnectedThreshold\nLower=50, Upper=250"),
    # ConfidenceConnected
    "CC_m1_i0_r1": ("../CC_m1_i0_r1.nii.gz", "ConfidenceConnected\nMult=1, Iter=0, Rad=1"),
    "CC_m2_i0_r1": ("../CC_m2_i0_r1.nii.gz", "ConfidenceConnected\nMult=2, Iter=0, Rad=1"),
    "CC_m2_i3_r1": ("../CC_m2_i3_r1.nii.gz", "ConfidenceConnected\nMult=2, Iter=3, Rad=1"),
    "CC_m3_i2_r2": ("../CC_m3_i2_r2.nii.gz", "ConfidenceConnected\nMult=3, Iter=2, Rad=2"),
}

def load_seg(path):
    r = itk.ImageFileReader[ImageType].New()
    r.SetFileName(path)
    r.Update()
    return itk.GetArrayFromImage(r.GetOutput())

def make_overlay(bg_slice, seg_slice):
    """Create RGB image with red overlay where segmented."""
    # Normalize background to 0-1
    bg = bg_slice.astype(np.float32)
    if bg.max() > 0:
        bg = bg / bg.max()
    rgb = np.stack([bg, bg, bg], axis=-1)
    mask = seg_slice > 0
    rgb[mask] = [1.0, 0.2, 0.0]  # red overlay
    return rgb

# Slice indices from seed (ITK array is Z, Y, X)
sz, sy, sx = SEED[2], SEED[1], SEED[0]

print(f"Generating comparison images at seed slice ({sx}, {sy}, {sz})...")

# --- Individual images per segmentation ---
for name, (path, title) in seg_files.items():
    seg = load_seg(path)
    voxel_count = np.count_nonzero(seg)

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle(f"{title}\nVoxels segmentados: {voxel_count:,}", fontsize=14, fontweight="bold")

    views = [
        ("Axial", orig[sz, :, :], seg[sz, :, :]),
        ("Coronal", orig[:, sy, :], seg[:, sy, :]),
        ("Sagital", orig[:, :, sx], seg[:, :, sx]),
    ]

    for col, (view_name, bg_sl, seg_sl) in enumerate(views):
        # Top row: original with seed marker
        axes[0, col].imshow(bg_sl, cmap="gray", aspect="auto")
        axes[0, col].set_title(f"{view_name} - Original", fontsize=11)
        # Mark seed
        if view_name == "Axial":
            axes[0, col].plot(sx, sy, "g+", markersize=15, markeredgewidth=2)
        elif view_name == "Coronal":
            axes[0, col].plot(sx, sz, "g+", markersize=15, markeredgewidth=2)
        else:
            axes[0, col].plot(sy, sz, "g+", markersize=15, markeredgewidth=2)
        axes[0, col].axis("off")

        # Bottom row: overlay
        overlay = make_overlay(bg_sl, seg_sl)
        axes[1, col].imshow(overlay, aspect="auto")
        axes[1, col].set_title(f"{view_name} - Segmentación", fontsize=11)
        axes[1, col].axis("off")

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, f"{name}.png")
    plt.savefig(out_path, dpi=120, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved: {out_path}")

# --- Summary comparison: all ConnectedThreshold side by side ---
fig, axes = plt.subplots(2, 4, figsize=(20, 10))
fig.suptitle("Comparación ConnectedThreshold - Corte Axial", fontsize=16, fontweight="bold")
ct_keys = ["CT_narrow_80_140", "CT_default_100_170", "CT_wide_60_200", "CT_verywide_50_250"]
for i, key in enumerate(ct_keys):
    seg = load_seg(seg_files[key][0])
    vc = np.count_nonzero(seg)
    axes[0, i].imshow(orig[sz, :, :], cmap="gray", aspect="auto")
    axes[0, i].set_title(seg_files[key][1].replace("\n", " | "), fontsize=9)
    axes[0, i].axis("off")
    overlay = make_overlay(orig[sz, :, :], seg[sz, :, :])
    axes[1, i].imshow(overlay, aspect="auto")
    axes[1, i].set_title(f"Voxels: {vc:,}", fontsize=9)
    axes[1, i].axis("off")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "comparacion_ConnectedThreshold.png"), dpi=120, bbox_inches="tight", facecolor="white")
plt.close()
print(f"  Saved: comparacion_ConnectedThreshold.png")

# --- Summary comparison: all ConfidenceConnected side by side ---
fig, axes = plt.subplots(2, 4, figsize=(20, 10))
fig.suptitle("Comparación ConfidenceConnected - Corte Axial", fontsize=16, fontweight="bold")
cc_keys = ["CC_m1_i0_r1", "CC_m2_i0_r1", "CC_m2_i3_r1", "CC_m3_i2_r2"]
for i, key in enumerate(cc_keys):
    seg = load_seg(seg_files[key][0])
    vc = np.count_nonzero(seg)
    axes[0, i].imshow(orig[sz, :, :], cmap="gray", aspect="auto")
    axes[0, i].set_title(seg_files[key][1].replace("\n", " | "), fontsize=9)
    axes[0, i].axis("off")
    overlay = make_overlay(orig[sz, :, :], seg[sz, :, :])
    axes[1, i].imshow(overlay, aspect="auto")
    axes[1, i].set_title(f"Voxels: {vc:,}", fontsize=9)
    axes[1, i].axis("off")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "comparacion_ConfidenceConnected.png"), dpi=120, bbox_inches="tight", facecolor="white")
plt.close()
print(f"  Saved: comparacion_ConfidenceConnected.png")

print("\nDone! Check the 'resultados_png' folder.")
