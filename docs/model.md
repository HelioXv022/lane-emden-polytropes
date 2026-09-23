# Model and numerical conventions

## Standard physical model

For spherical Newtonian hydrostatic equilibrium,

$$
\frac{dM}{dr}=4\pi r^2\rho,\qquad
\frac{dP}{dr}=-\frac{GM\rho}{r^2},\qquad
P=K\rho^{1+1/n}.
$$

For n > 0, choose $\rho=\rho_c\theta^n$, $r=\alpha\xi$ and

$$
\alpha^2=\frac{(n+1)K}{4\pi G}\rho_c^{1/n-1}.
$$

These assumptions give $\theta''+2\theta'/\xi+\theta^n=0$. Here n=0 is used only as the formal constant-density Lane–Emden benchmark, not by substituting zero into the stated equation of state. Background: [Caltech polytrope lecture notes, hosted at the University of Minnesota](https://www-users.cse.umn.edu/~kd/Ast4001-2015/NOTES/n062-polytropes-caltech.pdf).

## Regular center and physical surface

The new implementation uses $\theta(0)=1$ and $\theta'(0)=0$. Direct integration from zero would divide by zero. Its initial values at $\epsilon=10^{-5}$ follow the series

$$
\theta(\epsilon)=1-\frac{\epsilon^2}{6}+\frac{n\epsilon^4}{120}+O(\epsilon^6),\quad
\theta'(\epsilon)=-\frac{\epsilon}{3}+\frac{n\epsilon^3}{30}+O(\epsilon^5).
$$

The integration stops at the first zero of theta. Fractional powers are evaluated with `max(theta, 0)**n` inside trial steps only so that the solver can locate the zero; this is not a claimed negative-domain extension. A sampled zero is inserted at the event endpoint. For n=5, reaching xi=40 means only that the chosen interval ended, not that a finite surface was found.

DOP853 uses rtol=1e-10, atol=1e-12 and max_step=0.1. Profiles include the center explicitly and use 4,001 total samples by default. A failed integrator raises an exception. The implementation is a new reference, with no equivalence claim to the old MATLAB settings.

## Mass identity and its boundary term

Directly integrating $(\xi^2\theta')'=-\xi^2\theta^n$ gives

$$
\int_{\xi_a}^{\xi_b}\xi^2\theta^n\,d\xi
=-\xi_b^2\theta'(\xi_b)+\xi_a^2\theta'(\xi_a).
$$

At a regular center the second term tends to zero. The physical mass is $M=4\pi\rho_c\alpha^3m$, where $m=-\xi^2\theta'$. For a singular branch, the lower-boundary limit may be nonzero or divergent; it must not be discarded without analysis. A zero derivative at the upper limit alone is not sufficient to prove a zero integral on an arbitrary branch.

The new solver checks m against independent Simpson quadrature. `quadrature_convergence.csv` changes sample resolution with the ODE tolerances held fixed; it tests the quadrature and sampling contribution, not full solver convergence near singularities.

## A new autonomous transformation

The following autonomous transformation follows directly from the standard equation.

For n > 1, define

$$
t=\ln\xi,\qquad a=\frac{2}{n-1},\qquad
x=\xi^a\theta,\qquad v=\frac{dx}{dt}.
$$

Substituting $\theta=e^{-at}x$ gives

$$
\frac{dx}{dt}=v,\qquad
\frac{dv}{dt}=(2a-1)v+a(1-a)x-x^n.
$$

For n > 3 the positive fixed point is $x_s=[a(1-a)]^{1/(n-1)}$, v=0. It corresponds to the singular power-law solution $\theta=x_s\xi^{-a}$, which is distinct from a regular center. The phase plot marks this point in red.

Define

$$
E(x,v)=\frac{v^2}{2}+\frac{a(a-1)x^2}{2}+\frac{x^{n+1}}{n+1}.
$$

Differentiation along a trajectory yields the identity

$$
\frac{dE}{dt}=(2a-1)v^2=\frac{5-n}{n-1}v^2.
$$

Thus n=5 removes this effective damping/antidamping term and yields

$$
E=\frac{v^2}{2}-\frac{x^2}{8}+\frac{x^6}{6}=\mathrm{constant}.
$$

The double-well potential explains two sets of small closed contours, a zero-energy separatrix, and larger closed contours enclosing both wells. This is the double-lobed structure seen in the n=5 phase portraits of the undergraduate project. The E=0 separatrix reaches the origin asymptotically; it does not pass through that equilibrium in finite t.

The phase function permits negative x only for integer n. A signed-power rule such as `sign(x)*abs(x)**n` for fractional n would define another equation and is not used. The n=3.5, 4, 4.5, 5 comparison displays x>=0 only. In the n=5 full-plane figure, negative x is a mathematical extension; it implies negative theta and negative density in the standard mapping.

The monotone E identity for 1<n<5 also prevents nontrivial closed orbits on smooth solution domains in this particular transformed system. Dense plotted curves alone therefore do not establish chaotic dynamics. Since this is a two-dimensional autonomous flow, chaos is ruled out in any case by the Poincaré–Bendixson theorem.

## Analytic benchmarks and signed continuation

The standard regular solutions are $\theta_0=1-\xi^2/6$, $\theta_1=\sin\xi/\xi$, and $\theta_5=(1+\xi^2/3)^{-1/2}$. See [Vik Dhillon's analytic-solution notes](https://vikdhillon.staff.shef.ac.uk/teaching/phy213/phy213_le.html).

For the n=1 mathematical continuation,

$$
m(\xi)=\sin\xi-\xi\cos\xi.
$$

The standard physical model ends at pi. The first positive lobe contributes pi to the formal mass integral, the next negative lobe contributes -3pi, and the total to 2pi is -2pi. These values use the standard normalization; the numbers in the undergraduate study (-3.1835 and 6.3397) used different integration bounds and are not directly comparable.

For n=5 the exact mass is $m(\xi)=\xi^3/[3(1+\xi^2/3)^{3/2}]$, with limiting total mass $\sqrt{3}$. The plotted endpoint at xi=40 gives only the enclosed mass within that finite radius.
