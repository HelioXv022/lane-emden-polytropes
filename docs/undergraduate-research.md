# Undergraduate research: Lane–Emden solution families (2023–24)

Final-year undergraduate project with Prof. Yu-Qing Lou, Department of Physics, Tsinghua University. The results were written up in an unpublished progress report (Y.-Q. Lou and Z.-Q. Xu, 2023). All calculations were done in MATLAB with `ode45`, `ode89` and `ode113` and Simpson quadrature; that code is not included here.

The standard Lane–Emden problem fixes a regular centre, $\theta(0) = 1$, $\theta'(0) = 0$. The project looked at the wider family of solutions obtained from other initial conditions, and asked which of them could still be read as a self-gravitating configuration.

## What I did

**Solution families at n = 4.** I compared phase portraits with radial profiles to classify the solution branches, and followed one branch (starting from $\ln z = 0$, $w = 0.5$, $dw/dz = 0.5$ in the report's variables) that looked like it could describe a star with a hollow interior. I then looked at whether the signs of the pressure gradient and of the enclosed mass along that branch were physically consistent.

**Mass-integral test.** A proposed zero-mass condition for such branches required a mass integral to vanish up to the point where the derivative is zero. I sampled two n = 4 curves with an ODE solver and integrated them with Simpson's rule at step sizes $10^{-3}$, $10^{-4}$ and $10^{-5}$. Both results were stable to four decimals ([n4_table1.csv](../data/historical/n4_table1.csv)): 0.0013 for the first curve, small but not shown to be zero, and 1.2853 for the second, which clearly does not vanish. Accuracy near the singular point remained the main open problem.

**Non-integer indices.** I scanned $3 < n < 4$ in steps of 0.1 and compared $n = 3.5$ and $n = 4.5$ with $n = 4$. The $n = 4.5$ runs needed `ode113` because `ode45` was too slow. At $n = 3.5$ the phase-space curves became tangled, which we first described as chaotic.

**The special case n = 5.** The phase portrait has a symmetric double-lobed structure, with families of small loops around each lobe and larger loops around both.

**Oscillatory solutions at n = 1.** Beyond the first zero, $\theta = \sin\xi/\xi$ oscillates with decreasing amplitude. I tested whether the contributions of successive lobes to the mass integral cancel. The first test gave $-3.1835$, so the cancellation assumption failed; a further interval gave $+6.3397$, showing where a later positive contribution offsets the earlier negative one.

## Looking back with the Python version

Re-deriving the problem in 2026 cleared up two points:

- For $n > 1$ the equation maps to a two-dimensional autonomous system in $t = \ln\xi$ ([model.md](model.md)). A 2D autonomous flow cannot be chaotic (Poincaré–Bendixson), so the tangled $n = 3.5$ curves were most likely a numerical artefact, for example from fractional powers of negative $\theta$, rather than chaos.
- At $n = 5$ that system has a conserved energy with a double-well potential. Its level sets reproduce the double-lobed portrait: small closed orbits in each well, a separatrix, and large orbits around both.

The hollow-star and neutrino interpretations we discussed at the time stay conjectures; they would need an additional component with its own equation of state and boundary conditions.
