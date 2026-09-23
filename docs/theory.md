# Theoretical background: self-gravitating polytropic spheres

This document derives the standard theory of self-gravitating polytropes used in this project and connects it to the questions from my undergraduate research ([undergraduate-research.md](undergraduate-research.md)).

## 1. Physical question and assumptions

A self-gravitating fluid sphere is held together by gravity and supported by a pressure gradient. The structure problem is to determine how density, pressure and enclosed mass vary with distance from the center.

The standard model assumes spherical symmetry, Newtonian gravity, static equilibrium, an isotropic fluid pressure, and a polytropic equation of state with spatially constant K and n. Rotation, magnetic stresses and additional matter components are absent from this baseline. A polytropic structure model does not by itself calculate nuclear energy generation or energy transport.

| Symbol | Meaning |
| --- | --- |
| r | Physical radial coordinate |
| rho(r) | Mass density |
| P(r) | Pressure |
| M(r) | Mass enclosed within radius r |
| Phi(r) | Newtonian gravitational potential |
| G | Gravitational constant |
| K | Positive polytropic constant |
| n | Polytropic index, defining the pressure-density exponent |
| rho_c | Central density of a regular model |
| alpha | Radial scale used for nondimensionalization |
| xi = r/alpha | Dimensionless radius |
| theta(xi) | Dimensionless enthalpy variable; rho/rho_c = theta^n |

## 2. Governing equations

Mass conservation for a spherical shell gives

$$
\frac{dM}{dr}=4\pi r^2\rho.
$$

Hydrostatic equilibrium requires

$$
\frac{dP}{dr}=-\frac{GM\rho}{r^2}.
$$

With outward r taken as positive, the gravitational acceleration is $-GM/r^2$. The pressure acceleration is $-(1/\rho)dP/dr$, so a pressure that decreases outward provides outward support.

The polytropic equation of state closes the system:

$$
P=K\rho^{1+1/n},\qquad n>0.
$$

Changing n changes how pressure responds to density. The exponent $1+1/n$ describes this equilibrium relation; it is not automatically the adiabatic exponent for perturbations unless further thermodynamic assumptions are supplied. Consequently, the equilibrium calculation alone does not establish dynamical stability.

The corresponding gravitational-potential equation is

$$
\nabla^2\Phi=4\pi G\rho,\qquad
\frac{d\Phi}{dr}=\frac{GM}{r^2}
$$

