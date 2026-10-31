from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# Исходные данные варианта 2
POWER_W = 800.0
TIME_PHASE = 1.0 / 8.0  # момент времени в долях периода
A_CM = 3.0
B_CM = 1.0
N, M = 1, 1
F_MAX_GHZ = 50.0
C_M_S = 3.0e8
EPS0 = 8.8542e-12
MU0 = 4.0 * math.pi * 1.0e-7
ROOT_DJ1 = 1.8411837813406593  # первый ненулевой корень J'_1(x)=0
OUT_DIR = Path(__file__).resolve().parent / "results"


def cutoff_rect_ghz(a_cm: float, b_cm: float) -> float:
    return C_M_S / 2 * math.sqrt((N / a_cm) ** 2 + (M / b_cm) ** 2) * 100 / 1e9


def cutoff_circle_ghz(a_cm: float) -> float:
    return C_M_S / (2 * math.pi) * ROOT_DJ1 / a_cm * 100 / 1e9


def propagation(f_ghz: float, fc_ghz: float) -> tuple[float, float, float, float]:
    """beta (1/cm), lambda_g (cm), phase speed and group speed (m/s)."""
    beta = 2 * math.pi / C_M_S * 1e9 * math.sqrt(f_ghz**2 - fc_ghz**2) / 100
    wavelength = 2 * math.pi / beta
    vp = 2 * math.pi * f_ghz * 1e9 / (beta * 100)  # m/s
    vg = C_M_S**2 / vp
    return beta, wavelength, vp, vg


def _rect_amplitudes(a: float, b: float, fc: float, f: float) -> dict[str, float]:
    beta, wavelength, vp, vg = propagation(f, fc)
    # Коэффициент нормировки мощности из TE-формулы MATLAB-примера.
    k_a = (beta * 100 * 2 * math.pi * f * 1e9 / MU0 / 2
           * ((math.pi * N / a) ** 2 + (math.pi * M / b) ** 2) * a * b / 4)
    potential = math.sqrt(POWER_W / k_a) * 1e4
    g2 = (math.pi * N / a) ** 2 + (math.pi * M / b) ** 2
    an = math.pi * N / a * potential / math.sqrt(2)
    am = math.pi * M / b * potential / math.sqrt(2)
    bz = g2 * potential / math.sqrt(2)
    return dict(beta=beta, wavelength=wavelength, vp=vp, vg=vg, potential=potential,
                an=an, am=am, bz=bz, emax=2 * math.pi * f * 1e9 * max(an, am) / 1e4,
                btmax=beta * max(an, am), bzmax=bz)


def _circle_amplitudes(a: float, fc: float, f: float) -> dict[str, float]:
    beta, wavelength, vp, vg = propagation(f, fc)
    j1root = _bessel_j(1, ROOT_DJ1)
    potential = math.sqrt(POWER_W / (beta * 100 * 2 * math.pi * f * 1e9 * math.pi / MU0 / 2
                         * (ROOT_DJ1**2 - N**2) * j1root**2)) * 1e4
    an = N / a * potential * j1root
    bz = (ROOT_DJ1 / a) ** 2 * potential * j1root
    return dict(beta=beta, wavelength=wavelength, vp=vp, vg=vg, potential=potential,
                an=an, bz=bz, emax=2 * math.pi * f * 1e9 * an / 1e4,
                btmax=beta * an, bzmax=bz)


def _bessel_j(order: int, x: float) -> float:
    """Bessel J_n by its convergent power series (avoids an extra dependency)."""
    term = (x / 2) ** order / math.factorial(order)
    total = term
    for k in range(1, 80):
        term *= -(x * x / 4) / (k * (k + order))
        total += term
        if abs(term) < 1e-16:
            break
    return total


def save_figure(fig: plt.Figure, folder: str, filename: str) -> None:
    path = OUT_DIR / folder / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_dispersion(folder: str, fc_mode: float, title: str,
                   show_light_line: bool = False) -> None:
    f = np.linspace(0, F_MAX_GHZ, 1600)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    beta = 2 * math.pi / C_M_S * 1e9 / 100 * np.sqrt(np.maximum(f**2 - fc_mode**2, 0))
    beta[f < fc_mode] = np.nan
    ax.plot(f, beta, color="#2457a6", lw=2.5,
            label=f"H₁₁, fс = {fc_mode:.2f} ГГц")
    if show_light_line:
        beta_light = 2 * math.pi / C_M_S * 1e9 / 100 * f
        ax.plot(f, beta_light, color="#2e8b57", linestyle="--", lw=2,
                label="β = 2πf/c")
    ax.set(xlim=(0, F_MAX_GHZ), ylim=(0, None), xlabel="f, ГГц", ylabel="β, см⁻¹", title=title)
    ax.grid(True, alpha=.3)
    ax.legend(fontsize=8, ncol=2)
    save_figure(fig, folder, "02_dispersion.png")


