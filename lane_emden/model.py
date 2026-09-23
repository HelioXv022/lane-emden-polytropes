"""Regular Lane-Emden solutions and an explicitly defined phase transform.

The radial solver keeps the physical theta >= 0 branch. The autonomous
system uses t = ln(xi) and x = xi^a theta with a = 2/(n-1); see docs/model.md.
"""

from dataclasses import dataclass
import numpy as np
from scipy.integrate import solve_ivp, simpson


@dataclass(frozen=True)
class Profile:
    n: float
    xi: np.ndarray
    theta: np.ndarray
    derivative: np.ndarray
    surface: float | None

    @property
    def density(self):
        """rho/rho_c; n=0 is the formal incompressible limit."""
        return np.maximum(self.theta, 0.0) ** self.n

    @property
    def mass(self):
        """M/(4*pi*rho_c*alpha**3) from the integrated ODE."""
        return -self.xi**2 * self.derivative

    def mass_by_quadrature(self):
        """Independent Simpson estimate including the regular center."""
        return float(simpson(self.xi**2 * self.density, x=self.xi))


def solve_polytrope(n, xi_max=40.0, points=4001, rtol=1e-10, atol=1e-12):
    """Integrate from a center series to the first zero or xi_max.

    Negative trial-stage theta is clipped ONLY to evaluate the RHS during
    surface event localization. No negative branch is returned. Integrator
    failure is raised; an absent surface means the finite interval ended.
    """
    n = float(n)
    if not np.isfinite(n) or n < 0:
        raise ValueError("n must be finite and nonnegative")
    eps = 1e-5
    if not np.isfinite(xi_max) or xi_max <= eps:
        raise ValueError("xi_max must be finite and greater than 1e-5")
    if not isinstance(points, (int, np.integer)) or points < 3:
        raise ValueError("points must be an integer >= 3")
    theta0 = 1 - eps**2 / 6 + n * eps**4 / 120
    slope0 = -eps / 3 + n * eps**3 / 30

    def rhs(xi, state):
        theta, slope = state
        return [slope, -2 * slope / xi - max(theta, 0.0)**n]

    def surface_event(xi, state):
        return state[0]

    surface_event.terminal = True
    surface_event.direction = -1
    sol = solve_ivp(rhs, (eps, xi_max), [theta0, slope0],
                    method="DOP853", rtol=rtol, atol=atol,
                    max_step=0.1, events=surface_event, dense_output=True)
    if not sol.success:
        raise RuntimeError(sol.message)
    surface = float(sol.t_events[0][0]) if len(sol.t_events[0]) else None
    end = surface if surface is not None else xi_max
    grid = np.linspace(eps, end, points - 1)
    theta, slope = sol.sol(grid)
    if surface is not None:
        theta[-1] = 0.0
    return Profile(n, np.r_[0.0, grid], np.r_[1.0, theta],
                   np.r_[0.0, slope], surface)


def _phase_index(n):
    n = float(n)
    if not np.isfinite(n) or n <= 1:
        raise ValueError("This phase transformation requires n > 1")
    return n, 2.0 / (n - 1.0)


def phase_rhs(t, state, n):
    """t=ln(xi), x=xi**a*theta, v=dx/dt, a=2/(n-1).

    For noninteger n only x>=0 is defined as a real power. No signed-power
    replacement or real-part projection is silently introduced.
    """
    n, a = _phase_index(n)
    x, v = state
    x = np.asarray(x)
    if not n.is_integer() and np.any(x < 0):
        raise ValueError("Noninteger n requires x >= 0 in this model")
    return np.array([v, (2*a-1)*v + a*(1-a)*x - x**n])


def phase_energy(x, v, n):
    """E with dE/dt=(2*a-1)*v**2; conserved at n=5."""
    n, a = _phase_index(n)
    x = np.asarray(x)
    if not n.is_integer() and np.any(x < 0):
        raise ValueError("Noninteger n requires x >= 0 in this model")
    return np.asarray(v)**2/2 + a*(a-1)*x**2/2 + x**(n+1)/(n+1)
