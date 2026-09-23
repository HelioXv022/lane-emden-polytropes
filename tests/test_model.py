"""Analytic, mass-integral and invariant checks for the Lane-Emden solver."""
import unittest
import numpy as np
from scipy.integrate import solve_ivp
from lane_emden import solve_polytrope, phase_rhs, phase_energy


class ModelTests(unittest.TestCase):
    def test_analytic_profiles(self):
        for n, end, exact in [(0,2,lambda x:1-x*x/6),
                               (1,3,lambda x:np.sinc(x/np.pi)),
                               (5,30,lambda x:1/np.sqrt(1+x*x/3))]:
            with self.subTest(n=n):
                p = solve_polytrope(n, xi_max=end)
                np.testing.assert_allclose(p.theta, exact(p.xi), atol=2e-8, rtol=0)

    def test_analytic_surfaces(self):
        for n, radius, mass in [(0,np.sqrt(6),2*np.sqrt(6)), (1,np.pi,np.pi)]:
            with self.subTest(n=n):
                p = solve_polytrope(n)
                self.assertAlmostEqual(p.surface, radius, delta=2e-8)
                self.assertAlmostEqual(p.mass[-1], mass, delta=2e-8)

    def test_fractional_models_stop_at_surface_and_have_positive_mass(self):
        for n in [3.5,4,4.5]:
            with self.subTest(n=n):
                p = solve_polytrope(n)
                self.assertIsNotNone(p.surface)
                self.assertTrue(np.all(p.theta >= 0))
                self.assertTrue(np.all(np.diff(p.mass) >= -1e-8))
                self.assertLess(abs(p.mass[-1]-p.mass_by_quadrature()), 2e-7)

    def test_n5_finite_interval_is_not_a_surface(self):
        p = solve_polytrope(5)
        self.assertIsNone(p.surface)
        exact_mass = 40**3/(3*(1+40**2/3)**1.5)
        self.assertAlmostEqual(p.mass[-1], exact_mass, delta=2e-8)

    def test_n5_energy_conservation(self):
        sol = solve_ivp(lambda t,y:phase_rhs(t,y,5), (0,30), [.8,.15],
                        method="DOP853", rtol=1e-11, atol=1e-13, max_step=.05)
        self.assertTrue(sol.success)
        energies = phase_energy(*sol.y, 5)
        self.assertLess(np.max(abs(energies-energies[0])), 1e-9)

    def test_phase_transform_matches_exact_n5_solution(self):
        # Independent closed-form orbit transformed into the chosen coordinates.
        def exact(t):
            z = np.exp(t)
            theta = 1/np.sqrt(1+z*z/3)
            slope = -z/3/(1+z*z/3)**1.5
            x = np.sqrt(z)*theta
            return np.array([x, x/2+z**1.5*slope])
        times = np.linspace(-3,3,301)
        sol = solve_ivp(lambda t,y:phase_rhs(t,y,5), (-3,3), exact(-3),
                        t_eval=times, method="DOP853", rtol=1e-11, atol=1e-13)
        self.assertTrue(sol.success)
        np.testing.assert_allclose(sol.y, exact(times), atol=2e-8, rtol=0)

    def test_no_silent_fractional_negative_extension(self):
        with self.assertRaises(ValueError):
            phase_rhs(0, [-.1,0], 3.5)
        with self.assertRaises(ValueError):
            phase_rhs(0, [1,0], 1)
        with self.assertRaises(ValueError):
            solve_polytrope(-1)


if __name__ == "__main__":
    unittest.main()
