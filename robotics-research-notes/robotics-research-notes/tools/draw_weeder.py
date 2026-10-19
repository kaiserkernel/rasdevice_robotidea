# Regenerate the diagram from the repository root:  python tools/draw_weeder.py
# Requires: pip install matplotlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse, Polygon, FancyBboxPatch

C = dict(frame="#37474F", body="#BBDEFB", bodye="#1565C0", act="#FB8C00", sens="#8E24AA",
         soil="#D7CCC8", soile="#8D6E63", crop="#2E7D32", weed="#9E9D24", laser="#E53935",
         txt="#212121", hood="#ECEFF1", batt="#C8E6C9")

fig, ax = plt.subplots(figsize=(16, 10.3), dpi=130)
ax.set_xlim(0, 16); ax.set_ylim(-2.35, 9.0); ax.set_aspect("equal"); ax.axis("off")

def label(text, xy, xytext, ha="left"):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=9.5, color=C["txt"], ha=ha, va="center",
                arrowprops=dict(arrowstyle="-|>", color="#546E7A", lw=1.0, shrinkA=2, shrinkB=2),
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#B0BEC5", lw=0.8))

ax.text(8, 8.6, "Generic AI weeding robot - illustrative mechanical layout (side view)",
        ha="center", fontsize=15, fontweight="bold", color=C["txt"])
ax.text(8, 8.15, "Original schematic for concept discussion - not the design of any specific commercial product",
        ha="center", fontsize=10, style="italic", color="#616161")

# soil + ground
ax.add_patch(Rectangle((0.3, 0.55), 15.4, 0.65, fc=C["soil"], ec="none"))
ax.plot([0.3, 15.7], [1.2, 1.2], color=C["soile"], lw=2)

def crop(x):
    ax.plot([x, x], [1.2, 1.55], color=C["crop"], lw=2)
    for dx, ang in [(-0.22, 25), (0.22, -25), (0, 90)]:
        ax.add_patch(Ellipse((x + dx, 1.62 if dx else 1.75), 0.5 if dx else 0.22, 0.2 if dx else 0.45,
                             angle=ang if dx else 0, fc=C["crop"], ec="#1B5E20", lw=0.8))

def weed(x):
    pts = [(x - 0.2, 1.2), (x - 0.12, 1.45), (x - 0.05, 1.28), (x, 1.55), (x + 0.06, 1.3), (x + 0.14, 1.48), (x + 0.2, 1.2)]
    ax.add_patch(Polygon(pts, closed=True, fc=C["weed"], ec="#6B6B00", lw=0.8))

for x in [1.0, 3.6, 6.2, 8.8, 11.4, 14.6]:
    crop(x)
for x in [2.3, 5.0, 7.4, 9.9, 12.9]:
    weed(x)

# wheels + legs
for wx in [2.4, 12.6]:
    ax.add_patch(Rectangle((wx - 0.17, 2.1), 0.34, 2.15, fc=C["frame"], ec="none"))
    ax.add_patch(Circle((wx, 2.12), 0.92, fc="#424242", ec="#212121", lw=1.5))
    ax.add_patch(Circle((wx, 2.12), 0.42, fc="#9E9E9E", ec="#616161", lw=1))
    ax.add_patch(Circle((wx, 2.12), 0.18, fc=C["act"], ec="#E65100", lw=1))

# main frame
ax.add_patch(Rectangle((1.8, 4.2), 11.4, 0.4, fc=C["frame"], ec="none"))
# battery + compute
ax.add_patch(FancyBboxPatch((3.0, 4.62), 2.9, 0.8, boxstyle="round,pad=0.02", fc=C["batt"], ec="#2E7D32", lw=1.2))
ax.text(4.45, 5.02, "BATTERY", ha="center", va="center", fontsize=9, fontweight="bold", color="#1B5E20")
ax.add_patch(FancyBboxPatch((6.3, 4.62), 2.4, 0.7, boxstyle="round,pad=0.02", fc=C["body"], ec=C["bodye"], lw=1.2))
ax.text(7.5, 4.97, "AI COMPUTER", ha="center", va="center", fontsize=9, fontweight="bold", color="#0D47A1")
# solar panel on struts
for sx in [3.4, 9.6]:
    ax.plot([sx, sx], [4.6, 6.05], color=C["frame"], lw=2)
ax.add_patch(Rectangle((2.6, 6.05), 7.8, 0.22, fc="#1A237E", ec="#0D1442", lw=1))
for k in range(1, 12):
    ax.plot([2.6 + k * 0.65, 2.6 + k * 0.65], [6.05, 6.27], color="#5C6BC0", lw=0.6)
