"""Numerical tools for the Lane-Emden equation of polytropic stellar structure."""

from .model import solve_polytrope, phase_rhs, phase_energy

__all__ = ["solve_polytrope", "phase_rhs", "phase_energy"]
