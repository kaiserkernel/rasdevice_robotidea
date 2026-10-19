# Regenerate the diagram from the repository root:  python tools/draw_bottomstack.py
# Requires: pip install matplotlib
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch

fig, ax = plt.subplots(figsize=(21.5, 19.0), dpi=110)
ax.set_xlim(-0.7, 25.6); ax.set_ylim(-3.6, 20.4); ax.set_aspect("equal"); ax.axis("off")
TXT = "#212121"; PAWL = "#C62828"; NEW = "#FFE0B2"; NEWE = "#E65100"; OLD = "#D7B98E"; OLDE = "#8D6E63"
PW = 4.9           # panel pitch
P_OFF = 2.0        # pawl top surface height above floor
H = 1.0            # box pitch (flange 0.1 + body 0.9)

def label(text, xy, xytext, ha="left", fs=9):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=fs, color=TXT, ha=ha, va="center", zorder=30,
                arrowprops=dict(arrowstyle="-|>", color="#546E7A", lw=1.0, shrinkA=2, shrinkB=2),
                bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="#B0BEC5", lw=0.8))

def rot(pts, pivot, deg):
    a = math.radians(deg); px, py = pivot
    return [(px + (x - px) * math.cos(a) - (y - py) * math.sin(a), py + (x - px) * math.sin(a) + (y - py) * math.cos(a)) for x, y in pts]

def frame(ox, base):
    ax.plot([ox - 0.15, ox + 4.15], [base, base], color="#5D4037", lw=2)
    for x0 in [0.6, 3.2]:
        ax.add_patch(Rectangle((ox + x0, base), 0.2, 6.9, fc="#455A64", zorder=8))

def pawls(ox, base, state):
    P = base + P_OFF
    left = [(ox + 0.8, P), (ox + 1.05, P), (ox + 0.8, P - 0.32)]
    right = [(ox + 3.2, P), (ox + 2.95, P), (ox + 3.2, P - 0.32)]
    if state == "up":       # deflected by a rising flange (one-way)
        left = rot(left, (ox + 0.8, P), 62); right = rot(right, (ox + 3.2, P), -62)
    if state == "out":      # retracted into the post by the release actuator
        left = [(x - 0.26, y) for x, y in left]; right = [(x + 0.26, y) for x, y in right]
    for pts in (left, right):
        ax.add_patch(Polygon(pts, closed=True, fc=PAWL if state != "out" else "none", ec=PAWL, lw=1.4,
                             ls="-" if state != "out" else "--", zorder=12))
    if state == "out":
        ax.annotate("", xy=(ox + 0.25, P - 0.12), xytext=(ox + 0.75, P - 0.12), arrowprops=dict(arrowstyle="-|>", color=PAWL, lw=1.4), zorder=13)
        ax.annotate("", xy=(ox + 3.75, P - 0.12), xytext=(ox + 3.25, P - 0.12), arrowprops=dict(arrowstyle="-|>", color=PAWL, lw=1.4), zorder=13)
    for x0 in [0.42, 3.4]:   # release actuators on the posts
        ax.add_patch(Rectangle((ox + x0, P - 0.3), 0.18, 0.3, fc="#8E24AA", ec="#4A148C", lw=0.8, zorder=11))

def box(ox, y0, name, new=False):
    fc, ec = (NEW, NEWE) if new else (OLD, OLDE)
    ax.add_patch(Rectangle((ox + 0.85, y0), 2.3, 0.1, fc=fc, ec=ec, lw=1.2, zorder=10))
    ax.add_patch(Rectangle((ox + 1.1, y0 + 0.1), 1.8, 0.9, fc=fc, ec=ec, lw=1.2, zorder=10))
    ax.text(ox + 2.0, y0 + 0.55, name, ha="center", va="center", fontsize=10, fontweight="bold", color=ec, zorder=11)

def robot(ox, base, plat_top):
    ax.add_patch(FancyBboxPatch((ox + 0.95, base + 0.17), 2.1, 0.55, boxstyle="round,pad=0.03", fc="#BBDEFB", ec="#1565C0", lw=1.4, zorder=14))
    for wx in [1.3, 2.7]:
        ax.add_patch(Circle((ox + wx, base + 0.17), 0.16, fc="#424242", ec="#212121", zorder=15))
    yb0 = base + 0.74; yb = plat_top - 0.08
    if yb > yb0 + 0.02:
        n = max(1, math.ceil((yb - yb0) / 0.6)); h = (yb - yb0) / n
        for k in range(n):
            y1, y2 = yb0 + k * h, yb0 + (k + 1) * h
            ax.plot([ox + 1.4, ox + 2.6], [y1, y2], color="#EF6C00", lw=1.6, zorder=13)
            ax.plot([ox + 2.6, ox + 1.4], [y1, y2], color="#EF6C00", lw=1.6, zorder=13)
    ax.add_patch(Rectangle((ox + 1.2, yb), 1.6, 0.08, fc="#FB8C00", ec="#E65100", zorder=16))

