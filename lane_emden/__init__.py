"""New reference implementation; not recovered historical MATLAB code."""

from .model import solve_polytrope, phase_rhs, phase_energy

__all__ = ["solve_polytrope", "phase_rhs", "phase_energy"]