# GNSS mast
ax.plot([11.2, 11.2], [4.6, 7.0], color=C["frame"], lw=2.2)
ax.add_patch(Ellipse((11.2, 7.05), 0.7, 0.22, fc=C["sens"], ec="#4A148C"))
# e-stop
ax.add_patch(Circle((12.85, 4.85), 0.18, fc="#D32F2F", ec="#7F0000"))
# front nav sensor
ax.add_patch(Rectangle((13.2, 3.55), 0.55, 0.5, fc=C["sens"], ec="#4A148C"))
ax.plot([13.75, 14.6], [3.8, 3.3], color=C["sens"], lw=0.8, ls="--")
ax.plot([13.75, 14.6], [3.8, 4.3], color=C["sens"], lw=0.8, ls="--")

# camera hood (trapezoid) + camera + view cone
ax.add_patch(Polygon([(4.2, 4.2), (6.6, 4.2), (6.95, 1.75), (3.85, 1.75)], closed=True,
                     fc=C["hood"], ec="#78909C", lw=1.5, alpha=0.95))
ax.add_patch(Rectangle((5.1, 3.75), 0.6, 0.42, fc=C["sens"], ec="#4A148C"))
ax.add_patch(Rectangle((5.28, 3.6), 0.24, 0.16, fc="#212121"))
ax.plot([5.4, 4.0], [3.6, 1.3], color=C["sens"], lw=0.9, ls="--")
ax.plot([5.4, 6.8], [3.6, 1.3], color=C["sens"], lw=0.9, ls="--")
for lx in [4.35, 6.3]:
    ax.add_patch(Rectangle((lx, 3.95), 0.25, 0.12, fc="#FFEB3B", ec="#F9A825"))

# tool gantry: rail + carriage + laser head
ax.add_patch(Rectangle((8.4, 4.0), 0.15, 0.2, fc=C["frame"])); ax.add_patch(Rectangle((11.25, 4.0), 0.15, 0.2, fc=C["frame"]))
ax.add_patch(Rectangle((8.3, 3.72), 3.2, 0.28, fc="#90A4AE", ec="#455A64", lw=1))
ax.add_patch(Rectangle((9.6, 3.2), 0.85, 0.52, fc=C["act"], ec="#E65100", lw=1.2))
ax.add_patch(Rectangle((9.88, 2.82), 0.3, 0.4, fc="#5D4037", ec="#3E2723"))
ax.plot([10.03, 9.92], [2.82, 1.42], color=C["laser"], lw=2.2)
ax.plot([9.92], [1.42], marker="*", ms=16, color="#FF7043", mec="#BF360C")

# travel arrow
ax.annotate("", xy=(15.2, 7.7), xytext=(13.2, 7.7), arrowprops=dict(arrowstyle="-|>", lw=2.5, color="#2E7D32"))
ax.text(14.2, 7.95, "Direction of travel", ha="center", fontsize=10, color="#2E7D32", fontweight="bold")

# labels (callouts placed in free space)
label("Solar panel (optional, extends runtime)", (6.5, 6.27), (0.25, 7.25))
label("GNSS-RTK antenna (cm-level positioning,\nrow following, weed map logging)", (11.2, 7.15), (11.9, 6.55))
label("Battery pack + BMS", (3.6, 5.3), (0.25, 6.3))
label("Edge-AI computer (GPU/NPU) +\nmotor & tool controllers", (7.5, 5.32), (5.0, 7.25))
label("Emergency stop + bumper", (12.85, 5.0), (13.25, 5.6))
label("Forward camera / LiDAR\n(navigation, obstacle stop)", (13.5, 3.6), (13.9, 2.55))
label("Portal frame straddles\nthe crop row", (2.0, 4.4), (0.25, 3.35))
label("Drive wheel + hub motor\n& gearbox (x4, 2WS/4WS)", (2.4, 1.6), (0.25, 0.05))
label("Light hood + LED strobe:\nconstant lighting for the CNN", (6.75, 3.0), (6.15, -0.2))
label("Downward RGB camera(s)\n(crop vs weed detection)", (5.15, 3.9), (2.9, -0.95))
label("Tool carriage on cross-row\nlinear axis (belt / lead-screw)", (10.9, 3.86), (12.0, -0.25))
label("Weeding tool (choose one):\n1) laser emitter, galvo-steered\n2) hoe / finger weeder on Z-axis\n3) micro-spray solenoid nozzle", (10.03, 3.0), (9.0, -1.05))

# pipeline strip
ax.text(0.25, -2.1, "Control loop:  camera frame  ->  CNN detects crop vs weed  ->  pixel-to-ground calibration  ->  "
        "motion compensation (odometry / RTK)  ->  aim & actuate tool  ->  verify hit",
        fontsize=9.5, color="#37474F", style="italic")

plt.savefig("images/weeding_robot_generic.png", bbox_inches="tight", facecolor="white")
print("ok")
