"""Generate figures for the sep-coin-tori paper."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle
from pathlib import Path
import numpy as np


BASE = Path("docs/sep-coin-tori/components/figures")


def save(fig, rel):
    out = BASE / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=220, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out}")


def one_step():
    """One coin toss + one shift on a 3x3 torus, starting from |RU>."""
    rho = 2 / 3
    sqrt_r = np.sqrt(rho)          # sqrt(2/3)
    sqrt_1mr = np.sqrt(1 - rho)    # sqrt(1/3)

    # Amplitudes in basis order |LD>, |LU>, |RD>, |RU>.
    # C_x |R> =  sqrt(1/3)|L> - sqrt(2/3)|R>
    # C_y |U> =  sqrt(1/3)|D> - sqrt(2/3)|U>
    # Tensor product -> four amplitudes.
    amps = {
        "LD": ( sqrt_1mr *  sqrt_1mr, (-1, -1)),  # +1/3
        "LU": ( sqrt_1mr * -sqrt_r,   (-1, +1)),  # -sqrt(2)/3
        "RD": (-sqrt_r  *  sqrt_1mr,  (+1, -1)),  # -sqrt(2)/3
        "RU": (-sqrt_r  * -sqrt_r,    (+1, +1)),  # +2/3
    }

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 5.2))

    # ==================================================================
    # Panel (a): coin toss, arrows at 45 degrees to the four diagonal
    # neighbouring nodes
    # ==================================================================
    ax1.set_xlim(-2.2, 2.2)
    ax1.set_ylim(-2.4, 2.4)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_title("(a) Coin toss: split from $|RU\\rangle$ at $(0,0)$",
                  fontsize=11)

    # central origin node
    ax1.add_patch(Circle((0, 0), 0.13, fc="#222", ec="none"))
    ax1.text(0, 0, "00", color="white", ha="center", va="center",
             fontsize=8, fontweight="bold")

    # labels for the four diagonal destinations
    dest_offsets = {
        "LD": (-1, -1),
        "LU": (-1, +1),
        "RD": (+1, -1),
        "RU": (+1, +1),
    }
    dest_colours = {
        "LD": "#8e44ad",
        "LU": "#2980b9",
        "RD": "#e67e22",
        "RU": "#c0392b",
    }
    arrow_length = 1.25
    for key, (dx, dy) in dest_offsets.items():
        col = dest_colours[key]
        # arrow from origin to destination (diagonal)
        tip = (dx * arrow_length / np.sqrt(2) * np.sqrt(2),
               dy * arrow_length / np.sqrt(2) * np.sqrt(2))
        # simpler: tip = (dx * 1.0, dy * 1.0) for a unit-diagonal
        tip = (dx * 1.0, dy * 1.0)
        arrow = FancyArrowPatch(
            (0, 0), tip,
            arrowstyle="-|>", mutation_scale=20,
            color=col, linewidth=2.0)
        ax1.add_patch(arrow)

        # destination node marker
        ax1.add_patch(Circle(tip, 0.07, fc=col, ec="none"))
        # label just beyond the destination node
        lx, ly = dx * 1.45, dy * 1.35
        amp = amps[key][0]
        # format amplitude nicely
        if key == "LD":
            amp_str = r"$+\frac{1}{3}$"
        elif key == "RU":
            amp_str = r"$+\frac{2}{3}$"
        else:
            amp_str = r"$-\frac{\sqrt{2}}{3}$"
        ax1.text(lx, ly + 0.15, f"$|{key}\\rangle$",
                 ha="center", va="center", fontsize=10,
                 color=col, fontweight="bold")
        ax1.text(lx, ly - 0.20, amp_str,
                 ha="center", va="center", fontsize=9,
                 color=col)

    # parameter line
    ax1.text(0, -1.75,
             r"$\rho_x=\rho_y=2/3$, $\delta_x=\delta_y=0$",
             ha="center", va="center", fontsize=9)

    # equation
    ax1.text(0, -2.15,
             r"$|RU\rangle \to \frac{1}{3}|LD\rangle "
             r"- \frac{\sqrt{2}}{3}|LU\rangle "
             r"- \frac{\sqrt{2}}{3}|RD\rangle "
             r"+ \frac{2}{3}|RU\rangle$",
             ha="center", va="center", fontsize=9)

    # caption
    ax1.text(0, -2.60,
             "(a) Positions and spin after one coin toss.\n"
             "Amplitude is split over the four diagonal directions.",
             ha="center", va="top", fontsize=8.5, style="italic")

    # ==================================================================
    # Panel (b): shift on 3x3 torus, branches move to their nodes
    # ==================================================================
    ax2.set_xlim(-1.2, 3.7)
    ax2.set_ylim(-1.2, 3.7)
    ax2.set_aspect("equal")
    ax2.axis("off")
    ax2.set_title("(b) Shift: branches to nodes on $3\\times 3$ torus",
                  fontsize=11)

    # draw 3x3 grid
    for i in range(3):
        for j in range(3):
            ax2.add_patch(Rectangle((i, j), 1, 1,
                                    fill=False, edgecolor="#bbb",
                                    linewidth=0.8))

    # origin highlighted
    ax2.add_patch(Rectangle((0, 0), 1, 1,
                            fill=True, facecolor="#fff3b0",
                            edgecolor="#333", linewidth=1.4))
    ax2.text(0.5, 0.5, "start\n$|RU\\rangle$",
             ha="center", va="center", fontsize=8,
             fontweight="bold")

    # destinations and amplitudes
    dests = [
        ("LD", 2, 2, r"$+\frac{1}{3}$",     "#8e44ad"),
        ("LU", 2, 1, r"$-\frac{\sqrt{2}}{3}$", "#2980b9"),
        ("RD", 1, 2, r"$-\frac{\sqrt{2}}{3}$", "#e67e22"),
        ("RU", 1, 1, r"$+\frac{2}{3}$",     "#c0392b"),
    ]
    origin = (0.5, 0.5)
    for key, x, y, label, col in dests:
        ax2.add_patch(Rectangle((x, y), 1, 1,
                                fill=True, facecolor=col,
                                alpha=0.20, edgecolor=col,
                                linewidth=1.6))
        ax2.text(x + 0.5, y + 0.62, f"$|{key}\\rangle$",
                 ha="center", va="center", fontsize=9,
                 color=col, fontweight="bold")
        ax2.text(x + 0.5, y + 0.28, label,
                 ha="center", va="center", fontsize=9,
                 color=col)
        arrow = FancyArrowPatch(
            origin, (x + 0.5, y + 0.5),
            arrowstyle="-|>", mutation_scale=14,
            color=col, linewidth=1.6,
            connectionstyle="arc3,rad=0.12")
        ax2.add_patch(arrow)

    # axis labels
    ax2.text(1.5, -0.15, "$x$", ha="center", va="center", fontsize=10)
    ax2.text(-0.15, 1.5, "$y$", ha="center", va="center", fontsize=10)

    # norm line
    ax2.text(1.5, -1.05,
             r"$\sum |a_i|^2 = \frac{1}{9}+\frac{2}{9}+\frac{2}{9}+\frac{4}{9} = 1$",
             ha="center", va="top", fontsize=9)

    # caption
    ax2.text(1.5, -1.55,
             "(b) $3\\times 3$ torus showing the four destination nodes\n"
             "after one shift, with amplitudes.",
             ha="center", va="top", fontsize=8.5, style="italic")

    fig.tight_layout()
    save(fig, "fig-one-step/one-step.png")


if __name__ == "__main__":
    one_step()