def plot_rect_fields(folder: str, a: float, b: float) -> None:
    # H_type.m uses the TE H_nm potential. E_type.m has a sin*sin potential,
    # which belongs to TM modes; retain its two-grid plotting layout and colors.
    x_contour = np.linspace(0, a, 301)
    y_contour = np.linspace(0, b, 101)
    xx, yy = np.meshgrid(x_contour, y_contour)
    potential = (np.cos(math.pi * N * xx / a) * np.cos(math.pi * M * yy / b)
                 * math.sin(-2 * math.pi * TIME_PHASE))

    x_vector = np.linspace(0, a, 61)
    y_vector = np.linspace(0, b, 21)
    xv, yv = np.meshgrid(x_vector, y_vector)
    potential_vector = (np.cos(math.pi * N * xv / a) * np.cos(math.pi * M * yv / b)
                        * math.sin(-2 * math.pi * TIME_PHASE))
    dv_y, dv_x = np.gradient(-potential_vector, y_vector, x_vector)
    fig, ax = plt.subplots(figsize=(9, 4.4))
    ax.contour(xx, yy, potential, levels=10, colors="#2457a6", linewidths=1.2)
    ax.quiver(xv, yv, dv_x, dv_y, color="#c62828", scale=28)
    ax.set(xlim=(0, a), ylim=(0, b), xlabel="x, см", ylabel="y, см",
           title="Линии E и B в прямоугольном сечении H₁₁")
    ax.set_aspect("equal")
    ax.set_xticks(np.arange(0, a + 0.001, 0.5))
    ax.set_yticks(np.arange(0, b + 0.001, 0.5))
    ax.grid(alpha=.2)
    save_figure(fig, folder, "03_field_lines.png")


def plot_circle_fields(folder: str, a: float) -> None:
    grid = np.linspace(-a, a, 301)
    xx, yy = np.meshgrid(grid, grid)
    rr = np.hypot(xx, yy)
    phi = np.arctan2(yy, xx)
    potential = _bessel_j_grid(1, ROOT_DJ1 * rr / a) * np.sin(phi - 2 * math.pi * TIME_PHASE)
    inside = rr <= a
    potential = np.where(inside, potential, np.nan)
    dy, dx = np.gradient(-np.nan_to_num(potential), grid, grid)
    dx = np.where(inside, dx, np.nan)
    dy = np.where(inside, dy, np.nan)
    fig, ax = plt.subplots(figsize=(6.3, 6.3))
    ax.contour(xx, yy, potential, levels=18, colors="#2457a6", linewidths=1.1)
    st = (slice(8, -8, 18), slice(8, -8, 18))
    ax.quiver(xx[st], yy[st], dx[st], dy[st], color="#c62828", scale=8)
    ax.add_patch(plt.Circle((0, 0), a, fill=False, color="#30343b", lw=2))
    ax.set(xlim=(-a, a), ylim=(-a, a), xlabel="x, см", ylabel="y, см",
           title="Линии E и B в круглом сечении H₁₁")
    ax.set_aspect("equal")
    ax.grid(alpha=.2)
    save_figure(fig, folder, "03_field_lines.png")


def _bessel_j_grid(order: int, values: np.ndarray) -> np.ndarray:
    term = (values / 2) ** order / math.factorial(order)
    total = term.copy()
    for k in range(1, 45):
        term = term * (-(values * values / 4) / (k * (k + order)))
        total = total + term
    return total


