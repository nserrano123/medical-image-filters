"""
Interactive Region Growing Segmentation Viewer
- ConnectedThreshold (manual thresholds)
- ConfidenceConnected (automatic thresholds)

Uses matplotlib widgets for parameter tuning and real-time visualization.
"""
import itk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import sys

# --- Load volume ---
INPUT_PATH = sys.argv[1] if len(sys.argv) > 1 else "../A1_grayT1.nii.gz"

print(f"Loading {INPUT_PATH} ...")
PixelType = itk.US
Dimension = 3
ImageType = itk.Image[PixelType, Dimension]

reader = itk.ImageFileReader[ImageType].New()
reader.SetFileName(INPUT_PATH)
reader.Update()

image = reader.GetOutput()
size = image.GetLargestPossibleRegion().GetSize()
print(f"Volume size: {size[0]} x {size[1]} x {size[2]}")

# Convert to numpy for display (ITK uses [z, y, x] ordering)
arr = itk.GetArrayFromImage(image)  # shape: (Z, Y, X)

# --- State ---
current_method = "ConnectedThreshold"
current_slice_axis = 1  # 0=sagital, 1=coronal, 2=axial
seg_overlay = None

# Default params
params = {
    "seed_x": 132, "seed_y": 142, "seed_z": 96,
    "lower": 100, "upper": 170,
    "iterations": 0, "multiplier": 2.0, "radius": 1,
}

def run_connected_threshold():
    f = itk.ConnectedThresholdImageFilter[ImageType, ImageType].New()
    f.SetInput(image)
    f.SetLower(int(params["lower"]))
    f.SetUpper(int(params["upper"]))
    f.SetReplaceValue(255)
    f.SetSeed([int(params["seed_x"]), int(params["seed_y"]), int(params["seed_z"])])
    f.Update()
    return itk.GetArrayFromImage(f.GetOutput())

def run_confidence_connected():
    f = itk.ConfidenceConnectedImageFilter[ImageType, ImageType].New()
    f.SetInput(image)
    f.SetNumberOfIterations(int(params["iterations"]))
    f.SetMultiplier(float(params["multiplier"]))
    f.SetInitialNeighborhoodRadius(int(params["radius"]))
    f.SetReplaceValue(255)
    f.SetSeed([int(params["seed_x"]), int(params["seed_y"]), int(params["seed_z"])])
    f.Update()
    return itk.GetArrayFromImage(f.GetOutput())

def run_segmentation():
    global seg_overlay
    try:
        if current_method == "ConnectedThreshold":
            seg_overlay = run_connected_threshold()
        else:
            seg_overlay = run_confidence_connected()
        voxel_count = np.count_nonzero(seg_overlay)
        status_text.set_text(f"Segmented voxels: {voxel_count}")
    except Exception as e:
        seg_overlay = None
        status_text.set_text(f"Error: {e}")

def get_slice(vol, axis, idx):
    if axis == 2:    # axial
        return vol[idx, :, :]
    elif axis == 1:  # coronal
        return vol[:, idx, :]
    else:            # sagital
        return vol[:, :, idx]

def get_max_slice(axis):
    return arr.shape[axis] - 1

def get_seed_slice():
    seeds = [int(params["seed_z"]), int(params["seed_y"]), int(params["seed_x"])]
    return seeds[current_slice_axis]

# --- Build figure ---
fig = plt.figure(figsize=(14, 8))
fig.canvas.manager.set_window_title("Region Growing - Interactive Segmentation")
fig.patch.set_facecolor("#1e1e1e")

# Image axes
ax_img = fig.add_axes([0.05, 0.30, 0.42, 0.65])
ax_seg = fig.add_axes([0.52, 0.30, 0.42, 0.65])
for ax in [ax_img, ax_seg]:
    ax.set_facecolor("black")
    ax.tick_params(colors="white")

ax_img.set_title("Original", color="white", fontsize=12)
ax_seg.set_title("Segmentation Overlay", color="white", fontsize=12)