def panel(i, row_base, title, plat_top, stack, pawl_state, new_name=None, move=None):
    ox = i * PW
    frame(ox, row_base); pawls(ox, row_base, pawl_state); robot(ox, row_base, plat_top)
    for y0, name in stack:
        box(ox, y0, name, new=(name == new_name))
    ax.text(ox + 2.0, row_base + 7.55, title, ha="center", va="center", fontsize=10.2, color="#0D47A1", fontweight="bold")
    if move:
        ax.annotate("", xy=(ox + move[1], row_base - 0.35), xytext=(ox + move[0], row_base - 0.35),
                    arrowprops=dict(arrowstyle="-|>", lw=2, color="#1565C0"))

ax.text(12.4, 20.1, "Bottom push / pop cargo tower - mechanism concept for your robot", ha="center", fontsize=16, fontweight="bold", color=TXT)
ax.text(12.4, 19.55, "Original concept sketch (side view). Tower is passive (posts + one-way pawls); all lifting is done by the mobile robot.",
        ha="center", fontsize=10.5, style="italic", color="#616161")

# ---------- Row A : PUSH (insert) ----------
A = 10.4; PA = A + P_OFF; REST = A + 0.83
ax.text(-0.6, A + 8.45, "A) PUSH a new box in from the bottom  (insert uses passive one-way pawls - no actuator needed)",
        fontsize=12.5, fontweight="bold", color="#2E7D32")
panel(0, A, "1) Robot drives under the\ntower carrying new box B0", REST,
      [(REST, "B0"), (PA, "B1"), (PA + 1, "B2"), (PA + 2, "B3")], "in", "B0", move=(-0.4, 1.4))
y0 = PA - 0.05
panel(1, A, "2) Lift: B0 pushes the whole\nstack up; pawls swing aside", y0,
      [(y0, "B0"), (y0 + 1, "B1"), (y0 + 2, "B2"), (y0 + 3, "B3")], "up", "B0")
y0 = PA + 0.14
panel(2, A, "3) B0's flange clears the pawls;\nthey drop back underneath", y0,
      [(y0, "B0"), (y0 + 1, "B1"), (y0 + 2, "B2"), (y0 + 3, "B3")], "in", "B0")
panel(3, A, "4) Lower platform: stack rests\non pawls; robot drives away", A + 0.83,
      [(PA, "B0"), (PA + 1, "B1"), (PA + 2, "B2"), (PA + 3, "B3")], "in", "B0", move=(2.6, 4.4))

# ---------- Row B : POP (remove bottom box) ----------
B = 0.0; PB = B + P_OFF
ax.text(-0.6, B + 8.45, "B) POP the bottom box  (needs a pawl-release actuator: solenoid on the tower, or a lever pushed by the robot)",
        fontsize=12.5, fontweight="bold", color="#C62828")
y0 = PB + 0.1
panel(0, B, "1) Empty platform rises and\ntakes the stack load (+5 mm)", y0,
      [(y0, "B0"), (y0 + 1, "B1"), (y0 + 2, "B2"), (y0 + 3, "B3")], "in", "B0")
panel(1, B, "2) Release actuators pull\nthe pawls out of the way", y0,
      [(y0, "B0"), (y0 + 1, "B1"), (y0 + 2, "B2"), (y0 + 3, "B3")], "out", "B0")
y0 = PB + 0.1 - H
panel(2, B, "3) Lower exactly one pitch;\npawls re-engage under B1", y0,
      [(y0, "B0"), (y0 + 1, "B1"), (y0 + 2, "B2"), (y0 + 3, "B3")], "in", "B0")
panel(3, B, "4) Lower to rest: B1..B3 stay;\nrobot leaves with B0", B + 0.83,
      [(B + 0.83, "B0"), (PB, "B1"), (PB + 1, "B2"), (PB + 2, "B3")], "in", "B0", move=(2.6, 4.4))

