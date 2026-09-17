"""Generate the sample pipeline figure used by docs/sample-paper."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

OUT = Path("docs/sample-paper/components/figures/fig-pipeline/pipeline.png")

fig, ax = plt.subplots(figsize=(6, 2.8))
boxes = [
    (0.03, 0.55, "components/", "#cfe8ff"),
    (0.30, 0.55, "manifest",    "#ffe7b3"),
    (0.57, 0.55, "template",    "#d5f5d5"),
    (0.30, 0.15, "build.py",    "#f5d5e5"),
    (0.57, 0.15, "main.pdf",    "#e0e0e0"),
]
for x, y, label, color in boxes:
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), 0.20, 0.28,
        boxstyle="round,pad=0.02",
        linewidth=1, edgecolor="#333", facecolor=color))
    ax.text(x + 0.10, y + 0.14, label, ha="center", va="center",
            fontsize=10, family="monospace")

def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#333"))

arrow(0.23, 0.69, 0.30, 0.69)
arrow(0.50, 0.69, 0.57, 0.69)
arrow(0.67, 0.55, 0.67, 0.43)
arrow(0.50, 0.29, 0.57, 0.29)
arrow(0.40, 0.55, 0.40, 0.43)

ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.axis("off")
plt.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(OUT, dpi=200)
print(f"wrote {OUT}")
