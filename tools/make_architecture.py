import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(6, 3.2))
boxes = [
    (0.05, 0.55, "components/", "#cfe8ff"),
    (0.40, 0.55, "manifest",     "#ffe7b3"),
    (0.72, 0.55, "template",     "#d5f5d5"),
    (0.40, 0.15, "build.py",     "#f5d5e5"),
    (0.72, 0.15, "main.pdf",     "#e0e0e0"),
]
for x, y, label, color in boxes:
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), 0.22, 0.28,
        boxstyle="round,pad=0.02",
        linewidth=1, edgecolor="#333", facecolor=color))
    ax.text(x + 0.11, y + 0.14, label, ha="center", va="center",
            fontsize=10, family="monospace")

def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#333"))

arrow(0.27, 0.69, 0.40, 0.69)
arrow(0.62, 0.69, 0.72, 0.69)
arrow(0.83, 0.55, 0.83, 0.43)
arrow(0.62, 0.29, 0.72, 0.29)
arrow(0.51, 0.55, 0.51, 0.43)

ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.axis("off")
plt.tight_layout()
plt.savefig("components/figures/fig-architecture/architecture.png", dpi=200)
print("wrote components/figures/fig-architecture/architecture.png")