for a regular spherical source. These equations express the same gravitational balance in potential form. See the [polytrope lecture notes hosted at the University of Minnesota](https://www-users.cse.umn.edu/~kd/Ast4001-2015/NOTES/n062-polytropes-caltech.pdf) for the standard physical setup.

## 3. Deriving the Lane-Emden equation

The following steps make the nondimensionalization explicit. Divide hydrostatic equilibrium by rho, multiply by r squared and differentiate:

$$
\frac{1}{r^2}\frac{d}{dr}
\left(\frac{r^2}{\rho}\frac{dP}{dr}\right)
=-4\pi G\rho.
$$

For the stated equation of state, the specific enthalpy, with zero chosen at zero density, is

$$
h(\rho)=\int_0^\rho\frac{1}{\tilde\rho}
\frac{dP}{d\tilde\rho}\,d\tilde\rho
=(n+1)K\rho^{1/n}.
$$

Thus $dh/dr=(1/\rho)dP/dr$, and hydrostatic equilibrium also states that $h+\Phi$ is constant within a connected fluid region. Introduce

$$
\rho=\rho_c\theta^n,\qquad
P=K\rho_c^{1+1/n}\theta^{n+1},\qquad
r=\alpha\xi,
$$

with

$$
\alpha^2=\frac{(n+1)K}{4\pi G}\rho_c^{1/n-1}.
$$

Since $h=(n+1)K\rho_c^{1/n}\theta$, substitution yields

$$
\boxed{\frac{1}{\xi^2}\frac{d}{d\xi}
\left(\xi^2\frac{d\theta}{d\xi}\right)+\theta^n=0.}
$$

Equivalently, $\theta''+2\theta'/\xi+\theta^n=0$. The equation is nonlinear except at special indices. Theta is proportional to enthalpy on the physical branch; it is not generally the density itself.

## 4. Regular stellar models and more general solution families

A finite central density and spherical regularity impose

$$
\theta(0)=1,\qquad\theta'(0)=0.
$$

For a fixed n and this normalization, these conditions select the regular solution. Its center expansion begins

$$
\theta(\xi)=1-\frac{\xi^2}{6}+\frac{n\xi^4}{120}+O(\xi^6).
$$

The first zero $\xi_1$ defines the surface of a finite regular polytrope, with physical radius $R=\alpha\xi_1$. Ordinary stellar profiles retain the branch with nonnegative density and pressure.

The differential equation also admits other initial-value problems posed away from the center. These can generate singular solutions, turning points or mathematical continuations outside the regular stellar branch. Investigating those families is a broader task than computing one standard stellar model. The undergraduate project explored this broader family with phase portraits. How such curves should be interpreted physically depends on their boundary conditions.

## 5. Enclosed mass and the integral hypothesis

Define the dimensionless mass of a regular model by

$$
m(\xi)=\frac{M(r)}{4\pi\rho_c\alpha^3}
=\int_0^\xi s^2\theta(s)^n\,ds.
$$

Integrating the Lane-Emden equation gives

$$
m(\xi)=-\xi^2\theta'(\xi).
$$

This provides two independent numerical routes to the same quantity: integrating the density profile or evaluating the slope. At the surface,

$$
M_\star=4\pi\rho_c\alpha^3
\left[-\xi_1^2\theta'(\xi_1)\right].
$$

For a regular positive-density model, mass is nondecreasing and is positive after any nonzero amount of matter has been enclosed. Therefore theta decreases outward. An interior turning point with zero enclosed mass cannot occur in such a model once positive mass has accumulated.

For a general interval, however, the correct identity is

$$
\int_{\xi_a}^{\xi_b}\xi^2\theta^n\,d\xi
=-\xi_b^2\theta'(\xi_b)+\xi_a^2\theta'(\xi_a).
$$

The lower-boundary contribution is essential for singular or noncentral initial conditions. This is the theoretical issue behind revisiting a proposed cancellation or zero-mass integral: a vanishing derivative at one endpoint is insufficient by itself. The undergraduate project tested a condition of this kind numerically.

## 6. Analytically solvable cases

| Index | Regular solution | Physical-branch property |
| --- | --- | --- |
| n = 0 | $\theta=1-\xi^2/6$ | Formal constant-density benchmark; first zero at $\sqrt{6}$ |
| n = 1 | $\theta=\sin\xi/\xi$ | First zero at pi; continuation oscillates beyond the surface |
| n = 5 | $\theta=(1+\xi^2/3)^{-1/2}$ | No finite zero; finite limiting dimensionless mass $\sqrt{3}$ |

The n=0 solution is a formal incompressible limit of the Lane-Emden equation, not a substitution of zero into $1+1/n$. These standard solutions supply independent numerical benchmarks. Background: [Vik Dhillon's Lane-Emden notes](https://vikdhillon.staff.shef.ac.uk/teaching/phy213/phy213_le.html).

For n=1, extending the analytic formula past pi creates intervals where theta and the standard density are negative. The oscillations are mathematically well defined, but they do not describe additional ordinary stellar layers. The formal integrated mass is $m=\sin\xi-\xi\cos\xi$, so a decaying oscillation in theta does not imply a decaying mass contribution: the radial volume weighting matters.

## 7. Why phase portraits help

A second-order equation can be written as two coupled first-order equations. Each initial condition then gives a trajectory in a two-dimensional state space. Phase portraits help identify equilibrium points, special trajectories, turning behavior and qualitative differences among solution families. Their axes are state variables, not spatial coordinates inside a star; a closed curve in a phase portrait is not a physical orbit of stellar material.

To treat the solution families as a dynamical system, the implementation defines, for n>1,

$$
t=\ln\xi,\quad a=\frac{2}{n-1},\quad
x=\xi^a\theta,\quad v=\frac{dx}{dt}.
$$

The transformed equations are

$$
\dot x=v,\qquad
\dot v=(2a-1)v+a(1-a)x-x^n.
$$

At n=5, the coefficient of v vanishes and

$$
E=\frac{v^2}{2}-\frac{x^2}{8}+\frac{x^6}{6}
$$

is conserved. Its level sets explain the possibility of two families of small loops and larger loops enclosing both centers in the mathematical extension. This helps interpret why n=5 is structurally special. The full transformation and domain restrictions are in [model.md](model.md).

## 8. Connection to the undergraduate investigation

The undergraduate project asked how the solution families change with n, what distinguishes special branches, whether selected mass integrals cancel, and which mathematical solutions admit a consistent gravitational interpretation. It examined n=4 in detail, compared non-integer indices on either side of 4, and studied the special cases n=1 and n=5. The activities and numerical results are summarized in [undergraduate-research.md](undergraduate-research.md).
