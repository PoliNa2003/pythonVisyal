import numpy as np
import matplotlib.pyplot as plt


def main() -> None:
    # Вариант 2: y = T_2(2x), y = T_4(x/2), x ∈ [-1, 2].
    x = np.linspace(-1.0, 2.0, 1001)
    y1 = 2 * (2 * x) ** 2 - 1
    y2 = 8 * (x / 2) ** 4 - 8 * (x / 2) ** 2 + 1

    fig, ax = plt.subplots(figsize=(10, 6), facecolor="#edf2f7")
    ax.set_facecolor("#ffffff")
    ax.plot(x, y1, color="#1769aa", linewidth=2.6, label=r"$y=T_2(2x)$")
    ax.plot(x, y2, color="#d1495b", linewidth=2.6, label=r"$y=T_4(x/2)$")

    ax.axhline(0, color="#333333", linewidth=0.9)
    ax.axvline(0, color="#333333", linewidth=0.9)
    ax.set(
        title="Функции Чебышева — вариант 2",
        xlabel="$x$",
        ylabel="$T_n(x)$",
        xlim=(-1.05, 2.05),
    )
    ax.set_xticks(np.arange(-1.0, 2.01, 0.25))
    ax.tick_params(labelsize=10, colors="#263238")
    ax.grid(True, color="#9eacb5", linestyle="--", linewidth=0.65, alpha=0.65)
    ax.legend(fontsize=11, frameon=True)
    ax.set_title(ax.get_title(), fontsize=15, color="#17324d", pad=14)
    ax.xaxis.label.set_size(12)
    ax.yaxis.label.set_size(12)
    fig.tight_layout()
    fig.savefig("chebyshev_variant_2.png", dpi=160, facecolor=fig.get_facecolor())

    # Задание 2, вариант 2: z = y^2 cos(x), x ∈ [-10, 10], y ∈ [-2, 2].
    x3 = np.linspace(-10.0, 10.0, 180)
    y3 = np.linspace(-2.0, 2.0, 120)
    xx, yy = np.meshgrid(x3, y3)
    zz = yy**2 * np.cos(xx)
    fig3d = plt.figure(figsize=(11, 7))
    ax3d = fig3d.add_subplot(111, projection="3d")
    surface = ax3d.plot_surface(xx, yy, zz, cmap="jet", linewidth=0, antialiased=True)
    ax3d.set_title(r"$z=y^2\cos(x)$ — стиль jet", fontsize=15, pad=16)
    ax3d.set_xlabel("x", labelpad=8)
    ax3d.set_ylabel("y", labelpad=8)
    ax3d.set_zlabel("z", labelpad=8)
    ax3d.tick_params(labelsize=9)
    fig3d.colorbar(surface, ax=ax3d, shrink=0.65, pad=0.1, label="z")
    fig3d.tight_layout()
    fig3d.savefig("surface_variant_2_jet.png", dpi=160)

    fig_cool = plt.figure(figsize=(11, 7))
    ax_cool = fig_cool.add_subplot(111, projection="3d")
    surface_cool = ax_cool.plot_surface(xx, yy, zz, cmap="cool", linewidth=0, antialiased=True)
    ax_cool.set_title(r"$z=y^2\cos(x)$ — стиль cool", fontsize=15, pad=16)
    ax_cool.set_xlabel("x", labelpad=8)
    ax_cool.set_ylabel("y", labelpad=8)
    ax_cool.set_zlabel("z", labelpad=8)
    ax_cool.tick_params(labelsize=9)
    fig_cool.colorbar(surface_cool, ax=ax_cool, shrink=0.65, pad=0.1, label="z")
    fig_cool.tight_layout()
    fig_cool.savefig("surface_variant_2_cool.png", dpi=160)
    plt.show()


if __name__ == "__main__":
    main()
