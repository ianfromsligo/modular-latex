"""Generate all sample figures for the sample docs."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path


def _save(fig, out):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out}")


def paper_overview():
    fig, ax = plt.subplots(figsize=(5.5, 3))
    ax.text(0.5, 0.85, "U  =  U_k  x  U_m", ha="center", va="center",
            fontsize=15, family="monospace")
    ax.text(0.25, 0.42, "U_k", ha="center", va="center", fontsize=17,
            bbox=dict(boxstyle="round,pad=0.35", fc="#cfe8ff", ec="#333"))
    ax.text(0.75, 0.42, "U_m", ha="center", va="center", fontsize=17,
            bbox=dict(boxstyle="round,pad=0.35", fc="#d5f5d5", ec="#333"))
    ax.annotate("", xy=(0.32, 0.5), xytext=(0.44, 0.78),
                arrowprops=dict(arrowstyle="->", color="#333"))
    ax.annotate("", xy=(0.68, 0.5), xytext=(0.56, 0.78),
                arrowprops=dict(arrowstyle="->", color="#333"))
    ax.text(0.25, 0.15, "x-direction", ha="center", fontsize=9)
    ax.text(0.75, 0.15, "y-direction", ha="center", fontsize=9)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    _save(fig, "docs/sample-paper/components/figures/fig-overview/overview.png")


def paper_results():
    fig, ax = plt.subplots(figsize=(5.5, 3))
    sizes = ["2", "3", "4", "5", "8", "10"]
    periods = [2, 30, 24, 60, 24, 60]
    ax.bar(sizes, periods, color="#cfe8ff", edgecolor="#333")
    ax.set_xlabel("Torus dimension L (L x L)")
    ax.set_ylabel("Maximum period T")
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    _save(fig, "docs/sample-paper/components/figures/fig-results/results.png")


def experiment_revival_plot():
    fig, ax = plt.subplots(figsize=(5, 3))
    states = ["Phi+", "Phi-", "Psi+", "Psi-"]
    periods = [24, 8, 24, 24]
    colors = ["#cfe8ff", "#ffd7b3", "#cfe8ff", "#cfe8ff"]
    ax.bar(states, periods, color=colors, edgecolor="#333")
    ax.set_ylabel("Fundamental period N")
    ax.set_xlabel("Bell state")
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    _save(fig, "docs/sample-experiment/components/figures/fig-revival-plot/revival-plot.png")


if __name__ == "__main__":
    paper_overview()
    paper_results()
    experiment_revival_plot()
