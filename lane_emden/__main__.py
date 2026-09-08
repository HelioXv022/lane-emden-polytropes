"""Regenerate the figures, numerical tables, and environment manifest."""

import argparse
import csv
import json
import platform
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.integrate import solve_ivp

from .model import solve_polytrope, phase_rhs, phase_energy


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()
    out = args.output
    figs = out / "figures"
    figs.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 11, "axes.spines.top": False,
                         "axes.spines.right": False, "figure.dpi": 140})
    indices = [1.0, 3.5, 4.0, 4.5, 5.0]
    colors = ["#2563eb", "#059669", "#d97706", "#9333ea", "#dc2626"]
    profiles = [solve_polytrope(n) for n in indices]
    rows = []
    for p in profiles:
        rows.append({"n": p.n, "surface_xi": p.surface,
                     "xi_end": float(p.xi[-1]),
                     "mass_from_slope": float(p.mass[-1]),
                     "mass_from_simpson": p.mass_by_quadrature(),
                     "mass_abs_difference": abs(float(p.mass[-1])-p.mass_by_quadrature())})
        np.savetxt(out / f"profile_n{p.n:g}.csv",
                   np.column_stack([p.xi, p.theta, p.derivative, p.density, p.mass]),
                   delimiter=",", header="xi,theta,dtheta_dxi,rho_over_rhoc,dimensionless_mass",
                   comments="")
    with (out / "summary.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), layout="constrained")
    for p, color in zip(profiles, colors):
        axes[0].plot(p.xi, p.theta, label=f"n = {p.n:g}", color=color, lw=2)
        axes[1].plot(p.xi, p.mass, color=color, lw=2)
        if p.surface is not None:
            axes[0].scatter(p.surface, 0, color=color, s=24, zorder=3)
    axes[0].set(xlabel=r"Dimensionless radius $\xi$", ylabel=r"Lane-Emden function $\theta$",
                title="Regular solutions and first zeros", xlim=(0,40))
    axes[1].set(xlabel=r"Dimensionless radius $\xi$", ylabel=r"$m=-\xi^2\theta'$",
                title="Enclosed mass", xlim=(0,40))
    axes[0].legend(frameon=False)
    for ax in axes:
        ax.grid(alpha=.18)
    fig.suptitle("Lane-Emden polytropes | New reference computation", fontsize=15)
    fig.savefig(figs / "regular_profiles.png")
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(10, 8), layout="constrained")
    for n, ax in zip(indices[1:], axes.flat):
        # Positive x domain shared by all four models. Streamlines are
        # qualitative vector-field visualizations, not convergence evidence.
        x = np.linspace(0.0, 1.5, 100)
        v = np.linspace(-1.0, 1.0, 100)
        xx, vv = np.meshgrid(x, v)
        dx, dv = phase_rhs(0, [xx, vv], n)
        ax.streamplot(x, v, dx, dv, density=1.05, color="#94a3b8", linewidth=.65)
        p = profiles[indices.index(n)]
        a = 2/(n-1)
        mask = p.xi > 0
        px = p.xi[mask]**a*p.theta[mask]
        pv = a*px + p.xi[mask]**(a+1)*p.derivative[mask]
        ax.plot(px, pv, color="#2563eb", lw=2, label="Regular solution")
        fixed = (a*(1-a))**(1/(n-1))
        ax.scatter([fixed], [0], color="#dc2626", s=25, zorder=4)
        ax.set(xlabel=r"$x=\xi^{2/(n-1)}\theta$", ylabel=r"$v=dx/dt$",
               title=f"n = {n:g}", xlim=(0,1.5), ylim=(-1,1))
    axes[0,0].legend(frameon=False, loc="lower left")
    fig.suptitle("Explicit new phase coordinates | Positive x domain", fontsize=15)
    fig.savefig(figs / "phase_fields.png")
    plt.close(fig)

    x = np.linspace(-1.5, 1.5, 600)
    v = np.linspace(-1, 1, 450)
    xx, vv = np.meshgrid(x, v)
    fig, ax = plt.subplots(figsize=(7,5), layout="constrained")
    ax.contour(xx, vv, phase_energy(xx, vv, 5),
               levels=[-.04,-.02,-.005,.02,.06,.14,.28,.5],
               colors="#2563eb", linewidths=1.3)
    ax.contour(xx, vv, phase_energy(xx, vv, 5), levels=[0], colors="#dc2626", linewidths=2)
    fixed = (1/4)**(1/4)
    ax.scatter([-fixed,0,fixed], [0,0,0], color="#0f172a", s=25)
    ax.set(xlabel=r"$x=\sqrt{\xi}\,\theta$", ylabel=r"$v=dx/d\ln\xi$",
           title="n = 5 | Conserved-energy contours\nSigned mathematical extension; red: E = 0")
    ax.grid(alpha=.15)
    fig.savefig(figs / "n5_energy_contours.png")
    plt.close(fig)

    xi = np.linspace(.1, 30, 2500)
    theta = np.sinc(xi/np.pi)
    mass = np.sin(xi)-xi*np.cos(xi)
    fig, axes = plt.subplots(2, 1, figsize=(9,6), sharex=True, layout="constrained")
    axes[0].plot(xi, theta, color="#2563eb", lw=2)
    axes[1].plot(xi, mass, color="#9333ea", lw=2)
    for ax in axes:
        ax.axvline(np.pi, color="#dc2626", ls="--", label=r"Physical surface $\xi=\pi$")
        ax.axhline(0, color="gray", lw=.7)
        ax.axvspan(np.pi, 30, color="#94a3b8", alpha=.12)
        ax.grid(alpha=.15)
    axes[0].legend(frameon=False)
    axes[0].set(ylabel=r"$\theta=\sin\xi/\xi$", title="n = 1 | Analytic continuation beyond the stellar surface")
    axes[1].set(xlabel=r"Dimensionless radius $\xi$", ylabel=r"Formal signed mass $m(\xi)$", xlim=(0,30))
    fig.savefig(figs / "n1_signed_extension.png")
    plt.close(fig)

    convergence = []
    for count in [101, 501, 2001, 8001]:
        p = solve_polytrope(4, points=count)
        convergence.append({"samples": count,
                            "mass_abs_difference": abs(float(p.mass[-1])-p.mass_by_quadrature())})
    with (out / "quadrature_convergence.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(convergence[0]))
        writer.writeheader()
        writer.writerows(convergence)
    analytic_errors = {}
    for n, end in [(0,2), (1,3), (5,30)]:
        p = solve_polytrope(n, xi_max=end)
        exact = {0: lambda z: 1-z*z/6,
                 1: lambda z: np.sinc(z/np.pi),
                 5: lambda z: 1/np.sqrt(1+z*z/3)}[n](p.xi)
        analytic_errors[str(n)] = float(np.max(np.abs(p.theta-exact)))
    orbit = solve_ivp(lambda t,y: phase_rhs(t,y,5), (0,40), [.8,.15],
                      method="DOP853", rtol=1e-11, atol=1e-13, max_step=.05)
    if not orbit.success:
        raise RuntimeError(orbit.message)
    energies = phase_energy(*orbit.y, 5)
    diagnostics = {"analytic_max_abs_errors": analytic_errors,
                   "n5_max_energy_drift": float(np.max(np.abs(energies-energies[0]))),
                   "environment": {"python": platform.python_version(), "numpy": np.__version__,
                                   "scipy": scipy.__version__, "matplotlib": matplotlib.__version__},
                   "settings": {"solver": "DOP853", "rtol":1e-10, "atol":1e-12,
                                "radial_max_step":.1, "xi_max":40, "profile_points":4001},
                   "provenance": "New computation; not a reproduction of the historical figures or table"}
    (out / "validation.json").write_text(json.dumps(diagnostics, indent=2)+"\n")
    print(json.dumps({"output":str(out), **diagnostics}, indent=2))


if __name__ == "__main__":
    main()
