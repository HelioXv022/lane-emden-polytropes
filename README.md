# Lane–Emden Polytropes

[![Numerical checks](https://github.com/HelioXv022/lane-emden-polytropes/actions/workflows/check.yml/badge.svg)](https://github.com/HelioXv022/lane-emden-polytropes/actions/workflows/check.yml)

A Python solver for the Lane–Emden equation of stellar structure, tested against the known analytic solutions, together with notes on the solution families I studied as an undergraduate.

## Background

A self-gravitating gas sphere in hydrostatic equilibrium with a polytropic equation of state $P = K\rho^{1+1/n}$ reduces, in dimensionless form, to

$$
\theta'' + \frac{2}{\xi}\theta' + \theta^n = 0, \qquad \theta(0) = 1,\quad \theta'(0) = 0,
$$

where $\rho = \rho_c\theta^n$ and the enclosed mass is $m = -\xi^2\theta'$. The first zero of $\theta$ is the stellar surface.

In my final undergraduate year (2023–24) I worked on this equation with Prof. Yu-Qing Lou (Department of Physics, Tsinghua University). Using MATLAB ODE solvers and Simpson quadrature, I explored the solution families at $n = 1, 3.5, 4, 4.5$ and $5$, compared phase portraits with radial profiles, and tested proposed mass-integral cancellations numerically. [docs/undergraduate-research.md](docs/undergraduate-research.md) summarizes that work. The original MATLAB code is not in this repository.

This repository is a clean re-implementation in Python, written in 2026 to revisit the problem with reproducible, tested code.

## What the code does

- Solves regular polytropes with a series expansion at the centre, SciPy's DOP853 integrator (rtol 1e-10, atol 1e-12) and an event that stops at the surface.
- Computes the enclosed mass two independent ways, from $-\xi^2\theta'$ and by Simpson quadrature of $\xi^2\theta^n$, and checks that they agree.
- Maps the equation for $n > 1$ to an autonomous system in $t = \ln\xi$ and shows that $n = 5$ has a conserved energy, which explains the double-lobed phase portrait ([docs/model.md](docs/model.md)).

![Regular polytrope profiles and enclosed mass](results/figures/regular_profiles.png)

| $n$ | surface $\xi_1$ | mass $-\xi_1^2\theta'(\xi_1)$ | slope vs quadrature |
| --- | --- | --- | --- |
| 1 | 3.14159 ($=\pi$) | 3.14159 | 8e-11 |
| 3.5 | 9.53581 | 1.89056 | 4e-14 |
| 4 | 14.97155 | 1.79723 | 1e-13 |
| 4.5 | 31.83646 | 1.73780 | 9e-14 |
| 5 | no surface ($\xi \to \infty$) | 1.72719 at $\xi = 40$ ($\to\sqrt{3}$) | 8e-14 |

Against the analytic solutions for $n = 0, 1, 5$ the maximum error is below $4\times10^{-12}$, and the $n = 5$ phase-space energy drifts by less than $2\times10^{-16}$ ([results/validation.json](results/validation.json)).

![Conserved-energy contours for n = 5](results/figures/n5_energy_contours.png)

## Usage

Requires Python 3.10+.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v    # analytic, mass and invariant checks
python -m lane_emden                       # regenerate results/ and the figures
python -m lane_emden --output /tmp/run     # or write somewhere else
```

CI runs the tests and the full regeneration on every push.

## Layout

| Path | Contents |
| --- | --- |
| `lane_emden/model.py` | radial solver, mass diagnostics, phase-space vector field and energy |
| `lane_emden/__main__.py` | regenerates every CSV and figure in `results/` |
| `tests/test_model.py` | analytic profiles, surface positions, mass quadrature, $n=5$ invariant |
| `docs/theory.md` | derivation of the Lane–Emden equation and the mass relation |
| `docs/model.md` | the autonomous transformation, fixed points and the $n=5$ energy |
| `docs/undergraduate-research.md` | the 2023–24 project and its numerical results |
| `data/historical/` | values from the 2023 progress report, kept separate from new results |

## License

Code: MIT (see [LICENSE](LICENSE)).