def plot_rect_contour(folder: str, a: float, b: float, q: dict[str, float]) -> None:
    en = 2 * math.pi * (1.5 * cutoff_rect_ghz(a, b)) * 1e9 * q["an"] / 1e4
    em = 2 * math.pi * (1.5 * cutoff_rect_ghz(a, b)) * 1e9 * q["am"] / 1e4
    btn, btm = q["beta"] * q["an"], q["beta"] * q["am"]
    s1 = np.linspace(0, a, 350, endpoint=False); u1 = s1
    s2 = np.linspace(a, a + b, 120, endpoint=False); u2 = s2 - a
    s3 = np.linspace(a + b, 2 * a + b, 350, endpoint=False); u3 = 2 * a + b - s3
    s4 = np.linspace(2 * a + b, 2 * a + 2 * b, 120); u4 = 2 * a + 2 * b - s4
    s = np.concatenate((s1, s2, s3, s4))
    E = np.concatenate((en*np.sin(math.pi*N/a*u1), (-1)**N*em*np.sin(math.pi*M/b*u2),
                        (-1)**(M+1)*en*np.sin(math.pi*N/a*u3), -em*np.sin(math.pi*M/b*u4)))
    bt = np.concatenate((btn*np.sin(math.pi*N/a*u1), (-1)**N*btm*np.sin(math.pi*M/b*u2),
                         (-1)**(M+1)*btn*np.sin(math.pi*N/a*u3), -btm*np.sin(math.pi*M/b*u4))) * 1e6
    bz = q['bzmax'] * np.concatenate((np.cos(math.pi*N/a*u1), (-1)**N*np.cos(math.pi*M/b*u2),
                                      (-1)**M*np.cos(math.pi*N/a*u3), np.cos(math.pi*M/b*u4))) * 1e6
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(s, -E, color="#2457a6", label="E, В/см", lw=2)
    ax.plot(s, -bt, color="#2e8b57", linestyle="--", label="Bτ, мкТл", lw=2)
    ax.plot(s, bz, color="#c62828", linestyle="-.", label="Bz, мкТл", lw=2)
    ax.set(xlabel="s, см", ylabel="Поле (масштабы указаны в легенде)", title="Поля вдоль контура прямоугольного волновода H₁₁")
    ax.set_xlim(0, 2 * a + 2 * b)
    eb_max = max(q["emax"], q["btmax"] * 1e6, q["bzmax"] * 1e6)
    ax.set_ylim(-1.1 * eb_max, 1.1 * eb_max)
    ax.grid(alpha=.3)
    ax.legend()
    save_figure(fig, folder, "04_fields_on_contour.png")
    rho = E * 100 * EPS0 / 1e4 * 1e9 * 1e2
    jsz = bt / 1e6 / MU0 / 100
    jst = -bz / 1e6 / MU0 / 100
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(s, -rho, color="#2457a6", label="ρs, 10⁻² нКл/см²", lw=2)
    ax.plot(s, -jsz, color="#2e8b57", linestyle="--", label="jsz, А/см", lw=2)
    ax.plot(s, jst, color="#c62828", linestyle="-.", label="jsτ, А/см", lw=2)
    ax.set(xlabel="s, см", ylabel="Заряд и ток", title="Поверхностные заряд и ток на контуре прямоугольного волновода H₁₁")
    ax.set_xlim(0, 2 * a + 2 * b)
    rho_max_plot = q["emax"] * 100 * EPS0 / 1e4 * 1e9 * 1e2
    jsz_max = q["btmax"] / MU0 / 100
    jst_max = q["bzmax"] / MU0 / 100
    charge_current_max = max(rho_max_plot, jsz_max, jst_max)
    ax.set_ylim(-1.1 * charge_current_max, 1.1 * charge_current_max)
    ax.grid(alpha=.3)
    ax.legend()
    save_figure(fig, folder, "05_charge_current.png")


