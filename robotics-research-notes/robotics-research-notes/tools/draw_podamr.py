# Regenerate the diagram from the repository root:  python tools/draw_podamr.py
# Requires: pip install matplotlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Wedge

fig, ax = plt.subplots(figsize=(17, 8.2), dpi=130)
ax.set_xlim(-0.3, 18.3); ax.set_ylim(-2.6, 8.2); ax.set_aspect("equal"); ax.axis("off")
TXT = "#212121"

def label(text, xy, xytext, ha="left"):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=9.2, color=TXT, ha=ha, va="center", zorder=20,
                arrowprops=dict(arrowstyle="-|>", color="#546E7A", lw=1.0, shrinkA=2, shrinkB=2),
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#B0BEC5", lw=0.8))

ax.text(9, 7.85, "Generic tower (pod) lifting AMR - illustrative concept (side view)", ha="center",
        fontsize=15, fontweight="bold", color=TXT)
ax.text(9, 7.4, "Original schematic of the goods-to-person principle - not the design of any specific commercial product",
        ha="center", fontsize=10, style="italic", color="#616161")

def floor(ox):
    ax.plot([ox - 0.1, ox + 5.7], [0, 0], color="#5D4037", lw=2)
    for fx in [0.4, 1.9, 3.4, 4.9]:
        ax.add_patch(Rectangle((ox + fx, -0.02), 0.22, 0.06, fc="#212121", zorder=3))

def tower(ox, dz):
    for lx in [1.0, 4.4]:
        ax.add_patch(Rectangle((ox + lx, dz), 0.2, 5.2, fc="#455A64", zorder=12))
    for sy in [1.42, 2.62, 3.82, 5.02]:
        ax.add_patch(Rectangle((ox + 1.0, dz + sy), 3.6, 0.1, fc="#607D8B", zorder=5))
    box_rows = [(1.52, [0.25, 1.35, 2.35]), (2.72, [0.3, 1.5]), (3.92, [0.25, 1.25, 2.3]), (5.12, [0.6, 1.9])]
    for sy, xs in box_rows:
        for bx in xs:
            ax.add_patch(Rectangle((ox + 1.0 + bx, dz + sy), 0.9, 0.75, fc="#D7B98E", ec="#8D6E63", lw=1, zorder=4))
    # fiducial under bottom shelf
    ax.add_patch(Rectangle((ox + 2.62, dz + 1.33), 0.36, 0.09, fc="white", ec="#212121", lw=0.8, zorder=7))
    ax.add_patch(Rectangle((ox + 2.62, dz + 1.33), 0.12, 0.09, fc="#212121", zorder=8))
    ax.add_patch(Rectangle((ox + 2.86, dz + 1.33), 0.12, 0.09, fc="#212121", zorder=8))

def amr(x0, lift):
    ax.add_patch(FancyBboxPatch((x0, 0.2), 2.6, 0.72, boxstyle="round,pad=0.03", fc="#BBDEFB", ec="#1565C0", lw=1.5, zorder=9))
    for wx in [0.55, 2.05]:
        ax.add_patch(Circle((x0 + wx, 0.2), 0.19, fc="#424242", ec="#212121", zorder=10))
    if lift > 0:
        ax.add_patch(Rectangle((x0 + 1.12, 0.95), 0.36, lift, fc="#FFB74D", ec="#E65100", zorder=9))
    ax.add_patch(Rectangle((x0 + 0.6, 0.95 + lift), 1.4, 0.1, fc="#FB8C00", ec="#E65100", zorder=10))
    ax.add_patch(Rectangle((x0 + 1.22, 1.05 + lift), 0.16, 0.07, fc="#8E24AA", zorder=11))  # up camera
    ax.add_patch(Rectangle((x0 + 1.2, 0.12), 0.2, 0.08, fc="#8E24AA", zorder=11))  # down camera
    ax.add_patch(Wedge((x0 + 2.62, 0.6), 0.17, -90, 90, fc="#8E24AA", zorder=11))  # safety lidar
    ax.add_patch(Rectangle((x0 + 0.25, 0.4), 0.7, 0.3, fc="#C8E6C9", ec="#2E7D32", lw=0.8, zorder=10))

# panel 1
o1 = 0.0; floor(o1); tower(o1, 0.0); amr(o1 - 0.05, 0.0)
ax.annotate("", xy=(o1 + 3.6, -0.4), xytext=(o1 + 1.6, -0.4), arrowprops=dict(arrowstyle="-|>", lw=2.2, color="#1565C0"))
ax.text(o1 + 2.8, 6.7, "1) Drive under the tower", ha="center", fontsize=12, fontweight="bold", color="#0D47A1")

# panel 2
o2 = 6.2; dz = 0.23; floor(o2); tower(o2, dz); amr(o2 + 1.5, 0.6)
ax.text(o2 + 2.8, 6.7, "2) Lift the tower 2-5 cm", ha="center", fontsize=12, fontweight="bold", color="#0D47A1")
for lx in [1.1, 4.5]:
    ax.annotate("", xy=(o2 + lx, dz + 0.02), xytext=(o2 + lx, 0.0), arrowprops=dict(arrowstyle="<->", lw=0.9, color="#D32F2F"))

# panel 3
o3 = 12.4; floor(o3); tower(o3 + 0.25, dz); amr(o3 + 1.75, 0.6)
ax.text(o3 + 2.8, 6.7, "3) Carry it to station / storage", ha="center", fontsize=12, fontweight="bold", color="#0D47A1")
ax.annotate("", xy=(o3 + 5.9, 3.3), xytext=(o3 + 4.95, 3.3), arrowprops=dict(arrowstyle="-|>", lw=2.6, color="#1565C0"))
for yy in [2.4, 3.0, 3.6, 4.2]:
    ax.plot([o3 + 0.35, o3 + 0.95], [yy, yy], color="#90A4AE", lw=1.4)

# callouts
label("Tower = rack / pod on 4 legs;\nclear height > robot height", (o1 + 1.1, 3.0), (o1 - 0.25, -1.15))
label("Low-profile AMR passes\nbetween the legs", (o1 + 0.6, 0.75), (o1 - 0.25, -2.3))
label("Lift plate on screw / cam jack\n(carries the full tower load)", (o2 + 2.6, 1.6), (o2 - 1.6, -1.15))
label("Up-camera reads tower\nfiducial (alignment + ID)", (o2 + 3.0, 1.75), (o2 + 3.7, -1.15))
label("Down-camera reads floor 2D codes\n(or use LiDAR SLAM)", (o2 + 2.8, 0.13), (o2 + 1.2, -2.3))
label("Safety LiDAR /\nbumper", (o3 + 4.5, 0.62), (o3 + 3.75, -1.15))
label("Battery + drive electronics\ninside the chassis", (o3 + 2.3, 0.55), (o3 + 0.55, -1.15))
label("Differential-drive wheels\n(+ casters): rotate in place", (o3 + 2.3, 0.15), (o3 + 1.3, -2.3))

plt.savefig("images/tower_lifting_amr_generic.png", bbox_inches="tight", facecolor="white")
print("ok")