# Initial display
init_slice = get_seed_slice()
im_orig = ax_img.imshow(get_slice(arr, current_slice_axis, init_slice), cmap="gray", aspect="auto")
im_seg_bg = ax_seg.imshow(get_slice(arr, current_slice_axis, init_slice), cmap="gray", aspect="auto")
# Overlay as RGBA: red where segmented, fully transparent elsewhere
_init_seg_rgba = np.zeros((*get_slice(arr, current_slice_axis, init_slice).shape, 4), dtype=np.float32)
im_seg_ov = ax_seg.imshow(_init_seg_rgba, aspect="auto")

# Seed marker — always visible with crosshair + circle
seed_marker_orig, = ax_img.plot([], [], "g+", markersize=22, markeredgewidth=3)
seed_circle_orig, = ax_img.plot([], [], "go", markersize=12, markeredgewidth=2, fillstyle="none")
seed_marker_seg, = ax_seg.plot([], [], "g+", markersize=22, markeredgewidth=3)
seed_circle_seg, = ax_seg.plot([], [], "go", markersize=12, markeredgewidth=2, fillstyle="none")

# Status text
status_text = fig.text(0.5, 0.96, "", ha="center", color="cyan", fontsize=11)

# --- Sliders ---
slider_color = "#3a3a3a"
active_color = "#00aaff"

ax_slice = fig.add_axes([0.15, 0.20, 0.70, 0.025], facecolor=slider_color)
ax_sx = fig.add_axes([0.15, 0.16, 0.20, 0.025], facecolor=slider_color)
ax_sy = fig.add_axes([0.42, 0.16, 0.20, 0.025], facecolor=slider_color)
ax_sz = fig.add_axes([0.69, 0.16, 0.20, 0.025], facecolor=slider_color)

# Method-specific slider axes
ax_p1 = fig.add_axes([0.15, 0.11, 0.30, 0.025], facecolor=slider_color)
ax_p2 = fig.add_axes([0.55, 0.11, 0.30, 0.025], facecolor=slider_color)
ax_p3 = fig.add_axes([0.15, 0.06, 0.30, 0.025], facecolor=slider_color)

s_slice = Slider(ax_slice, "Slice", 0, get_max_slice(current_slice_axis), valinit=init_slice, valstep=1, color=active_color)
s_sx = Slider(ax_sx, "Seed X", 0, size[0]-1, valinit=params["seed_x"], valstep=1, color=active_color)
s_sy = Slider(ax_sy, "Seed Y", 0, size[1]-1, valinit=params["seed_y"], valstep=1, color=active_color)
s_sz = Slider(ax_sz, "Seed Z", 0, size[2]-1, valinit=params["seed_z"], valstep=1, color=active_color)

# Initial method sliders (ConnectedThreshold)
s_p1 = Slider(ax_p1, "Lower", 0, 500, valinit=params["lower"], valstep=1, color="#ff6600")
s_p2 = Slider(ax_p2, "Upper", 0, 500, valinit=params["upper"], valstep=1, color="#ff6600")
s_p3 = Slider(ax_p3, "---", 0, 1, valinit=0, valstep=1, color="#666666")
s_p3.ax.set_visible(False)

# Make all slider labels and values white
for s in [s_slice, s_sx, s_sy, s_sz, s_p1, s_p2, s_p3]:
    s.label.set_color("white")
    s.valtext.set_color("white")

# Method selector
ax_radio = fig.add_axes([0.55, 0.01, 0.35, 0.08], facecolor="#2a2a2a")
radio = RadioButtons(ax_radio, ("ConnectedThreshold", "ConfidenceConnected"), active=0)
for label in radio.labels:
    label.set_color("white")
    label.set_fontsize(10)

# Run button
ax_btn = fig.add_axes([0.15, 0.01, 0.15, 0.04])
btn_run = Button(ax_btn, "Run Segmentation", color="#005500", hovercolor="#008800")
btn_run.label.set_color("white")

# Axis selector
ax_axis_radio = fig.add_axes([0.35, 0.01, 0.15, 0.08], facecolor="#2a2a2a")
axis_radio = RadioButtons(ax_axis_radio, ("Sagital", "Coronal", "Axial"), active=1)
for label in axis_radio.labels:
    label.set_color("white")
    label.set_fontsize(9)

