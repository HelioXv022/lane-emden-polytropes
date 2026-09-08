# Undergraduate research contributions

**Researcher:** Zi-Qi Xu  
**Research collaborator and supervisor, as identified by Zi-Qi Xu:** Prof. Yu-Qing Lou, Department of Physics, Tsinghua University  
**Stage:** Final undergraduate year  
**Research area:** Computational astrophysics and nonlinear differential equations

## Project summary

In this undergraduate project, I investigated the solution structure of self-gravitating polytropic spheres with Prof. Yu-Qing Lou. My work focused on numerical exploration of Lane-Emden-type solution families, comparison of phase portraits and radial profiles across polytropic indices, and mass-integral calculations used to test proposed interpretations of special branches.

The surviving progress report credits Yu-Qing Lou and Zi-Qi Xu jointly. The account below describes my participation in the research documented there; the excerpt does not specify an exclusive person-by-person division of every calculation or derivation. The Python package in this repository is a subsequent reference implementation and is described separately at the end.

## 1. Numerical exploration and classification at n = 4

The n=4 case formed a detailed part of the investigation. The work compared a phase portrait with radial curves to distinguish several labeled solution families and examine their qualitative behavior.

The report discusses a special branch labeled with N* symbols and a sequence of signs, and provides one initial condition: ln(z)=0, w(z)=0.5 and dw/dz=0.5. It then investigates whether the shape of that branch could be associated with a hollow interior and how pressure-gradient and gravitational terms would balance.

**Documented output:** Figures 3–5 and Section 2 on printed page 4. The complete classification notation and coordinate definitions belong to the missing earlier pages, so those labels are preserved as historical notation rather than assigned new meanings.

**Contribution represented:** numerical solution-family exploration, cross-comparison of phase-space and radial representations, and analysis of candidate physical interpretations.

## 2. Mass-integral calculations and resolution checks

The work selected two n=4 curves and used numerical sampling with an ODE solver followed by Simpson integration to examine a proposed zero-integral condition up to a point where the derivative vanishes. The report mentions ode89 for sampling in this calculation.

The original displayed results are:

| Reported integration step size | Curve 1 integral | Curve 2 integral |
| --- | --- | --- |
| 0.001 | 0.0013 | 1.2853 |
| 0.0001 | 0.0013 | 1.2853 |
| 0.00001 | 0.0013 | 1.2853 |

The values are stable to the displayed four decimal places across the three step sizes. They do not demonstrate that both integrals are zero. The report explicitly identifies loss of numerical accuracy near a singular point as an unresolved issue.

**Documented output:** Table 1, Figure 5 and the accompanying discussion on printed page 4; the values are transcribed in [n4_table1.csv](../data/historical/n4_table1.csv).

**Contribution represented:** numerical quadrature, a step-size comparison, quantitative testing of a research hypothesis, and recognition of numerical difficulties near singularities. The original integrand, normalization and complete endpoint definitions are not available, so this table is not presented as independently reproduced.

## 3. Comparison of noninteger polytropic indices

The investigation compared behavior in the ranges 3<n<4 and 4<n<5. The report states that indices between 3 and 4 were sampled at increments of 0.1, and presents n=3.5 as an example of a more tangled numerical pattern. It also presents n=4.5 and describes its qualitative behavior as similar to n=4.

The methods mentioned in this part include ode45 and ode113. The n=4.5 prose reports using ode113 because ode45 took too long; one caption still names ode45. The original files would be needed to determine which solver produced each figure.

**Documented output:** Section 3 on printed page 4 and Figures 6–9 on printed page 5.

**Contribution represented:** parameter scanning, qualitative comparison of nonlinear solution families, and consideration of numerical-solver efficiency. Although the report calls the n=3.5 pattern chaotic, the excerpt does not establish deterministic chaos; that remains an interpretation requiring further analysis.

## 4. Study of the special n = 5 phase structure

The n=5 investigation identified a distinctive, approximately centrosymmetric double-lobed pattern. The report discusses loops, deformed loops and curves associated with the origin, then groups the loop-like curves together in its qualitative classification.

**Documented output:** Figure 10 and Section 4 on printed page 5. Section 4 refers to Figure 4, but Figure 10 is the displayed n=5 phase plot; the cross-reference appears inconsistent.

**Contribution represented:** recognition of a qualitative change at a special polytropic index and classification of phase-space geometry. The conserved-energy explanation derived in this repository is a later addition; it is not claimed as a recovered original derivation.

## 5. Oscillatory solutions and cancellation tests at n = 1

The n=1 study examined oscillations whose amplitude decreases as radius increases and tested whether contributions from successive regions cancel. The report gives an integral of -3.1835 for one test and concludes that the corresponding cancellation assumption does not hold. A subsequent calculation gives 6.3397 over a further interval and motivates the statement that a positive contribution can offset an earlier negative contribution before a later zero.

**Documented output:** Section 5 on printed pages 5–6 and Figures 11–12 on printed page 6.

**Contribution represented:** analysis of oscillatory radial behavior, numerical integration over selected regions, and revision of a hypothesis in response to computed results. The missing bounds and normalization prevent reconstructing these exact numbers. The standard n=1 analytic demonstration supplied with the new code is a separate calculation.

## 6. Physical interpretation and research documentation

The report connects numerical profiles to questions about pressure gradients, gravitational balance, hollow regions and formal negative-mass behavior. It also proposes a possible neutrino explanation for a dense region surrounding a hollow interior, explicitly naming it as a second assumption.

These discussions show an effort to connect mathematical solutions with physical mechanisms. A verified hollow-star or neutrino model would require additional equations and boundary conditions not provided in the excerpt. The work is therefore described as investigation of candidate interpretations, rather than discovery of an established physical object.

The surviving coauthored progress report records the numerical figures, table and open questions. Its running title is *Gravitational Lensing of Polytropic Spheres*, but no lensing observable is calculated in these three pages.

## Technical skills demonstrated by the historical work

| Skill | Evidence in the report |
| --- | --- |
| Numerical ODE analysis | Use of ode45, ode89 and ode113 in the described workflow |
| Parameter exploration | Comparison of n=1, 3.5, 4, 4.5 and 5; reported scan within 3<n<4 |
| Phase-space analysis | Classification and comparison of plotted solution families |
| Numerical quadrature | Simpson integration for the n=4 and n=1 hypotheses |
| Numerical diagnostics | Multiple step sizes, solver-runtime discussion and singularity concerns |
| Physical reasoning | Examination of equilibrium, pressure gradients and mass interpretation |
| Scientific communication | Joint progress report containing figures, a numerical table and unresolved questions |

## Subsequent additions in this repository

The following items were newly prepared with AI assistance when organizing this repository: the standard-theory exposition, an explicit autonomous-coordinate derivation, the Python reference solver, analytic and integral tests, CSV datasets generated by that solver, and the four new figures. These are distinguishable from the historical report and its transcribed table.

The new code solves regular central models and selected illustrative mathematical extensions. It does not recover the original MATLAB programs or reproduce all historical branch families. This distinction allows the repository to present the original research clearly while providing a practical basis for future reconstruction.
