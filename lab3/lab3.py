"""Лабораторная работа 3: линии электрического поля, вариант 2."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT_DIR = Path(__file__).resolve().parent / "results"
# Параметры зарядов варианта 2. Заряды заданы в единицах e,
# координаты — в условных единицах.
CHARGES = np.array([
    [2.0, 0.0, 0.0, 1.0],
    [0.0, 2.0, 0.0, 1.0],
    [0.0, -2.0, 0.0, 1.0],
], dtype=float)
COLORS = np.where(CHARGES[:, 3] > 0, "#d1495b", "#2463a6")
BOUNDS = 2.0


def field(points: np.ndarray) -> np.ndarray:
    """Вектор E = sum(q r / |r|^3) в массиве точек."""
    delta = points[..., None, :] - CHARGES[:, :3]
    r2 = np.sum(delta * delta, axis=-1)
    r2 = np.maximum(r2, 1e-5)
    return np.sum(delta * CHARGES[:, 3] / (r2 ** 1.5)[..., None], axis=-2)


def integrate(seed: np.ndarray, sign: float, step: float = 0.035) -> np.ndarray:
    points = [seed.astype(float)]
    p = points[0].copy()
    for _ in range(900):
        e = field(p)
        mag = np.linalg.norm(e)
        if mag < 1e-10:
            break
        p = p + sign * step * e / mag
        if np.linalg.norm(p) > BOUNDS or np.min(np.linalg.norm(CHARGES[:, :3] - p, axis=1)) < 0.035:
            points.append(p.copy())
            break
        points.append(p.copy())
    return np.asarray(points)


def make_lines() -> list[tuple[np.ndarray, str]]:
    lines = []
    for x, y, z, q in CHARGES:
        n = max(10, int(24 * abs(q)))
        radius = 0.09
        for theta in np.linspace(0, 2 * np.pi, n, endpoint=False):
            seed = np.array([x + radius * np.cos(theta), y + radius * np.sin(theta), z])
            lines.append((integrate(seed, np.sign(q)), "#d1495b" if q > 0 else "#2463a6"))
    return lines


def projection(points: np.ndarray, perspective: bool) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    # Camera rotated to expose the charge plane and the field's 3D structure.
    az, el = np.deg2rad(38), np.deg2rad(24)
    ca, sa, ce, se = np.cos(az), np.sin(az), np.cos(el), np.sin(el)
    x, y, z = points.T
    u = ca * x - sa * y
    v0 = sa * x + ca * y
    v = -se * v0 + ce * z
    depth = ce * v0 + se * z
    if perspective:
        factor = 4.5 / np.maximum(4.5 - depth, 0.5)
        u, v = u * factor, v * factor
    return u, v, depth


def draw(index: int, lines: list[tuple[np.ndarray, str]]) -> None:
    perspective = index == 6
    arrows = index >= 3
    zbuffer = index >= 4
    fig, ax = plt.subplots(figsize=(9, 7), facecolor="#f2f5f8")
    ax.set_facecolor("#ffffff")
    for pts, color in lines:
        u, v, d = projection(pts, perspective)
        shade = np.clip(0.58 + (d - d.min()) / (np.ptp(d) + 1e-9) * 0.42, 0.35, 1.0) if zbuffer else np.ones_like(d)
        # draw segment-by-segment in depth order to emulate a simple Z-buffer.
        order = np.argsort((d[:-1] + d[1:]) * 0.5) if zbuffer else np.arange(len(d) - 1)
        for k in order:
            c = np.array(plt.matplotlib.colors.to_rgb(color)) * (shade[k] if zbuffer else 1.0)
            ax.plot(u[k:k + 2], v[k:k + 2], color=c, lw=1.05, alpha=0.9, zorder=2 + d[k] * 0.01)
        if arrows and len(u) > 12:
            k = len(u) // 2
            ax.annotate("", xy=(u[k + 2], v[k + 2]), xytext=(u[k - 2], v[k - 2]),
                        arrowprops={"arrowstyle": "-|>", "color": color, "lw": 1.0})
    # Charge markers and their labels are drawn above field lines.
    cu, cv, _ = projection(CHARGES[:, :3], perspective)
    for i, (x, y, z, q) in enumerate(CHARGES):
        ax.scatter(cu[i], cv[i], s=115, c=COLORS[i], edgecolor="white", linewidth=1.4, zorder=10)
        ax.text(cu[i], cv[i], f"{q:+g}", color="white", weight="bold", ha="center", va="center", fontsize=9, zorder=11)
    titles = {
        2: "Линии электрического поля — вариант 2",
        3: "Направление линий поля",
        4: "Z-буфер и затемнение по глубине",
        5: "Z-буфер с палитрой глубины",
        6: "Центральное проецирование",
    }
    ax.set_title(titles[index], fontsize=14, color="#17324d", pad=14)
    ax.set_xlabel("u (проекция мировой системы)")
    ax.set_ylabel("v (проекция мировой системы)")
    ax.grid(True, linestyle="--", alpha=0.25)
    ax.set_aspect("equal", adjustable="datalim")
    fig.tight_layout()
    fig.savefig(OUT_DIR / f"electric_field_{index:02d}.png", dpi=180, facecolor=fig.get_facecolor())


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    lines = make_lines()
    for index in range(2, 7):
        draw(index, lines)
    print(f"Сохранено 5 графиков: {OUT_DIR}")
    plt.show()


if __name__ == "__main__":
    main()