# --- Callbacks ---
def update_display(val=None):
    idx = int(s_slice.val)
    sl = get_slice(arr, current_slice_axis, idx)
    im_orig.set_data(sl)
    im_seg_bg.set_data(sl)

    if seg_overlay is not None:
        seg_sl = get_slice(seg_overlay, current_slice_axis, idx)
        rgba = np.zeros((*seg_sl.shape, 4), dtype=np.float32)
        mask = seg_sl > 0
        rgba[mask] = [1.0, 0.2, 0.0, 0.65]  # red-orange, visible
        im_seg_ov.set_data(rgba)
    else:
        im_seg_ov.set_data(np.zeros((*sl.shape, 4), dtype=np.float32))

    # Show seed marker — always visible, brighter on seed slice
    seeds_idx = [int(params["seed_z"]), int(params["seed_y"]), int(params["seed_x"])]
    if current_slice_axis == 2:    # axial: x horizontal, y vertical
        mx, my = int(params["seed_x"]), int(params["seed_y"])
    elif current_slice_axis == 1:  # coronal: x horizontal, z vertical
        mx, my = int(params["seed_x"]), int(params["seed_z"])
    else:                          # sagital: y horizontal, z vertical
        mx, my = int(params["seed_y"]), int(params["seed_z"])

    on_seed_slice = (idx == seeds_idx[current_slice_axis])
    alpha = 1.0 if on_seed_slice else 0.3
    for m in [seed_marker_orig, seed_marker_seg]:
        m.set_data([mx], [my])
        m.set_alpha(alpha)
    for c in [seed_circle_orig, seed_circle_seg]:
        c.set_data([mx], [my])
        c.set_alpha(alpha)

    fig.canvas.draw_idle()

def on_run(event):
    params["seed_x"] = int(s_sx.val)
    params["seed_y"] = int(s_sy.val)
    params["seed_z"] = int(s_sz.val)
    if current_method == "ConnectedThreshold":
        params["lower"] = int(s_p1.val)
        params["upper"] = int(s_p2.val)
    else:
        params["iterations"] = int(s_p1.val)
        params["multiplier"] = float(s_p2.val)
        params["radius"] = int(s_p3.val)
    run_segmentation()
    update_display()

def on_method_change(label):
    global current_method
    current_method = label
    if label == "ConnectedThreshold":
        s_p1.ax.set_visible(True)
        s_p2.ax.set_visible(True)
        s_p3.ax.set_visible(False)
        s_p1.label.set_text("Lower")
        s_p1.valmin, s_p1.valmax = 0, 500
        s_p1.set_val(params["lower"])
        s_p2.label.set_text("Upper")
        s_p2.valmin, s_p2.valmax = 0, 500
        s_p2.set_val(params["upper"])
    else:
        s_p1.ax.set_visible(True)
        s_p2.ax.set_visible(True)
        s_p3.ax.set_visible(True)
        s_p1.label.set_text("Iterations")
        s_p1.valmin, s_p1.valmax = 0, 10
        s_p1.set_val(params["iterations"])
        s_p2.label.set_text("Multiplier")
        s_p2.valmin, s_p2.valmax = 0.5, 5.0
        s_p2.set_val(params["multiplier"])
        s_p3.label.set_text("Radius")
        s_p3.valmin, s_p3.valmax = 1, 5
        s_p3.set_val(params["radius"])
    fig.canvas.draw_idle()

def on_axis_change(label):
    global current_slice_axis
    axis_map = {"Sagital": 0, "Coronal": 1, "Axial": 2}
    current_slice_axis = axis_map[label]
    max_s = get_max_slice(current_slice_axis)
    s_slice.valmax = max_s
    s_slice.ax.set_xlim(0, max_s)
    seed_sl = get_seed_slice()
    s_slice.set_val(min(seed_sl, max_s))
    update_display()

s_slice.on_changed(update_display)
btn_run.on_clicked(on_run)
radio.on_clicked(on_method_change)
axis_radio.on_clicked(on_axis_change)

# --- Initial run ---
run_segmentation()
update_display()

print("Interactive viewer ready. Adjust parameters and click 'Run Segmentation'.")
plt.show()