def plot_circle_contour(folder: str, a: float, q: dict[str, float]) -> None:
    s = np.linspace(0, 2 * math.pi * a, 900)
    phase = N * s / a - 2 * math.pi * TIME_PHASE
    e = q['emax'] * np.cos(phase)
    bt = q['bzmax'] * np.cos(phase) * 1e6
    bz = q['btmax'] * np.cos(phase) * 1e6
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(s, e, color="#2457a6", label="E, В/см", lw=2)
    ax.plot(s, bt, color="#2e8b57", linestyle="--", label="Bτ, мкТл", lw=2)
    ax.plot(s, bz, color="#c62828", linestyle="-.", label="Bz, мкТл", lw=2)
    ax.set(xlabel="s, см", ylabel="Поле (масштабы указаны в легенде)", title="Поля вдоль контура круглого волновода H₁₁")
    ax.set_xlim(0, 2 * math.pi * a)
    eb_max = max(q["emax"], q["bzmax"] * 1e6, q["btmax"] * 1e6)
    ax.set_ylim(-1.1 * eb_max, 1.1 * eb_max)
    ax.grid(alpha=.3); ax.legend()
    save_figure(fig, folder, "04_fields_on_contour.png")
    rho = e * 100 * EPS0 / 1e4 * 1e9 * 1e2
    jsz = q['btmax'] * np.cos(phase) / MU0 / 100
    jst = -q['bzmax'] * np.cos(phase) / MU0 / 100
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(s, rho, color="#2457a6", label="ρs, 10⁻² нКл/см²", lw=2)
    ax.plot(s, jsz, color="#2e8b57", linestyle="--", label="jsz, А/см", lw=2)
    ax.plot(s, jst, color="#c62828", linestyle="-.", label="jsτ, А/см", lw=2)
    ax.set(xlabel="s, см", ylabel="Заряд и ток", title="Поверхностные заряд и ток на контуре круглого волновода H₁₁")
    ax.set_xlim(0, 2 * math.pi * a)
    rho_max_plot = q["emax"] * 100 * EPS0 / 1e4 * 1e9 * 1e2
    jsz_max = q["btmax"] / MU0 / 100
    jst_max = q["bzmax"] / MU0 / 100
    charge_current_max = max(rho_max_plot, jsz_max, jst_max)
    ax.set_ylim(-1.1 * charge_current_max, 1.1 * charge_current_max)
    ax.grid(alpha=.3); ax.legend()
    save_figure(fig, folder, "05_charge_current.png")


def print_parameters(name: str, fc: float, q: dict[str, float]) -> None:
    f = 1.5 * fc
    print(f"{name}, H_11, P={POWER_W:g} Вт")
    print(f"  Частота отсечки fс = {fc:.6f} ГГц; расчетная частота f = 1.5 fс = {f:.6f} ГГц")
    print(f"  beta = {q['beta']:.6f} 1/cm; lambda_waveguide = {q['wavelength']:.6f} cm")
    print(f"  vp = {q['vp']:.6e} м/с; vg = {q['vg']:.6e} м/с")
    print(f"  A2 = {q['potential']:.6g} T*cm^2")
    print(f"  Max fields: Emax = {q['emax']:.6g} V/cm, Btmax = {q['btmax']:.6g} T, Bzmax = {q['bzmax']:.6g} T")
    print(f"  Max magnetic field strengths: Htmax = {q['btmax'] / MU0 / 100:.6g} A/cm, Hzmax = {q['bzmax'] / MU0 / 100:.6g} A/cm")
    rho_max = q['emax'] * 100 * EPS0 / 1e4 * 1e9
    jsz_max = q['btmax'] / MU0 / 100
    jst_max = q['bzmax'] / MU0 / 100
    print(f"  Max surface charge = {rho_max:.6g} nC/cm^2; max currents: jsz = {jsz_max:.6g} A/cm, jst = {jst_max:.6g} A/cm")


def main() -> None:
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.titlesize": 13})
    fc_r = cutoff_rect_ghz(A_CM, B_CM)
    fc_c = cutoff_circle_ghz(A_CM)
    q_r = _rect_amplitudes(A_CM, B_CM, fc_r, 1.5 * fc_r)
    q_c = _circle_amplitudes(A_CM, fc_c, 1.5 * fc_c)
    print_parameters("Прямоугольный волновод (a=3 см, b=1 см)", fc_r, q_r)
    print_parameters("Круглый волновод (a=3 см)", fc_c, q_c)

    plot_dispersion("01_rectangular", fc_r,
                    "Дисперсионная кривая прямоугольного волновода H₁₁",
                    show_light_line=True)
    plot_rect_fields("01_rectangular", A_CM, B_CM)
    plot_rect_contour("01_rectangular", A_CM, B_CM, q_r)
    plot_dispersion("02_circular", fc_c,
                    "Дисперсионная кривая круглого волновода H₁₁",
                    show_light_line=True)
    plot_circle_fields("02_circular", A_CM)
    plot_circle_contour("02_circular", A_CM, q_c)
    print(f"\nСохранено 8 графиков в каталоге: {OUT_DIR}")


if __name__ == "__main__":
    main()