# legend column (replaces callouts)
LX = 19.9; LY = A + 6.6
ax.add_patch(FancyBboxPatch((LX - 0.3, B + 0.2), 5.9, A + 7.0 - B, boxstyle="round,pad=0.1", fc="#FAFAFA", ec="#B0BEC5", lw=1))
ax.text(LX, LY + 0.25, "Legend", fontsize=12, fontweight="bold", color=TXT, va="center")
def leg(y, draw, text):
    draw(y); ax.text(LX + 1.25, y, text, fontsize=9.6, color=TXT, va="center", linespacing=1.35)
leg(LY - 1.3, lambda y: ax.add_patch(Polygon([(LX, y + 0.2), (LX + 0.6, y + 0.2), (LX, y - 0.45)], fc=PAWL, ec=PAWL)),
    "One-way pawl (gravity or spring):\nflat top carries the stack; sloped\nunderside lets a rising box push\nit aside (insert needs no actuator)")
leg(LY - 3.25, lambda y: ax.add_patch(Rectangle((LX + 0.15, y - 0.35), 0.3, 0.7, fc="#8E24AA", ec="#4A148C")),
    "Pawl-release actuator (solenoid,\nor lever pushed by the robot):\nneeded only for POP")
def tote(y):
    ax.add_patch(Rectangle((LX - 0.15, y - 0.4), 0.95, 0.07, fc=NEW, ec=NEWE)); ax.add_patch(Rectangle((LX, y - 0.33), 0.65, 0.7, fc=NEW, ec=NEWE))
leg(LY - 5.05, tote, "Cargo tote / tray with a protruding\nbottom flange (what the pawls hook)")
def lift(y):
    ax.plot([LX, LX + 0.65], [y - 0.4, y + 0.25], color="#EF6C00", lw=1.8); ax.plot([LX + 0.65, LX], [y - 0.4, y + 0.25], color="#EF6C00", lw=1.8)
    ax.add_patch(Rectangle((LX - 0.08, y + 0.25), 0.8, 0.1, fc="#FB8C00", ec="#E65100"))
leg(LY - 6.85, lift, "Scissor / screw lift on the robot:\nmust carry the WHOLE stack")
def bot(y):
    ax.add_patch(FancyBboxPatch((LX - 0.1, y - 0.25), 0.85, 0.42, boxstyle="round,pad=0.03", fc="#BBDEFB", ec="#1565C0"))
    ax.add_patch(Circle((LX + 0.1, y - 0.27), 0.11, fc="#424242")); ax.add_patch(Circle((LX + 0.55, y - 0.27), 0.11, fc="#424242"))
leg(LY - 8.45, bot, "Mobile robot: drives under the\ntower (open front / back)")
leg(LY - 9.95, lambda y: ax.add_patch(Rectangle((LX + 0.2, y - 0.5), 0.2, 1.0, fc="#455A64")),
    "Passive tower frame: 4 posts,\nno motors, cheap to replicate")
leg(LY - 11.55, lambda y: ax.annotate("", xy=(LX + 0.8, y), xytext=(LX - 0.1, y), arrowprops=dict(arrowstyle="-|>", lw=2, color="#1565C0")),
    "Robot drive direction")
leg(LY - 13.05, lambda y: [ax.add_patch(Rectangle((LX + 0.05, y - 0.35), 0.55, 0.7, fc=OLD, ec=OLDE))],
    "Boxes already in the tower;\nB0 (orange) = box being moved")

notes = ("Design notes:  (1) standardise the cargo carrier - totes or trays with a protruding flange or side slots - so pawls can catch every unit.  "
         "(2) Size the lift for the FULL stack: e.g. 8 boxes x 25 kg = 200 kg plus a safety factor.\n"
         "(3) Add a sensor per pawl (engaged / retracted) and a load cell or motor-current check on the lift; never release pawls unless the lift is carrying the load.  "
         "(4) To relocate a full tower, give the\nrobot a second wide docking plate that lifts the tower frame itself by 2-5 cm (same principle as the tower-lifting AMR figure).  "
         "(5) The pitch H must be constant, so the lift needs an encoder / absolute position.")
ax.text(-0.6, -2.25, notes, fontsize=9.4, color="#37474F", va="center",
        bbox=dict(boxstyle="round,pad=0.5", fc="#FAFAFA", ec="#B0BEC5"))

plt.savefig("images/bottom_push_pop_tower_concept.png", bbox_inches="tight", facecolor="white")
print("ok")
